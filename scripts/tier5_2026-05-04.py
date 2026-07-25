"""TIER 5 — Mixture-Bayesian (Gaussian + atoms at .0/.25/.5/.75) for proper PPC,
permutation test on AUS-bloc, hold-out validation on reserved 2025 women's CT,
Callaway-Sant'Anna staggered DiD for BRA panel reform.

All local. Zero LLM tokens. Writes outputs/tier5_results.json.
"""
import json, warnings, time
from pathlib import Path
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent.parent
HEATS = pd.read_parquet(ROOT / "data" / "heats.parquet")
JUDGES = pd.read_parquet(ROOT / "data" / "judges.parquet")
HOLDOUT = pd.read_parquet(ROOT / "data" / "heats_holdout.parquet")
HOLDOUT_MANIFEST = json.load(open(ROOT / "data" / "HOLDOUT_MANIFEST.json"))

df = HEATS[HEATS["wave_score"] > 0].copy()
df["surfer_id"] = df["surfer_athlete_id"].fillna(df["surfer_name_full"]).astype(str)
results: dict = {}

def stamp(t): print(f"\n{'='*72}\n{t}\n{'='*72}", flush=True)

# ---------------------------------------------------------------
# T5.A Mixture-Bayesian (atoms at round values + Gaussian) — fix PPC for H11
# ---------------------------------------------------------------
stamp("T5.A Mixture-Bayesian (atoms + Gaussian) for H11 PPC fix")
import pymc as pm

t2 = df.dropna(subset=["surfer_world_rank_at_event_start"]).copy()
t2["rank"] = t2["surfer_world_rank_at_event_start"].astype(float)
ts = t2.sample(min(8000, len(t2)), random_state=42)
ys = ts["wave_score"].values

# Pre-cluster observations as round-or-not
last_dec = (ys * 100 % 100).astype(int)
is_round = ((last_dec == 0) | (last_dec == 25) | (last_dec == 50) | (last_dec == 75)).astype(int)
emp_round_rate = float(is_round.mean())
print(f"  n={len(ys):,}, observed round-rate={emp_round_rate:.4f}", flush=True)

t0 = time.time()
with pm.Model() as mix:
    pi_round = pm.Beta("pi_round", 2, 5)  # mass on round atoms
    mu = pm.Normal("mu", 4.0, 1.5)
    sigma = pm.HalfNormal("sigma", 2.0)
    sigma_atom = 0.05  # narrow atoms

    # 5-component flat mixture: 4 round atoms + 1 continuous Gaussian
    comps = [
        pm.Normal.dist(mu=0.0,  sigma=sigma_atom),
        pm.Normal.dist(mu=0.25, sigma=sigma_atom),
        pm.Normal.dist(mu=0.50, sigma=sigma_atom),
        pm.Normal.dist(mu=0.75, sigma=sigma_atom),
        pm.Normal.dist(mu=mu,   sigma=sigma),
    ]
    w_atom = pi_round / 4.0
    weights = pm.math.stack([w_atom, w_atom, w_atom, w_atom, 1.0 - pi_round])
    pm.Mixture("y", w=weights, comp_dists=comps, observed=ys)
    idata = pm.sample(draws=400, tune=400, chains=2, target_accept=0.9, random_seed=42, progressbar=False)
    idata.extend(pm.sample_posterior_predictive(idata, random_seed=42, progressbar=False))
elapsed = time.time() - t0

post = idata.posterior
pi_post = post["pi_round"].values.flatten()
print(f"  Sampling: {elapsed:.1f}s", flush=True)
print(f"  pi_round posterior: mean={pi_post.mean():.3f}, 95% CrI [{np.percentile(pi_post, 2.5):.3f}, {np.percentile(pi_post, 97.5):.3f}]", flush=True)

# PPC: simulate from posterior, check round-rate
ppc_mean = float(post["mu"].values.mean())
ppc_sigma = float(post["sigma"].values.mean())
ppc_pi = float(pi_post.mean())
rng = np.random.default_rng(42)
sim_y = []
for _ in range(2000):
    is_atom = rng.random(len(ys)) < ppc_pi
    atoms_arr = np.array([0.0, 0.25, 0.50, 0.75])
    yi = np.where(is_atom,
                  rng.choice(atoms_arr, len(ys)) + rng.normal(0, 0.05, len(ys)),
                  rng.normal(ppc_mean, ppc_sigma, len(ys)))
    sim_y.append(yi)
sim_y = np.array(sim_y)
sim_round = ((sim_y * 100 % 100).astype(int))
sim_rates = ((sim_round == 0) | (sim_round == 25) | (sim_round == 50) | (sim_round == 75)).mean(axis=1)
print(f"  PPC round-rate (mixture): mean={sim_rates.mean():.3f}, CI [{np.percentile(sim_rates, 2.5):.3f}, {np.percentile(sim_rates, 97.5):.3f}]", flush=True)
print(f"  Observed: {emp_round_rate:.3f}", flush=True)
ppc_pass = (emp_round_rate >= np.percentile(sim_rates, 2.5)) and (emp_round_rate <= np.percentile(sim_rates, 97.5))
verdict = "PASS — mixture model recovers H11" if ppc_pass else "FAIL — model still misspec"
print(f"  PPC verdict: {verdict}", flush=True)
results["mixture_bayesian_PPC"] = {
    "pi_round_mean": float(pi_post.mean()),
    "pi_round_ci": [float(np.percentile(pi_post, 2.5)), float(np.percentile(pi_post, 97.5))],
    "ppc_round_rate_mean": float(sim_rates.mean()),
    "ppc_round_rate_ci": [float(np.percentile(sim_rates, 2.5)), float(np.percentile(sim_rates, 97.5))],
    "observed_round_rate": emp_round_rate,
    "ppc_pass": bool(ppc_pass),
    "elapsed_s": float(elapsed),
}

# ---------------------------------------------------------------
# T5.B Permutation test on AUS bloc (parallel to H32)
# ---------------------------------------------------------------
stamp("T5.B Permutation test on AUS-bloc (10K reps, surfer-clustered)")

aus_match = ((df["surfer_country"] == "AUS") & (df["event_country"] == "AUS")).astype(float).values
y_full = df["wave_score"].astype(float).values
obs_diff = y_full[aus_match == 1].mean() - y_full[aus_match == 0].mean()
print(f"  Observed AUS-bloc diff (raw): {obs_diff:+.4f}", flush=True)

# Permutation null: shuffle aus_match within each event (preserves event-level structure)
event_codes = df["event_code"].values
ev_unique = np.unique(event_codes)
rng = np.random.RandomState(42)
n_perm = 10000
null_diffs = np.zeros(n_perm)
# Cluster permutation: shuffle treatment status of surfers within each event
df_perm = df[["surfer_id", "event_code", "wave_score"]].copy()
df_perm["aus"] = aus_match
for b in range(n_perm):
    # Permute treatment labels within each event
    shuffled = df_perm.groupby("event_code")["aus"].transform(
        lambda x: pd.Series(x.values).sample(frac=1, random_state=rng.randint(0, 1<<30)).values
    ).values
    null_diffs[b] = (df_perm.loc[shuffled == 1, "wave_score"].mean()
                     - df_perm.loc[shuffled == 0, "wave_score"].mean())
    if b % 2000 == 0 and b > 0:
        print(f"    {b}/{n_perm} done", flush=True)
p_perm = float((np.abs(null_diffs) >= np.abs(obs_diff)).mean())
print(f"  Permutation p (event-cluster, B={n_perm}): {p_perm:.4g}", flush=True)
print(f"  Null distribution: mean={null_diffs.mean():+.4f}, sd={null_diffs.std():.4f}", flush=True)
results["permutation_aus_bloc"] = {
    "observed_diff": float(obs_diff),
    "p_perm": p_perm,
    "null_mean": float(null_diffs.mean()),
    "null_sd": float(null_diffs.std()),
    "n_perm": n_perm,
    "method": "Within-event permutation of AUS-bloc treatment label",
}

# ---------------------------------------------------------------
# T5.C Hold-out validation on reserved 2025 women's CT (n=1,815)
# ---------------------------------------------------------------
stamp("T5.C Hold-out validation — 2025 women's CT (sealed)")
print(f"  Hold-out manifest: {HOLDOUT_MANIFEST}", flush=True)
print(f"  Hold-out rows: {len(HOLDOUT):,}", flush=True)
H = HOLDOUT[HOLDOUT["wave_score"] > 0].copy()
H["surfer_id"] = H["surfer_athlete_id"].fillna(H["surfer_name_full"]).astype(str)

# Replicate primary tests on held-out
import statsmodels.api as sm
from statsmodels.regression.linear_model import OLS

# T2 rank prior on hold-out
H2 = H.dropna(subset=["surfer_world_rank_at_event_start"]).copy()
H2["rank"] = H2["surfer_world_rank_at_event_start"].astype(float)
H2["heat_key"] = H2["event_code"].astype(str) + "_" + H2["heat_id"].astype(str)
def wd(s, g): return s - s.groupby(g).transform("mean")
y_h = wd(H2["wave_score"], H2["heat_key"]).values
x_h = wd(H2["rank"], H2["heat_key"]).values
X = sm.add_constant(x_h)
res_t2 = OLS(y_h, X).fit(cov_type="cluster", cov_kwds={"groups": H2["surfer_id"].values})
print(f"  T2 rank prior (hold-out): coef={res_t2.params[1]:+.5f}, p={res_t2.pvalues[1]:.4g}, n={len(H2):,}", flush=True)

# H11 round-number on hold-out (need per-judge data for full test, use trim-mean here)
last_dec = (H["wave_score"].values * 100 % 100).astype(int)
hold_round = ((last_dec == 0) | (last_dec == 25) | (last_dec == 50) | (last_dec == 75)).mean()
print(f"  H11 trim-mean round-rate (hold-out): {hold_round:.3f} (n={len(H):,})", flush=True)

# Compatriot effect (women-only proxy via surfer_country == event_country)
H["home"] = (H["surfer_country"] == H["event_country"]).astype(float)
res_h = OLS(H["wave_score"].values, sm.add_constant(H["home"].values)).fit(
    cov_type="cluster", cov_kwds={"groups": H["surfer_id"].values})
print(f"  Home-event effect (hold-out): coef={res_h.params[1]:+.4f}, p={res_h.pvalues[1]:.4g}, n_match={int(H['home'].sum())}", flush=True)

results["holdout_validation"] = {
    "manifest": HOLDOUT_MANIFEST,
    "n_holdout": int(len(H)),
    "T2_rank_prior_holdout": {"coef": float(res_t2.params[1]), "p": float(res_t2.pvalues[1]), "n": int(len(H2))},
    "H11_round_rate_holdout": float(hold_round),
    "home_event_holdout": {"coef": float(res_h.params[1]), "p": float(res_h.pvalues[1]),
                            "n_match": int(H["home"].sum())},
}

# ---------------------------------------------------------------
# T5.D Callaway-Sant'Anna staggered DiD for BRA panel reform
# ---------------------------------------------------------------
stamp("T5.D Callaway-Sant'Anna staggered DiD — BRA panel rotation")
nat_cols = [c for c in JUDGES.columns if c.startswith("judge_") and "nationality" in c]
sn_map = (HEATS.dropna(subset=["surfer_country", "surfer_name_full"])
          .drop_duplicates("surfer_name_full")
          .set_index("surfer_name_full")["surfer_country"].to_dict())
J = JUDGES.dropna(subset=nat_cols).copy()
J["surfer_country_iso"] = J["surfer_name"].map(sn_map)

# Per (year, surfer_country_iso) panel: mean compatriot count
ISO_NAME = {"AUS": "Australia", "BRA": "Brazil", "USA": "United States",
            "FRA": "France", "ZAF": "South Africa", "PRT": "Portugal",
            "JPN": "Japan", "ESP": "Spain", "PER": "Peru", "IDN": "Indonesia"}

def n_compat(row, full):
    return sum(1 for c in nat_cols if row[c] == full)

panel = []
for iso, full in ISO_NAME.items():
    sub = J[J["surfer_country_iso"] == iso].copy()
    if len(sub) < 50: continue
    sub["n_compat"] = sub.apply(lambda r: n_compat(r, full), axis=1)
    yr_means = sub.groupby("year")["n_compat"].mean()
    for yr, val in yr_means.items():
        panel.append({"year": int(yr), "country": iso, "n_compat": float(val), "n_obs": int((sub["year"] == yr).sum())})
panel_df = pd.DataFrame(panel)
print(f"  Panel: {len(panel_df)} country-year cells", flush=True)

# CS-style: BRA = treated (intervention 2023-10-11), others = controls
# Compute event-study: τ_yr = E[outcome_BRA_yr - outcome_control_yr] - same in pre-period
TREATED = "BRA"
controls = [c for c in panel_df["country"].unique() if c != TREATED]
years = sorted(panel_df["year"].unique())

# ATT(t) = avg(outcome_treated_t - outcome_treated_pre) - avg(outcome_control_t - outcome_control_pre)
pre_years = [y for y in years if y < 2023]
post_years = [y for y in years if y >= 2023]

def country_year(c, y):
    sub = panel_df[(panel_df["country"] == c) & (panel_df["year"] == y)]
    return float(sub["n_compat"].iloc[0]) if len(sub) > 0 else np.nan

bra_pre_avg = np.nanmean([country_year(TREATED, y) for y in pre_years])
ctrl_pre_avgs = {c: np.nanmean([country_year(c, y) for y in pre_years]) for c in controls}
print(f"  BRA pre-2023 avg: {bra_pre_avg:.3f}", flush=True)

# CS ATT for each post-period year
print(f"  Year |  BRA  | ctrl-mean |  ATT", flush=True)
att_per_year = {}
for y in post_years:
    bra_y = country_year(TREATED, y)
    if np.isnan(bra_y): continue
    ctrl_devs = []
    for c in controls:
        cy = country_year(c, y)
        if not np.isnan(cy) and not np.isnan(ctrl_pre_avgs[c]):
            ctrl_devs.append(cy - ctrl_pre_avgs[c])
    ctrl_dev_mean = float(np.mean(ctrl_devs)) if ctrl_devs else np.nan
    bra_dev = bra_y - bra_pre_avg
    att = bra_dev - ctrl_dev_mean
    att_per_year[int(y)] = {"bra_dev": float(bra_dev), "ctrl_dev": ctrl_dev_mean, "att": float(att)}
    print(f"  {y} | {bra_y:.3f} | dev_ctrl={ctrl_dev_mean:+.3f} | ATT={att:+.3f}", flush=True)
results["CS_DiD_bra_panel"] = {
    "treated": TREATED,
    "controls": controls,
    "pre_years": pre_years,
    "post_years": post_years,
    "bra_pre_avg": float(bra_pre_avg),
    "att_per_year": att_per_year,
    "intervention_date": "2023-10-11 (Pereira head-judge transition)",
}

# Save
out = ROOT / "outputs" / "tier5_results.json"
with open(out, "w") as f:
    json.dump(results, f, indent=2, default=str)
print(f"\n=> Wrote {out}", flush=True)
print("\n" + "="*72 + "\nTIER 5 DONE\n" + "="*72, flush=True)
