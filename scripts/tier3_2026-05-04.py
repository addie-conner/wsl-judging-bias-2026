"""TIER 3 — Bayesian Model Averaging, Conformal prediction, Negative-control test, Stability selection.

All local. Zero LLM tokens. Writes outputs/tier3_results.json.
"""
import json, warnings
from pathlib import Path
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent.parent
HEATS = pd.read_parquet(ROOT / "data" / "heats.parquet")
JUDGES = pd.read_parquet(ROOT / "data" / "judges.parquet")
df = HEATS[HEATS["wave_score"] > 0].copy()
df["surfer_id"] = df["surfer_athlete_id"].fillna(df["surfer_name_full"]).astype(str)
results: dict = {}

def stamp(t): print(f"\n{'='*72}\n{t}\n{'='*72}", flush=True)

# ---------------------------------------------------------------
# T3.15 Bayesian Model Averaging across the spec battery for AUS bloc
# ---------------------------------------------------------------
stamp("T3.15 Bayesian Model Averaging — AUS bloc spec battery")
import statsmodels.api as sm

specs = {}
T = ((df["surfer_country"] == "AUS") & (df["event_country"] == "AUS")).astype(float).values
y = df["wave_score"].astype(float).values

# Spec 1: no controls
X1 = sm.add_constant(T)
r1 = sm.OLS(y, X1).fit()
specs["S1_no_controls"] = {"coef": float(r1.params[1]), "se": float(r1.bse[1]), "bic": float(r1.bic)}

# Spec 2: + rank
m2 = df.dropna(subset=["surfer_world_rank_at_event_start"]).copy()
T2_ = ((m2["surfer_country"] == "AUS") & (m2["event_country"] == "AUS")).astype(float).values
X2 = sm.add_constant(np.column_stack([T2_, m2["surfer_world_rank_at_event_start"].astype(float).values]))
r2 = sm.OLS(m2["wave_score"].astype(float).values, X2).fit()
specs["S2_rank"] = {"coef": float(r2.params[1]), "se": float(r2.bse[1]), "bic": float(r2.bic)}

# Spec 3: + rank + year
X3 = sm.add_constant(np.column_stack([T2_,
                                      m2["surfer_world_rank_at_event_start"].astype(float).values,
                                      m2["year"].astype(float).values]))
r3 = sm.OLS(m2["wave_score"].astype(float).values, X3).fit()
specs["S3_rank_year"] = {"coef": float(r3.params[1]), "se": float(r3.bse[1]), "bic": float(r3.bic)}

# Spec 4: + rank + year + gender
X4 = sm.add_constant(np.column_stack([T2_,
                                      m2["surfer_world_rank_at_event_start"].astype(float).values,
                                      m2["year"].astype(float).values,
                                      (m2["gender"] == "m").astype(float).values]))
r4 = sm.OLS(m2["wave_score"].astype(float).values, X4).fit()
specs["S4_rank_year_gender"] = {"coef": float(r4.params[1]), "se": float(r4.bse[1]), "bic": float(r4.bic)}

# Spec 5: + heat-FE demeaning
m2["heat_key"] = m2["event_code"].astype(str) + "_" + m2["heat_id"].astype(str)
def wd(s, g): return s - s.groupby(g).transform("mean")
yh = wd(m2["wave_score"], m2["heat_key"]).values
Th = wd(pd.Series(T2_, index=m2.index), m2["heat_key"]).values
X5 = sm.add_constant(Th)
r5 = sm.OLS(yh, X5).fit()
specs["S5_heatFE"] = {"coef": float(r5.params[1]), "se": float(r5.bse[1]), "bic": float(r5.bic)}

bic_min = min(s["bic"] for s in specs.values())
weights = {k: float(np.exp(-0.5 * (s["bic"] - bic_min))) for k, s in specs.items()}
w_sum = sum(weights.values())
weights = {k: v / w_sum for k, v in weights.items()}
bma_coef = sum(weights[k] * specs[k]["coef"] for k in specs)
bma_var = sum(weights[k] * (specs[k]["se"] ** 2 + (specs[k]["coef"] - bma_coef) ** 2) for k in specs)
bma_se = float(np.sqrt(bma_var))

print("  Spec | coef | se | BIC | weight", flush=True)
for k, s in specs.items():
    print(f"  {k}: coef={s['coef']:+.4f}, se={s['se']:.4f}, BIC={s['bic']:.1f}, w={weights[k]:.3f}", flush=True)
print(f"  BMA AUS-bloc estimate: {bma_coef:+.4f} ± {bma_se:.4f}", flush=True)
results["BMA_aus_bloc"] = {
    "specs": specs, "weights": weights,
    "bma_coef": float(bma_coef), "bma_se": bma_se,
}

# ---------------------------------------------------------------
# T3.16 Conformal prediction — distribution-free CI on disputed-prob
# ---------------------------------------------------------------
stamp("T3.16 Conformal prediction — split conformal on heat-mean prediction")
from sklearn.ensemble import RandomForestRegressor

heat_df = df.groupby(["event_code", "heat_id"]).agg(
    heat_mean=("wave_score", "mean"),
    rank_med=("surfer_world_rank_at_event_start", "median"),
    year=("year", "first"),
    n=("wave_score", "count"),
).reset_index().dropna()
heat_df["aus_evt"] = (heat_df["event_code"].str.contains("Austral|Margaret|Bells|Gold", case=False, na=False)).astype(int)

# Split: 60% train / 20% calibration / 20% test
rng = np.random.RandomState(42)
idx = rng.permutation(len(heat_df))
n_tr = int(0.6 * len(idx)); n_ca = int(0.2 * len(idx))
tr, ca, te = idx[:n_tr], idx[n_tr:n_tr+n_ca], idx[n_tr+n_ca:]
feat_cols = ["rank_med", "year", "n", "aus_evt"]
Xtr, ytr = heat_df.iloc[tr][feat_cols].values, heat_df.iloc[tr]["heat_mean"].values
Xca, yca = heat_df.iloc[ca][feat_cols].values, heat_df.iloc[ca]["heat_mean"].values
Xte, yte = heat_df.iloc[te][feat_cols].values, heat_df.iloc[te]["heat_mean"].values
mod = RandomForestRegressor(n_estimators=100, max_depth=6, random_state=42, n_jobs=4).fit(Xtr, ytr)
resid_ca = np.abs(yca - mod.predict(Xca))
alpha = 0.05
q = np.quantile(resid_ca, 1 - alpha)
y_pred_te = mod.predict(Xte)
covered = ((yte >= y_pred_te - q) & (yte <= y_pred_te + q)).mean()
print(f"  Split conformal half-width: ±{q:.3f} (target 95%)", flush=True)
print(f"  Empirical coverage on test: {covered*100:.2f}% (n_test={len(te)})", flush=True)
results["conformal_split"] = {
    "half_width_95": float(q), "empirical_coverage": float(covered),
    "n_train": int(n_tr), "n_cal": int(n_ca), "n_test": int(len(te)),
}

# ---------------------------------------------------------------
# T3.17 Negative-control outcome test
# ---------------------------------------------------------------
stamp("T3.17 Negative-control outcome test — pre-event proxies that judges can't see")
nc_results = {}

# NC1: surfer's birth year (judges shouldn't systematically bias by birth year)
sub = df.copy()
sub["birth_year_proxy"] = sub.groupby("surfer_id")["year"].transform("min")
T = ((sub["surfer_country"] == "AUS") & (sub["event_country"] == "AUS")).astype(float).values
X = sm.add_constant(T)
res = sm.OLS(sub["birth_year_proxy"].values, X).fit(cov_type="cluster", cov_kwds={"groups": sub["surfer_id"].values})
print(f"  NC1: AUS-bloc → birth-year-proxy: coef={res.params[1]:+.3f}, p={res.pvalues[1]:.4g}", flush=True)
nc_results["NC1_birth_year_proxy"] = {"coef": float(res.params[1]), "p": float(res.pvalues[1])}

# NC2: heat-number (administrative ordering, judges can't bias to)
sub2 = df.dropna(subset=["heat_number"]).copy()
T2 = ((sub2["surfer_country"] == "AUS") & (sub2["event_country"] == "AUS")).astype(float).values
res2 = sm.OLS(pd.to_numeric(sub2["heat_number"], errors="coerce").fillna(0).astype(float).values,
              sm.add_constant(T2)).fit(cov_type="cluster", cov_kwds={"groups": sub2["surfer_id"].values})
print(f"  NC2: AUS-bloc → heat-number: coef={res2.params[1]:+.3f}, p={res2.pvalues[1]:.4g}", flush=True)
nc_results["NC2_heat_number"] = {"coef": float(res2.params[1]), "p": float(res2.pvalues[1])}

# NC3: wave-index (which wave in heat order — judges can't pre-select)
sub3 = df.dropna(subset=["wave_index_for_surfer"]).copy()
T3 = ((sub3["surfer_country"] == "AUS") & (sub3["event_country"] == "AUS")).astype(float).values
res3 = sm.OLS(pd.to_numeric(sub3["wave_index_for_surfer"], errors="coerce").fillna(0).astype(float).values,
              sm.add_constant(T3)).fit(cov_type="cluster", cov_kwds={"groups": sub3["surfer_id"].values})
print(f"  NC3: AUS-bloc → wave-index: coef={res3.params[1]:+.3f}, p={res3.pvalues[1]:.4g}", flush=True)
nc_results["NC3_wave_index"] = {"coef": float(res3.params[1]), "p": float(res3.pvalues[1])}

n_pass = sum(1 for v in nc_results.values() if v["p"] > 0.05)
print(f"  NC verdict: {n_pass}/{len(nc_results)} negative controls non-significant (target = all)", flush=True)
results["negative_control"] = nc_results
results["negative_control_summary"] = {"n_pass": n_pass, "n_total": len(nc_results)}

# ---------------------------------------------------------------
# T3.18 Stability selection (Lasso bootstrap) on the 26-feature set
# ---------------------------------------------------------------
stamp("T3.18 Stability selection — bootstrap-Lasso feature stability")
from sklearn.linear_model import Lasso
from sklearn.preprocessing import StandardScaler

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
y_lasso = rf_df["wave_score"].astype(float).values
sc = StandardScaler()
Xs = sc.fit_transform(Xf.values)

B = 100
sel_count = np.zeros(Xs.shape[1])
rng = np.random.RandomState(42)
for _ in range(B):
    idx = rng.choice(len(y_lasso), int(0.7 * len(y_lasso)), replace=False)
    lasso = Lasso(alpha=0.05, max_iter=5000)
    lasso.fit(Xs[idx], y_lasso[idx])
    sel_count += (np.abs(lasso.coef_) > 1e-4).astype(int)
sel_freq = sel_count / B
stab_df = pd.DataFrame({"feature": Xf.columns, "sel_freq": sel_freq}).sort_values("sel_freq", ascending=False)
print(f"  Stability selection (B={B}, threshold 0.7):", flush=True)
print(f"  {'Feature':35s}  Sel-freq", flush=True)
for _, r in stab_df.iterrows():
    flag = " ★" if r["sel_freq"] >= 0.7 else ""
    print(f"  {r['feature']:35s}  {r['sel_freq']:.2f}{flag}", flush=True)
results["stability_selection"] = {
    "B": B, "alpha": 0.05,
    "selection_freq": stab_df.set_index("feature")["sel_freq"].to_dict(),
    "stable_features_at_0p7": stab_df[stab_df["sel_freq"] >= 0.7]["feature"].tolist(),
}

out = ROOT / "outputs" / "tier3_results.json"
out.parent.mkdir(parents=True, exist_ok=True)
with open(out, "w") as f:
    json.dump(results, f, indent=2, default=str)
print(f"\n=> Wrote {out}", flush=True)
print("\n" + "="*72 + "\nTIER 3 DONE\n" + "="*72, flush=True)
