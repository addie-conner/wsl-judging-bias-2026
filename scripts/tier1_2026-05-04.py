"""TIER 1 — Hierarchical Bayes, sensitivity, FDR, synth control, causal forest, XGB+SHAP, PPC, permutation.

All local. Zero LLM tokens. Writes outputs/tier1_results.json + console.
"""
import json, warnings, math, time
from pathlib import Path
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore")

ROOT = Path("/Users/addieconner/chorus/wsl")
HEATS = pd.read_parquet(ROOT / "data" / "heats.parquet")
JUDGES = pd.read_parquet(ROOT / "data" / "judges.parquet")
df = HEATS[HEATS["wave_score"] > 0].copy()
df["surfer_id"] = df["surfer_athlete_id"].fillna(df["surfer_name_full"]).astype(str)

results: dict = {}

def stamp(title):
    print(f"\n{'='*72}\n{title}\n{'='*72}", flush=True)

# ---------------------------------------------------------------
# T1.3 FDR correction (Benjamini-Hochberg) on the test family
# ---------------------------------------------------------------
stamp("T1.3 FDR correction (Benjamini-Hochberg)")
from statsmodels.stats.multitest import multipletests

# Pull p-values from prior outputs
prior = {}
for fn in ["full_paper_grade_results.json", "comprehensive_stats_2026-05-04.json",
           "full_data_rerun_results.json", "median_polish_rf_interactions_results.json",
           "sophisticated_stats_results.json"]:
    p = ROOT / "outputs" / fn
    if p.exists():
        prior[fn] = json.load(open(p))

# Collect p-values
pvals = []
def collect_p(d, prefix=""):
    if isinstance(d, dict):
        for k, v in d.items():
            kp = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict):
                collect_p(v, kp)
            elif k in ("p", "pvalue", "p_value", "sc_p", "ols_p") and isinstance(v, (int, float)):
                if 0 < v <= 1: pvals.append((kp, float(v)))

for fn, d in prior.items(): collect_p(d, fn)
print(f"  Collected {len(pvals)} p-values from prior outputs.", flush=True)
ps = np.array([p for _, p in pvals])
rej_bh, p_bh, _, _ = multipletests(ps, alpha=0.05, method="fdr_bh")
rej_bonf, p_bonf, _, _ = multipletests(ps, alpha=0.05, method="bonferroni")
print(f"  Survive BH(0.05): {rej_bh.sum()}/{len(ps)}    Bonferroni: {rej_bonf.sum()}/{len(ps)}", flush=True)
top_surv = sorted(zip([k for k, _ in pvals], ps, p_bh), key=lambda x: x[2])[:15]
print("  Top-15 surviving (lowest BH-adjusted p):", flush=True)
for name, p_raw, p_a in top_surv:
    print(f"    {name}: p={p_raw:.4g} -> BH p={p_a:.4g}", flush=True)
results["FDR"] = {
    "n_tests": len(ps),
    "n_survive_BH_05": int(rej_bh.sum()),
    "n_survive_bonferroni_05": int(rej_bonf.sum()),
    "top_surviving": [{"name": n, "p_raw": float(p), "p_bh": float(pa)} for n, p, pa in top_surv],
}

# ---------------------------------------------------------------
# T1.2 Sensitivity — Rosenbaum bounds (Γ) + E-value (VanderWeele-Ding)
# ---------------------------------------------------------------
stamp("T1.2 Sensitivity — Rosenbaum bounds + E-value for AUS bloc")
import statsmodels.api as sm
df["aus_match"] = ((df["surfer_country"] == "AUS") & (df["event_country"] == "AUS")).astype(int)
y = df["wave_score"].astype(float).values
T = df["aus_match"].astype(int).values
X = sm.add_constant(T)
res = sm.OLS(y, X).fit(cov_type="cluster", cov_kwds={"groups": df["surfer_id"].values})
beta = float(res.params[1]); se = float(res.bse[1])
mean_ctrl = float(df.loc[T == 0, "wave_score"].mean())
rr = (mean_ctrl + beta) / mean_ctrl
# E-value for risk-ratio (VanderWeele-Ding 2017)
e_val = rr + math.sqrt(rr * (rr - 1)) if rr > 1 else 1/rr + math.sqrt((1/rr) * (1/rr - 1))
ci_lo_rr = (mean_ctrl + beta - 1.96 * se) / mean_ctrl
e_val_ci = ci_lo_rr + math.sqrt(ci_lo_rr * (ci_lo_rr - 1)) if ci_lo_rr > 1 else 1.0
print(f"  Risk ratio (treated vs ctrl): {rr:.4f}", flush=True)
print(f"  E-value (point): {e_val:.3f}", flush=True)
print(f"  E-value (CI lower bound): {e_val_ci:.3f}", flush=True)
print(f"  Interpretation: an unobserved confounder would need RR>={e_val:.2f} with both treatment and outcome to overturn.", flush=True)

# Rosenbaum Γ scan (paired-comparison framework approximation via heat-pair within-event match)
gammas = [1.0, 1.5, 2.0, 2.5, 3.0, 5.0]
ros_scan = []
for g in gammas:
    # Approximation: how would the lower bound on the test statistic shift under bias multiplier g?
    # Use logistic transform on (beta/se) shifted by ln(g)
    z = beta / se
    z_ros = (z - math.log(g)) / 1  # standardized shift; approximation
    p_g = float(1 - 0.5 * (1 + math.erf(z_ros / math.sqrt(2))))
    ros_scan.append({"gamma": g, "z_under_bias": float(z_ros), "p_one_sided": p_g})
    print(f"  Γ={g}: z={z_ros:.2f}, p={p_g:.4g}", flush=True)
results["sensitivity"] = {
    "rr_aus_bloc": rr, "e_value_point": e_val, "e_value_ci_lower": e_val_ci,
    "rosenbaum_scan": ros_scan,
}

# ---------------------------------------------------------------
# T1.4 Synthetic control for 2023 BRA panel-policy break
# ---------------------------------------------------------------
stamp("T1.4 Synthetic control — BRA panel-rate post-2023 break")
nat_cols = [c for c in JUDGES.columns if c.startswith("judge_") and "nationality" in c]
Jn = JUDGES.dropna(subset=nat_cols).copy()
sn_map = (HEATS.dropna(subset=["surfer_country", "surfer_name_full"])
          .drop_duplicates("surfer_name_full")
          .set_index("surfer_name_full")["surfer_country"].to_dict())
Jn["surfer_country_iso"] = Jn["surfer_name"].map(sn_map)

ISO_NAME = {"AUS":"Australia", "BRA":"Brazil", "USA":"United States",
            "FRA":"France", "ZAF":"South Africa"}
def nat_count_for(g, full):
    return sum(1 for c in nat_cols if g.get(c) == full)

# Build per-year mean compatriot count for AUS, BRA, USA, FRA, ZAF
yearly = {}
for iso, full in ISO_NAME.items():
    sub = Jn[Jn["surfer_country_iso"] == iso].copy()
    sub["n_compat"] = sub.apply(lambda r: nat_count_for(r, full), axis=1)
    yr_means = sub.groupby("year")["n_compat"].mean().to_dict()
    yearly[iso] = yr_means

years = sorted({y for d in yearly.values() for y in d.keys()})
print("  Year |  AUS  |  BRA  |  USA  |  FRA  |  ZAF", flush=True)
for y in years:
    row = "  " + str(int(y)) + " | "
    row += " | ".join([f"{yearly[iso].get(y, np.nan):.2f}" if y in yearly[iso] else "  -- " for iso in ISO_NAME])
    print(row, flush=True)

# Synthetic control: predict BRA from convex combo of AUS/USA/FRA/ZAF in pre-period (2018-2022), compare 2023+
pre_years = [2018, 2019, 2021, 2022]
post_years = [2023, 2024, 2025, 2026]
donors = ["AUS", "USA", "FRA", "ZAF"]
Y_bra_pre = np.array([yearly["BRA"].get(y, np.nan) for y in pre_years])
X_donors_pre = np.array([[yearly[d].get(y, np.nan) for d in donors] for y in pre_years])

# Drop years missing data
valid = ~np.isnan(Y_bra_pre) & ~np.isnan(X_donors_pre).any(axis=1)
Y_bra_pre = Y_bra_pre[valid]
X_donors_pre = X_donors_pre[valid]
print(f"  Synth control: {valid.sum()} pre-period years, {len(donors)} donors.", flush=True)

# Solve constrained LS: w >= 0, sum(w) == 1, minimize ||Y - Xw||
from scipy.optimize import minimize
def loss(w):
    return ((Y_bra_pre - X_donors_pre @ w) ** 2).sum()
cons = ({"type": "eq", "fun": lambda w: w.sum() - 1.0},)
bnds = [(0, 1)] * len(donors)
w0 = np.ones(len(donors)) / len(donors)
opt = minimize(loss, w0, constraints=cons, bounds=bnds, method="SLSQP")
w = opt.x
print(f"  Synthetic-BRA weights: {dict(zip(donors, np.round(w, 3).tolist()))}", flush=True)
synth_post = []
for y in post_years:
    if not all(y in yearly[d] for d in donors): continue
    pred = sum(w[i] * yearly[donors[i]][y] for i in range(len(donors)))
    actual = yearly["BRA"].get(y, np.nan)
    synth_post.append({"year": int(y), "synthetic": float(pred),
                       "actual_BRA": float(actual) if not np.isnan(actual) else None,
                       "gap": float(actual - pred) if not np.isnan(actual) else None})
    print(f"  {y}: synthetic={pred:.3f}, actual_BRA={actual:.3f}, gap={actual - pred:+.3f}", flush=True)
results["synth_control_BRA_panel"] = {
    "weights": dict(zip(donors, w.tolist())),
    "post_period": synth_post,
}

# ---------------------------------------------------------------
# T1.6 XGBoost + SHAP
# ---------------------------------------------------------------
stamp("T1.6 XGBoost + SHAP")
import xgboost as xgb
import shap

rf_df = df.dropna(subset=["surfer_world_rank_at_event_start", "wave_score"]).copy()
top_c = rf_df["surfer_country"].value_counts().head(10).index.tolist()
top_ec = rf_df["event_country"].value_counts().head(10).index.tolist()
Xf = pd.DataFrame()
Xf["rank"] = rf_df["surfer_world_rank_at_event_start"].astype(float)
Xf["year"] = rf_df["year"].astype(float)
Xf["is_male"] = (rf_df["gender"] == "m").astype(float)
Xf["heat_number"] = pd.to_numeric(rf_df["heat_number"], errors="coerce").fillna(0).astype(float)
Xf["wave_index_for_surfer"] = pd.to_numeric(rf_df["wave_index_for_surfer"], errors="coerce").fillna(0).astype(float)
Xf["wave_position_in_heat"] = pd.to_numeric(rf_df["wave_global_position_in_heat"], errors="coerce").fillna(0).astype(float)
Xf["home_match"] = (rf_df["surfer_country"] == rf_df["event_country"]).astype(float)
for c in top_c: Xf[f"sc_{c}"] = (rf_df["surfer_country"] == c).astype(float)
for c in top_ec: Xf[f"ec_{c}"] = (rf_df["event_country"] == c).astype(float)
y = rf_df["wave_score"].astype(float).values

print(f"  n={len(y):,}, n_features={Xf.shape[1]}", flush=True)
xgb_m = xgb.XGBRegressor(n_estimators=200, max_depth=6, learning_rate=0.05, random_state=42, n_jobs=4)
xgb_m.fit(Xf.values, y)
print(f"  XGBoost R² (in-sample): {xgb_m.score(Xf.values, y):.4f}", flush=True)
expl = shap.TreeExplainer(xgb_m)
sample_idx = np.random.RandomState(42).choice(len(Xf), min(2000, len(Xf)), replace=False)
shap_vals = expl.shap_values(Xf.values[sample_idx])
shap_imp = np.abs(shap_vals).mean(axis=0)
imp_df = pd.DataFrame({"feature": Xf.columns, "shap_imp": shap_imp}).sort_values("shap_imp", ascending=False)
print("  Top-10 SHAP importances:", flush=True)
for _, r in imp_df.head(10).iterrows():
    print(f"    {r['feature']}: |SHAP|={r['shap_imp']:.4f}", flush=True)
results["xgboost_shap"] = {
    "r2": float(xgb_m.score(Xf.values, y)),
    "top10_shap": imp_df.head(10).to_dict(orient="records"),
}

# ---------------------------------------------------------------
# T1.5 Causal forest — heterogeneous AUS-bloc effect
# ---------------------------------------------------------------
stamp("T1.5 Causal forest — heterogeneous AUS-bloc effect")
from econml.dml import CausalForestDML
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

dml_df = df.dropna(subset=["surfer_country", "event_country", "surfer_world_rank_at_event_start"]).copy()
dml_df["aus_match"] = ((dml_df["surfer_country"] == "AUS") & (dml_df["event_country"] == "AUS")).astype(int)
top_c = dml_df["surfer_country"].value_counts().head(8).index.tolist()
top_ec = dml_df["event_country"].value_counts().head(8).index.tolist()
Xc = pd.DataFrame()
Xc["rank"] = dml_df["surfer_world_rank_at_event_start"].astype(float).fillna(50)
Xc["year"] = dml_df["year"].astype(float)
Xc["is_male"] = (dml_df["gender"] == "m").astype(float)
for c in top_c: Xc[f"sc_{c}"] = (dml_df["surfer_country"] == c).astype(float)
for c in top_ec: Xc[f"ec_{c}"] = (dml_df["event_country"] == c).astype(float)

Y = dml_df["wave_score"].astype(float).values
T = dml_df["aus_match"].astype(int).values
print(f"  n={len(Y):,}, n_treated={T.sum()}", flush=True)
cf = CausalForestDML(
    model_y=RandomForestRegressor(n_estimators=50, max_depth=4, random_state=42, n_jobs=4),
    model_t=RandomForestClassifier(n_estimators=50, max_depth=4, random_state=42, n_jobs=4),
    n_estimators=200, max_depth=4, discrete_treatment=True, random_state=42, cv=3,
)
cf.fit(Y, T, X=Xc.values)
ate = np.asarray(cf.const_marginal_effect(Xc.values)).ravel()
ci_lo_arr = np.asarray(cf.const_marginal_effect_interval(Xc.values, alpha=0.05)[0]).ravel()
ci_hi_arr = np.asarray(cf.const_marginal_effect_interval(Xc.values, alpha=0.05)[1]).ravel()
print(f"  Causal-forest ATE: {ate.mean():+.4f}, 95% CI [{ci_lo_arr.mean():+.4f}, {ci_hi_arr.mean():+.4f}]", flush=True)
print(f"  CATE std (pop heterogeneity): {ate.std():.4f}", flush=True)
# Heterogeneity by rank quartile
q = pd.qcut(Xc["rank"].values, 4, labels=False, duplicates="drop")
q_arr = np.asarray(q).ravel()
het = pd.DataFrame({"rank_q": q_arr, "cate": ate}).groupby("rank_q")["cate"].mean()
print(f"  CATE by rank quartile (Q1=top, Q4=bottom):", flush=True)
for qi, val in het.items():
    print(f"    Q{int(qi)+1}: {val:+.4f}", flush=True)
results["causal_forest"] = {
    "ate": float(ate.mean()), "ci_lo": float(ci_lo_arr.mean()), "ci_hi": float(ci_hi_arr.mean()),
    "cate_std": float(ate.std()),
    "cate_by_rank_quartile": {int(k)+1: float(v) for k, v in het.items()},
}

# ---------------------------------------------------------------
# T1.8 Permutation test on H32 BRA-panel-rate decline
# ---------------------------------------------------------------
stamp("T1.8 Permutation test — H32 BRA-panel-rate trend (2018→2026)")
bra_J = Jn[Jn["surfer_country_iso"] == "BRA"].copy()
bra_J["n_bra"] = bra_J.apply(lambda r: nat_count_for(r, "Brazil"), axis=1)
yr_obs = bra_J.groupby("year")["n_bra"].mean()
years_a = np.array(sorted(yr_obs.index.astype(int)))
vals_a = np.array([yr_obs[y] for y in years_a])
print(f"  Observed BRA-panel-rate by year:", dict(zip(years_a.tolist(), np.round(vals_a, 3).tolist())), flush=True)

# Observed trend: simple slope
obs_slope = np.polyfit(years_a, vals_a, 1)[0]
print(f"  Observed slope: {obs_slope:+.4f} per year", flush=True)

# Permutation null: shuffle year labels within bra_J, re-compute slope, repeat
rng = np.random.RandomState(42)
n_perm = 1000
null_slopes = []
for _ in range(n_perm):
    perm_year = rng.permutation(bra_J["year"].values)
    yr_perm = bra_J.assign(yr_p=perm_year).groupby("yr_p")["n_bra"].mean()
    yp = np.array(sorted(yr_perm.index.astype(int)))
    vp = np.array([yr_perm[y] for y in yp])
    null_slopes.append(np.polyfit(yp, vp, 1)[0])
null_slopes = np.array(null_slopes)
p_perm = (np.abs(null_slopes) >= np.abs(obs_slope)).mean()
print(f"  Permutation p (B={n_perm}): {p_perm:.4g}  (two-sided)", flush=True)
print(f"  Null distribution: mean={null_slopes.mean():+.4f}, sd={null_slopes.std():.4f}", flush=True)
results["H32_permutation"] = {
    "observed_slope": float(obs_slope), "p_perm": float(p_perm),
    "null_mean": float(null_slopes.mean()), "null_sd": float(null_slopes.std()), "n_perm": n_perm,
}

# ---------------------------------------------------------------
# T1.1 Hierarchical Bayes (PyMC) — surfer + event REs on T2 rank prior
# T1.7 Posterior predictive checks
# ---------------------------------------------------------------
stamp("T1.1 + T1.7 Hierarchical Bayes (PyMC) + posterior predictive checks")
import pymc as pm
import arviz as az
t2 = df.dropna(subset=["surfer_world_rank_at_event_start"]).copy()
t2["rank"] = t2["surfer_world_rank_at_event_start"].astype(float)
t2["surfer_idx"] = pd.Categorical(t2["surfer_id"]).codes
t2["event_idx"] = pd.Categorical(t2["event_code"]).codes
# Subsample for tractability
ns = min(15000, len(t2))
ts = t2.sample(ns, random_state=42)
n_surfer = ts["surfer_idx"].nunique()
n_event = ts["event_idx"].nunique()
print(f"  n={ns:,}, n_surfer={n_surfer}, n_event={n_event}", flush=True)

t0 = time.time()
with pm.Model() as hb:
    sigma_s = pm.HalfNormal("sigma_s", 1.5)
    sigma_e = pm.HalfNormal("sigma_e", 1.5)
    sigma_obs = pm.HalfNormal("sigma_obs", 2.0)
    mu = pm.Normal("mu", 4.0, 2.0)
    beta_rank = pm.Normal("beta_rank", 0.0, 0.05)
    a_s = pm.Normal("a_s", 0, sigma_s, shape=n_surfer)
    a_e = pm.Normal("a_e", 0, sigma_e, shape=n_event)
    yhat = mu + beta_rank * ts["rank"].values + a_s[ts["surfer_idx"].values] + a_e[ts["event_idx"].values]
    pm.Normal("y", yhat, sigma_obs, observed=ts["wave_score"].values)
    idata = pm.sample(draws=500, tune=500, chains=2, target_accept=0.9, random_seed=42, progressbar=False)
    idata.extend(pm.sample_posterior_predictive(idata, random_seed=42, progressbar=False))
elapsed = time.time() - t0
print(f"  Sampling complete in {elapsed:.1f}s", flush=True)

post = idata.posterior
beta_post = post["beta_rank"].values.flatten()
sigma_s_post = post["sigma_s"].values.flatten()
sigma_e_post = post["sigma_e"].values.flatten()
sigma_o_post = post["sigma_obs"].values.flatten()
print(f"  beta_rank posterior: mean={beta_post.mean():+.5f}, 95% CrI [{np.percentile(beta_post, 2.5):+.5f}, {np.percentile(beta_post, 97.5):+.5f}]", flush=True)
print(f"  sigma_surfer (RE): mean={sigma_s_post.mean():.4f}, 95% CrI [{np.percentile(sigma_s_post, 2.5):.4f}, {np.percentile(sigma_s_post, 97.5):.4f}]", flush=True)
print(f"  sigma_event (RE): mean={sigma_e_post.mean():.4f}", flush=True)
print(f"  sigma_obs: mean={sigma_o_post.mean():.4f}", flush=True)

# ICCs
icc_s = (sigma_s_post**2) / (sigma_s_post**2 + sigma_e_post**2 + sigma_o_post**2)
icc_e = (sigma_e_post**2) / (sigma_s_post**2 + sigma_e_post**2 + sigma_o_post**2)
print(f"  ICC surfer: mean={icc_s.mean():.4f}; ICC event: mean={icc_e.mean():.4f}", flush=True)

# Posterior predictive: replicate H11 round-number rate
ppc = idata.posterior_predictive["y"].values  # (chain, draw, obs)
pp_flat = ppc.reshape(-1, ppc.shape[-1])
draw_idx = np.random.RandomState(42).choice(pp_flat.shape[0], 200, replace=False)
round_rates_pp = []
for di in draw_idx:
    s = pp_flat[di]
    last = (s * 100 % 100).astype(int) % 100
    rate = ((last == 0) | (last == 25) | (last == 50) | (last == 75)).mean()
    round_rates_pp.append(rate)
round_rates_pp = np.array(round_rates_pp)
last_obs = (ts["wave_score"].values * 100 % 100).astype(int) % 100
obs_round = ((last_obs == 0) | (last_obs == 25) | (last_obs == 50) | (last_obs == 75)).mean()
print(f"  PPC round-rate: posterior {round_rates_pp.mean():.3f} [{np.percentile(round_rates_pp, 2.5):.3f}, {np.percentile(round_rates_pp, 97.5):.3f}]   observed {obs_round:.3f}", flush=True)
ppc_pass = (obs_round >= np.percentile(round_rates_pp, 2.5)) and (obs_round <= np.percentile(round_rates_pp, 97.5))
ppc_verdict = "PASS — model recovers H11" if ppc_pass else "FAIL — Gaussian misspec wrt H11 (expected; cannot reproduce categorical rounding)"
print(f"  PPC verdict: {ppc_verdict}", flush=True)

results["hierarchical_bayes"] = {
    "beta_rank_mean": float(beta_post.mean()),
    "beta_rank_ci_lo": float(np.percentile(beta_post, 2.5)),
    "beta_rank_ci_hi": float(np.percentile(beta_post, 97.5)),
    "sigma_surfer_mean": float(sigma_s_post.mean()),
    "sigma_event_mean": float(sigma_e_post.mean()),
    "sigma_obs_mean": float(sigma_o_post.mean()),
    "icc_surfer": float(icc_s.mean()),
    "icc_event": float(icc_e.mean()),
    "n": int(ns),
    "elapsed_s": float(elapsed),
    "ppc_round_rate_mean": float(round_rates_pp.mean()),
    "ppc_round_rate_ci": [float(np.percentile(round_rates_pp, 2.5)), float(np.percentile(round_rates_pp, 97.5))],
    "ppc_observed_round_rate": float(obs_round),
    "ppc_pass": bool(ppc_pass),
}

# ---------------------------------------------------------------
out = ROOT / "outputs" / "tier1_results.json"
out.parent.mkdir(parents=True, exist_ok=True)
with open(out, "w") as f:
    json.dump(results, f, indent=2, default=str)
print(f"\n=> Wrote {out}", flush=True)
print("\n" + "="*72 + "\nTIER 1 DONE\n" + "="*72, flush=True)
