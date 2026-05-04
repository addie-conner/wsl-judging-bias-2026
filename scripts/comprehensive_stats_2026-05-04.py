"""Comprehensive statistical battery on the full 60,834-row / 301,478-judge-score WSL corpus.

Wires in:
  - Chorus prediction_stack.brier_index for Brier decomposition framework
  - Chorus prediction_stack.blf_ensemble for ensemble of bias-detection models
  - Chorus prediction_stack.extremizing for calibrated extremizer
  - Nielsen-style two-sided contribution matrix (judge-nationality x surfer-country)

Methods covered (all local, zero LLM tokens):
  1. Median polish + RF + doubles/triples/quads (rerun, fixed)
  2. ANOVA — one-way / two-way / three-way / mixed-effects on wave_score
  3. Contribution analysis — variance decomposition (Type II/III SS) + Shapley R^2
  4. Multivariate — PCA, Factor Analysis, Canonical Correlation, MANOVA
  5. Robust regression — Huber + Theil-Sen as sensitivity to OLS
  6. Bootstrap confidence on top-2 findings (T2 rep prior + T4 AUS bloc)
  7. Nielsen-style two-sided contribution matrix
  8. Chorus blf_ensemble + brier_index plumbing report

Output: outputs/comprehensive_stats_2026-05-04.json + console table.
"""
import sys
import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
warnings.filterwarnings("ignore")

ROOT = Path("/Users/addieconner/chorus/wsl")
CHORUS = Path("/Users/addieconner/chorus")
sys.path.insert(0, str(CHORUS))

HEATS = pd.read_parquet(ROOT / "data" / "heats.parquet")
JUDGES = pd.read_parquet(ROOT / "data" / "judges.parquet")
print(f"heats={len(HEATS):,} | judges={len(JUDGES):,}")

results: dict = {}
df = HEATS[HEATS["wave_score"] > 0].copy()
df["surfer_id"] = df["surfer_athlete_id"].fillna(df["surfer_name_full"]).astype(str)

# Build surfer_id -> name map for printing (FIX for prior lambda-in-set_index bug)
NAME_MAP = (
    HEATS.dropna(subset=["surfer_name_full"])
    .assign(sid=lambda d: d["surfer_athlete_id"].fillna(d["surfer_name_full"]).astype(str))
    .drop_duplicates("sid")
    .set_index("sid")["surfer_name_full"]
    .to_dict()
)

def name_of(sid):
    return NAME_MAP.get(str(sid), str(sid))

# ============================================================
# 1. MEDIAN POLISH (Tukey)  — already validated; recap for completeness
# ============================================================
print("\n" + "=" * 72)
print("1. MEDIAN POLISH (Tukey) — surfer x event")
print("=" * 72)

pivot = df.pivot_table(values="wave_score", index="surfer_id", columns="event_code", aggfunc="median")
pivot = pivot.dropna(thresh=5, axis=0).dropna(thresh=5, axis=1)
print(f"  Pivot (filtered ≥5 non-NA each axis): {pivot.shape}")


def median_polish(M, max_iter=20, tol=1e-4):
    Z = np.array(M, dtype=float).copy()
    grand = 0.0
    rE = np.zeros(Z.shape[0])
    cE = np.zeros(Z.shape[1])
    for _ in range(max_iter):
        rm = np.nanmedian(Z, axis=1); rm[np.isnan(rm)] = 0
        Z -= rm[:, None]; rE += rm
        cm = np.nanmedian(Z, axis=0); cm[np.isnan(cm)] = 0
        Z -= cm[None, :]; cE += cm
        gm_r = np.nanmedian(rE)
        if not np.isnan(gm_r): rE -= gm_r; grand += gm_r
        gm_c = np.nanmedian(cE)
        if not np.isnan(gm_c): cE -= gm_c; grand += gm_c
        if np.nanmax(np.abs(rm)) < tol and np.nanmax(np.abs(cm)) < tol:
            break
    return grand, rE, cE, Z


grand, surfer_eff, event_eff, residuals = median_polish(pivot.values)
sdf = pd.DataFrame({"sid": pivot.index, "effect": surfer_eff}).sort_values("effect", ascending=False)
sdf["surfer"] = sdf["sid"].map(name_of)
print(f"  Grand median: {grand:.3f}")
print("  Top-5 OVER-scored (most positive surfer effect):")
for _, r in sdf.head(5).iterrows():
    print(f"    {r['surfer']}: {r['effect']:+.4f}")
print("  Bot-5 UNDER-scored:")
for _, r in sdf.tail(5).iterrows():
    print(f"    {r['surfer']}: {r['effect']:+.4f}")

results["median_polish"] = {
    "grand": float(grand),
    "top_5_over": sdf.head(5).to_dict(orient="records"),
    "bot_5_under": sdf.tail(5).to_dict(orient="records"),
    "n_surfers": len(sdf),
    "n_events": pivot.shape[1],
}

# ============================================================
# 2. RANDOM FOREST  — feature importance (already converged; re-run for completeness)
# ============================================================
print("\n" + "=" * 72)
print("2. RANDOM FOREST — feature importance for wave_score")
print("=" * 72)

from sklearn.ensemble import RandomForestRegressor

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
X = Xf.values
print(f"  n={len(y):,}, n_features={X.shape[1]}")

rf = RandomForestRegressor(n_estimators=100, max_depth=10, n_jobs=4, random_state=42)
rf.fit(X, y)
print(f"  R² (in-sample): {rf.score(X, y):.4f}")
imp = pd.DataFrame({"feature": Xf.columns, "importance": rf.feature_importances_}).sort_values(
    "importance", ascending=False
)
print("  Top-10 features by importance:")
for _, r in imp.head(10).iterrows():
    print(f"    {r['feature']}: {r['importance']:.4f}")
results["random_forest"] = {"r2": float(rf.score(X, y)), "top10": imp.head(10).to_dict(orient="records")}

# ============================================================
# 3. INTERACTIONS — doubles / triples / quads (cluster-robust)
# ============================================================
print("\n" + "=" * 72)
print("3. INTERACTIONS — singles / doubles / triples / quads")
print("=" * 72)

import statsmodels.api as sm
from statsmodels.regression.linear_model import OLS

groups = rf_df["surfer_id"].values

doubles_to_test = [
    ("rank", "year"), ("rank", "is_male"), ("rank", "home_match"),
    ("home_match", "year"), ("is_male", "home_match"),
    ("heat_number", "rank"), ("wave_position_in_heat", "rank"),
]
doubles = {}
for a_, b_ in doubles_to_test:
    a, b = Xf[a_].values, Xf[b_].values
    Xs = sm.add_constant(np.column_stack([a, b, a * b]))
    res = OLS(y, Xs).fit(cov_type="cluster", cov_kwds={"groups": groups})
    doubles[f"{a_}_x_{b_}"] = {"coef": float(res.params[3]), "p": float(res.pvalues[3])}
    print(f"  {a_} × {b_}: coef={res.params[3]:+.5f}, p={res.pvalues[3]:.4g}")
results["doubles"] = doubles

triples_to_test = [
    ("rank", "is_male", "home_match"),
    ("rank", "year", "home_match"),
    ("home_match", "is_male", "year"),
]
triples = {}
for a_, b_, c_ in triples_to_test:
    a, b, c = Xf[a_].values, Xf[b_].values, Xf[c_].values
    Xs = sm.add_constant(np.column_stack([a, b, c, a*b, a*c, b*c, a*b*c]))
    res = OLS(y, Xs).fit(cov_type="cluster", cov_kwds={"groups": groups})
    triples[f"{a_}_x_{b_}_x_{c_}"] = {"coef": float(res.params[7]), "p": float(res.pvalues[7])}
    print(f"  {a_} × {b_} × {c_}: 3-way coef={res.params[7]:+.5f}, p={res.pvalues[7]:.4g}")
results["triples"] = triples

quads_to_test = [("rank", "is_male", "home_match", "year")]
quads = {}
for a_, b_, c_, d_ in quads_to_test:
    a, b, c, d = Xf[a_].values, Xf[b_].values, Xf[c_].values, Xf[d_].values
    Xs = sm.add_constant(np.column_stack([a, b, c, d, a*b*c*d]))
    res = OLS(y, Xs).fit(cov_type="cluster", cov_kwds={"groups": groups})
    quads[f"{a_}_x_{b_}_x_{c_}_x_{d_}"] = {"coef": float(res.params[5]), "p": float(res.pvalues[5])}
    print(f"  {a_}×{b_}×{c_}×{d_}: 4-way coef={res.params[5]:+.5e}, p={res.pvalues[5]:.4g}")
print("  HONEST NOTE: 4-way interactions usually noise per Cogo/ROAS prior.")
results["quads"] = quads

# ============================================================
# 4. ANOVA — one-way / two-way / three-way + mixed-effects
# ============================================================
print("\n" + "=" * 72)
print("4. ANOVA — one-way / two-way / three-way / mixed-effects")
print("=" * 72)
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

# Subsample to 30K rows for tractability
adf = df.dropna(subset=["surfer_country", "event_country", "year"]).copy()
adf["sc"] = adf["surfer_country"].astype(str)
adf["ec"] = adf["event_country"].astype(str)
adf["yr"] = adf["year"].astype(str)
adf["gender_str"] = adf["gender"].astype(str)
adf = adf.sample(min(30000, len(adf)), random_state=42)

print(f"  ANOVA n={len(adf):,}")

# One-way: surfer_country
m1 = ols("wave_score ~ C(sc)", data=adf).fit()
a1 = anova_lm(m1, typ=2)
print("  One-way (C(sc)) — F, p, η²:")
ss_total = a1["sum_sq"].sum()
for idx, row in a1.iterrows():
    eta2 = row["sum_sq"] / ss_total
    print(f"    {idx}: F={row.get('F', np.nan):.3f}, p={row.get('PR(>F)', np.nan):.4g}, η²={eta2:.4f}")
oneway = {"sc_eta2": float(a1.loc["C(sc)", "sum_sq"] / ss_total),
          "sc_F": float(a1.loc["C(sc)", "F"]),
          "sc_p": float(a1.loc["C(sc)", "PR(>F)"])}

# Two-way: surfer_country × event_country
m2 = ols("wave_score ~ C(sc) + C(ec) + C(sc):C(ec)", data=adf).fit()
a2 = anova_lm(m2, typ=2)
ss_total = a2["sum_sq"].sum()
twoway = {}
print("  Two-way (sc × ec) — F, p, η²:")
for idx, row in a2.iterrows():
    eta2 = row["sum_sq"] / ss_total
    print(f"    {idx}: F={row.get('F', np.nan):.3f}, p={row.get('PR(>F)', np.nan):.4g}, η²={eta2:.4f}")
    twoway[idx] = {"F": float(row.get("F", np.nan)), "p": float(row.get("PR(>F)", np.nan)), "eta2": float(eta2)}

# Three-way: sc × ec × gender
m3 = ols("wave_score ~ C(sc) + C(ec) + C(gender_str) + C(sc):C(ec) + C(sc):C(gender_str) + C(ec):C(gender_str) + C(sc):C(ec):C(gender_str)", data=adf).fit()
a3 = anova_lm(m3, typ=2)
ss_total = a3["sum_sq"].sum()
threeway = {}
print("  Three-way (sc × ec × gender) — F, p, η²:")
for idx, row in a3.iterrows():
    eta2 = row["sum_sq"] / ss_total
    print(f"    {idx}: F={row.get('F', np.nan):.3f}, p={row.get('PR(>F)', np.nan):.4g}, η²={eta2:.4f}")
    threeway[idx] = {"F": float(row.get("F", np.nan)), "p": float(row.get("PR(>F)", np.nan)), "eta2": float(eta2)}

results["ANOVA"] = {"one_way_sc": oneway, "two_way": twoway, "three_way": threeway}

# Mixed-effects ANOVA: surfer as random
from statsmodels.regression.mixed_linear_model import MixedLM
ts = adf.copy()
print(f"  Mixed-effects (random intercept = surfer_id), n={len(ts):,}")
try:
    mlm = MixedLM(
        endog=ts["wave_score"].values,
        exog=sm.add_constant(pd.get_dummies(ts["yr"], drop_first=True).values.astype(float)),
        groups=ts["surfer_id"].values,
    ).fit(method="lbfgs", maxiter=300)
    cov_re = float(np.asarray(mlm.cov_re)[0, 0])
    icc = cov_re / (cov_re + mlm.scale)
    print(f"    ICC (surfer): {icc:.4f}, scale={mlm.scale:.4f}, cov_re={cov_re:.4f}")
    results["ANOVA"]["MLM_year_surfer_RE"] = {"icc_surfer": float(icc), "cov_re": cov_re, "scale": float(mlm.scale)}
except Exception as e:
    print(f"    MLM failed: {e}")
    results["ANOVA"]["MLM_year_surfer_RE"] = {"error": str(e)}

# ============================================================
# 5. CONTRIBUTION ANALYSIS — Shapley R² + LMG
# ============================================================
print("\n" + "=" * 72)
print("5. CONTRIBUTION ANALYSIS — Shapley R² (LMG-style)")
print("=" * 72)

# LMG decomposition: average R² contribution across all feature orderings
# For tractability, group features into 5 buckets and compute exact Shapley over buckets
from itertools import permutations
from sklearn.linear_model import LinearRegression

groups_def = {
    "rank": ["rank"],
    "tempo": ["heat_number", "wave_index_for_surfer", "wave_position_in_heat"],
    "year": ["year"],
    "gender": ["is_male"],
    "geo": ["home_match"] + [c for c in Xf.columns if c.startswith("sc_") or c.startswith("ec_")],
}
print(f"  Feature buckets: {list(groups_def.keys())}")

def r2_of(cols):
    if not cols:
        return 0.0
    Xsub = Xf[cols].values
    return LinearRegression().fit(Xsub, y).score(Xsub, y)

# Exact Shapley over 5 buckets — 5! = 120 permutations
buckets = list(groups_def.keys())
contrib = {b: 0.0 for b in buckets}
n_perm = 0
for perm in permutations(buckets):
    cum = []
    prev = 0.0
    for b in perm:
        cum += groups_def[b]
        cur = r2_of(cum)
        contrib[b] += (cur - prev)
        prev = cur
    n_perm += 1
shapley = {b: contrib[b] / n_perm for b in buckets}
total = sum(shapley.values())
print(f"  Total R² (linear, all buckets): {total:.5f}")
print("  Shapley R² contribution per bucket:")
for b, v in sorted(shapley.items(), key=lambda x: -x[1]):
    pct = (v / total * 100) if total > 0 else 0
    print(f"    {b}: ΔR²={v:.5f}  ({pct:.1f}% of explained)")
results["shapley_r2"] = {"total_r2": float(total), "per_bucket": {k: float(v) for k, v in shapley.items()}}

# ============================================================
# 6. MULTIVARIATE — PCA / Factor Analysis / CCA / MANOVA
# ============================================================
print("\n" + "=" * 72)
print("6. MULTIVARIATE — PCA / Factor Analysis / CCA / MANOVA")
print("=" * 72)

# Heat-level mechanism vector (re-derived)
heat_mech = df.groupby(["event_code", "heat_id"]).agg(
    heat_mean=("wave_score", "mean"), heat_std=("wave_score", "std"), heat_n=("wave_score", "count"),
).reset_index()

def round_rate(g):
    last = (g["wave_score"] * 100 % 100).astype(int)
    return ((last == 0) | (last == 25) | (last == 50) | (last == 75)).mean()
m1 = df.groupby(["event_code", "heat_id"]).apply(round_rate).reset_index()
m1.columns = ["event_code", "heat_id", "M1_round"]

def rank_gap(g):
    sub = g.dropna(subset=["surfer_world_rank_at_event_start"]).sort_values("surfer_world_rank_at_event_start")
    if len(sub) < 2: return np.nan
    return sub.iloc[0]["wave_score"] - sub.iloc[-1]["wave_score"]
m2 = df.groupby(["event_code", "heat_id"]).apply(rank_gap).reset_index()
m2.columns = ["event_code", "heat_id", "M2_rank_gap"]

def home_match_rate(g):
    return (g["surfer_country"] == g["event_country"]).mean()
m3 = df.groupby(["event_code", "heat_id"]).apply(home_match_rate).reset_index()
m3.columns = ["event_code", "heat_id", "M3_home_match"]

mech = heat_mech.merge(m1, on=["event_code", "heat_id"]).merge(m2, on=["event_code", "heat_id"]).merge(m3, on=["event_code", "heat_id"])
mech_cols = ["M1_round", "M2_rank_gap", "M3_home_match", "heat_std", "heat_mean"]
mech_clean = mech[mech_cols].dropna()
print(f"  Heats with all mechanisms: {len(mech_clean):,}")

# PCA
from sklearn.decomposition import PCA, FactorAnalysis
from sklearn.preprocessing import StandardScaler
Xs = StandardScaler().fit_transform(mech_clean.values)
pca = PCA(n_components=len(mech_cols)).fit(Xs)
print("  PCA explained-variance ratio:", np.round(pca.explained_variance_ratio_, 3))
print("  PC1 loadings:")
for col, load in zip(mech_cols, pca.components_[0]):
    print(f"    {col}: {load:+.3f}")

# Factor analysis (latent factor count = 2)
fa = FactorAnalysis(n_components=2, random_state=42).fit(Xs)
print("  FA loadings (2 factors):")
for i, col in enumerate(mech_cols):
    print(f"    {col}: F1={fa.components_[0, i]:+.3f}, F2={fa.components_[1, i]:+.3f}")

results["multivariate"] = {
    "pca_explained_var": pca.explained_variance_ratio_.tolist(),
    "pc1_loadings": dict(zip(mech_cols, pca.components_[0].tolist())),
    "fa_loadings": {col: {"F1": float(fa.components_[0, i]), "F2": float(fa.components_[1, i])}
                    for i, col in enumerate(mech_cols)},
}

# CCA — bias mechanisms (X) vs heat-quality outcomes (Y)
from sklearn.cross_decomposition import CCA
X_bias = mech_clean[["M1_round", "M2_rank_gap", "M3_home_match"]].values
Y_qual = mech_clean[["heat_std", "heat_mean"]].values
cca = CCA(n_components=2).fit(X_bias, Y_qual)
Xc, Yc = cca.transform(X_bias, Y_qual)
canon_corr_1 = float(np.corrcoef(Xc[:, 0], Yc[:, 0])[0, 1])
canon_corr_2 = float(np.corrcoef(Xc[:, 1], Yc[:, 1])[0, 1])
print(f"  CCA canonical-corr 1: {canon_corr_1:+.4f}")
print(f"  CCA canonical-corr 2: {canon_corr_2:+.4f}")
results["multivariate"]["cca"] = {"r1": canon_corr_1, "r2": canon_corr_2}

# MANOVA — bias-mechanism vector ~ surfer_country (top 5)
from statsmodels.multivariate.manova import MANOVA
mn = df.dropna(subset=["surfer_country", "wave_score"]).copy()
top5_sc = mn["surfer_country"].value_counts().head(5).index.tolist()
mn = mn[mn["surfer_country"].isin(top5_sc)]
heat_y = mn.groupby(["event_code", "heat_id", "surfer_country"]).agg(
    mean_=("wave_score", "mean"), std_=("wave_score", "std"),
).reset_index().dropna()
print(f"  MANOVA n={len(heat_y):,}, k={heat_y['surfer_country'].nunique()}")
try:
    mv = MANOVA.from_formula("mean_ + std_ ~ C(surfer_country)", data=heat_y).mv_test()
    wilks = mv.results["C(surfer_country)"]["stat"].loc["Wilks' lambda"]
    print(f"  MANOVA Wilks' λ = {wilks['Value']:.4f}, F = {wilks['F Value']:.3f}, p = {wilks['Pr > F']:.4g}")
    results["multivariate"]["manova_country"] = {
        "wilks_lambda": float(wilks["Value"]), "F": float(wilks["F Value"]), "p": float(wilks["Pr > F"]),
    }
except Exception as e:
    print(f"  MANOVA failed: {e}")
    results["multivariate"]["manova_country"] = {"error": str(e)}

# ============================================================
# 7. ROBUST REGRESSION — Huber + Theil-Sen sensitivity
# ============================================================
print("\n" + "=" * 72)
print("7. ROBUST REGRESSION — Huber / Theil-Sen sensitivity for T2 prior")
print("=" * 72)

t2 = df.dropna(subset=["surfer_world_rank_at_event_start"]).copy()
t2["rank"] = t2["surfer_world_rank_at_event_start"].astype(float)
t2["heat_key"] = t2["event_code"].astype(str) + "_" + t2["heat_id"].astype(str)

def within_demean(s, g):
    return s - s.groupby(g).transform("mean")

y2 = within_demean(t2["wave_score"], t2["heat_key"]).values
x2 = within_demean(t2["rank"], t2["heat_key"]).values

ols_t2 = OLS(y2, sm.add_constant(x2)).fit(cov_type="cluster", cov_kwds={"groups": t2["surfer_id"].values})
print(f"  OLS heat-FE: coef={ols_t2.params[1]:+.5f}, p={ols_t2.pvalues[1]:.4g}")

from sklearn.linear_model import HuberRegressor
sample_idx = np.random.RandomState(42).choice(len(y2), min(20000, len(y2)), replace=False)
hub = HuberRegressor(epsilon=1.35).fit(x2[sample_idx].reshape(-1, 1), y2[sample_idx])
print(f"  Huber (eps=1.35, n={len(sample_idx):,}): coef={hub.coef_[0]:+.5f}")

from sklearn.linear_model import TheilSenRegressor
ts_idx = np.random.RandomState(42).choice(len(y2), min(5000, len(y2)), replace=False)
tsr = TheilSenRegressor(random_state=42, max_subpopulation=1000).fit(x2[ts_idx].reshape(-1, 1), y2[ts_idx])
print(f"  Theil-Sen (n={len(ts_idx):,}): coef={tsr.coef_[0]:+.5f}")

results["robust_T2"] = {
    "ols_coef": float(ols_t2.params[1]), "ols_p": float(ols_t2.pvalues[1]),
    "huber_coef": float(hub.coef_[0]), "theilsen_coef": float(tsr.coef_[0]),
}
delta_huber = abs(hub.coef_[0] - ols_t2.params[1]) / abs(ols_t2.params[1])
print(f"  Robustness — Huber|OLS Δ = {delta_huber*100:.1f}%  ({'STABLE' if delta_huber < 0.30 else 'UNSTABLE'})")

# ============================================================
# 8. NIELSEN-style two-sided contribution matrix
#    judge-nationality x surfer-country -> mean-score deviation
# ============================================================
print("\n" + "=" * 72)
print("8. NIELSEN-style two-sided contribution matrix (judge-nat × surfer-country)")
print("=" * 72)

nat_cols = [c for c in JUDGES.columns if c.startswith("judge_") and "nationality" in c]
score_cols = [c for c in JUDGES.columns if c.startswith("judge_") and c.endswith("_score")]
ISO_NAME = {"AUS": "Australia", "USA": "United States", "BRA": "Brazil", "JPN": "Japan",
            "FRA": "France", "PRT": "Portugal", "ESP": "Spain", "ZAF": "South Africa"}
sn_map = (HEATS.dropna(subset=["surfer_country", "surfer_name_full"])
          .drop_duplicates("surfer_name_full")
          .set_index("surfer_name_full")["surfer_country"].to_dict())

J = JUDGES.dropna(subset=nat_cols).copy()
J["surfer_country"] = J["surfer_name"].map(sn_map)
J = J.dropna(subset=["surfer_country"])

# For top-5 ISO codes, build per-(judge_nat, surfer_nat) score deviation
top_isos = ["AUS", "USA", "BRA", "ZAF", "FRA"]
# Long-form: each row = (wave, judge_idx, judge_nat, judge_score, surfer_country)
rows = []
for jc, sc in zip(nat_cols, score_cols):
    sub = J[[jc, sc, "surfer_country"]].rename(columns={jc: "jnat", sc: "jscore"})
    sub = sub.dropna(subset=["jnat", "jscore", "surfer_country"])
    rows.append(sub)
LONG = pd.concat(rows, ignore_index=True)
print(f"  Long-form judge-rows: {len(LONG):,}")

# Map judge nationality (full names) -> ISO
NAME_TO_ISO = {v: k for k, v in ISO_NAME.items()}
LONG["jnat_iso"] = LONG["jnat"].map(NAME_TO_ISO)
LONG = LONG[LONG["jnat_iso"].isin(top_isos) & LONG["surfer_country"].isin(top_isos)]
print(f"  After top-5 × top-5 filter: {len(LONG):,}")

# Two-sided matrix: mean(judge_score) deviation from grand mean
gm_score = LONG["jscore"].mean()
matrix = LONG.groupby(["jnat_iso", "surfer_country"])["jscore"].agg(["mean", "count"]).reset_index()
matrix["dev"] = matrix["mean"] - gm_score
piv = matrix.pivot(index="jnat_iso", columns="surfer_country", values="dev")
piv_n = matrix.pivot(index="jnat_iso", columns="surfer_country", values="count")
print("  Mean-score deviation (rows = judge nat, cols = surfer nat):")
print(piv.round(3).to_string())
print("  Cell counts:")
print(piv_n.fillna(0).astype(int).to_string())
print(f"  Diagonal (compatriot) cells:")
diag_devs = []
for iso in top_isos:
    if iso in piv.index and iso in piv.columns and not pd.isna(piv.loc[iso, iso]):
        dev = piv.loc[iso, iso]
        n = int(piv_n.loc[iso, iso])
        diag_devs.append((iso, dev, n))
        print(f"    {iso}|{iso}: dev={dev:+.4f}, n={n}")
results["nielsen_contribution_matrix"] = {
    "grand_mean": float(gm_score),
    "matrix_dev": piv.fillna(0.0).to_dict(),
    "matrix_n": piv_n.fillna(0).astype(int).to_dict(),
    "diagonal_compatriot": [{"iso": d[0], "dev": float(d[1]), "n": int(d[2])} for d in diag_devs],
}

# ============================================================
# 9. CHORUS prediction-stack plumbing report
# ============================================================
print("\n" + "=" * 72)
print("9. CHORUS prediction_stack — Brier + ensemble plumbing")
print("=" * 72)
try:
    from prediction_stack.brier_index import brier, score, ScoredForecast  # type: ignore
    from prediction_stack.blf_ensemble import ensemble, BLFConfig  # type: ignore
    from prediction_stack.extremizing import extremize  # type: ignore

    pred_path = CHORUS / "prediction_stack" / "wsl_predictions.jsonl"
    n_pred = sum(1 for _ in open(pred_path)) if pred_path.exists() else 0
    n_resolved = 0
    if pred_path.exists():
        for line in open(pred_path):
            r = json.loads(line)
            if r.get("resolved"):
                n_resolved += 1
    print(f"  WSL SHA-locked predictions: {n_pred} (resolved: {n_resolved})")

    # Demo extremizer on the 49 stored P(disputed) values
    if pred_path.exists():
        probs = [json.loads(line)["predicted_prob"] for line in open(pred_path)]
        ex_probs = [extremize(p, a=1.5) for p in probs]
        print(f"  Mean p(disputed): {np.mean(probs):.3f}, after extremize(a=1.5): {np.mean(ex_probs):.3f}")
        results["chorus_predictions"] = {
            "n_predictions": n_pred, "n_resolved": n_resolved,
            "mean_p_disputed": float(np.mean(probs)),
            "mean_p_extremized_a1p5": float(np.mean(ex_probs)),
        }

    # Demo ensemble: stack 3 toy bias-detection probs per heat (round-bias / rank-gap / home-match)
    # Using normalized M1/M2/M3 as if they were 3 forecasters' probabilities of "this heat is biased"
    heat_p1 = mech_clean["M1_round"].clip(0, 1).values
    heat_p2 = (mech_clean["M2_rank_gap"].abs() / mech_clean["M2_rank_gap"].abs().max()).clip(0, 1).values
    heat_p3 = mech_clean["M3_home_match"].clip(0, 1).values
    cfg = BLFConfig()
    forecast_arrays = [heat_p1, heat_p2, heat_p3]
    ens = []
    for i in range(len(heat_p1)):
        triple = [arr[i] for arr in forecast_arrays]
        triple = [max(min(p, 1 - 1e-6), 1e-6) for p in triple]
        ens.append(ensemble(triple, cfg))
    print(f"  3-forecaster blf_ensemble: mean p_ens={np.mean(ens):.4f}, n={len(ens):,}")
    results["chorus_predictions"]["ensemble_demo_mean_p"] = float(np.mean(ens))
except Exception as e:
    print(f"  Chorus plumbing skipped: {e}")
    results["chorus_predictions"] = {"error": str(e)}

# ============================================================
# 10. BOOTSTRAP CI on top-2 published findings
# ============================================================
print("\n" + "=" * 72)
print("10. BOOTSTRAP CI — T2 (rank prior) + T4 (AUS bloc)")
print("=" * 72)

rng = np.random.RandomState(42)
B = 1000

# T2 bootstrap of heat-FE coefficient on cluster-resampled surfers
sids = t2["surfer_id"].unique()
boots_t2 = []
for _ in range(B):
    sample_sids = rng.choice(sids, len(sids), replace=True)
    sample = t2[t2["surfer_id"].isin(sample_sids)]
    if len(sample) < 100:
        continue
    yy = within_demean(sample["wave_score"], sample["heat_key"]).values
    xx = within_demean(sample["rank"], sample["heat_key"]).values
    if np.var(xx) == 0:
        continue
    b, _ = np.polyfit(xx, yy, 1, full=False), None
    boots_t2.append(b[0])
boots_t2 = np.array(boots_t2)
print(f"  T2 bootstrap: median={np.median(boots_t2):+.5f}, CI95=[{np.percentile(boots_t2, 2.5):+.5f}, {np.percentile(boots_t2, 97.5):+.5f}]")

# T4 AUS bloc bootstrap (heat-clustered)
df_aus = df.copy()
df_aus["aus_match"] = ((df_aus["surfer_country"] == "AUS") & (df_aus["event_country"] == "AUS")).astype(int)
heat_keys = df_aus.groupby(["event_code", "heat_id"]).ngroup().values
unique_heats = np.unique(heat_keys)
boots_t4 = []
for _ in range(B):
    sample_h = rng.choice(unique_heats, len(unique_heats), replace=True)
    mask = np.isin(heat_keys, sample_h)
    sample = df_aus[mask]
    if sample["aus_match"].sum() == 0:
        continue
    coef = (sample[sample["aus_match"] == 1]["wave_score"].mean()
            - sample[sample["aus_match"] == 0]["wave_score"].mean())
    boots_t4.append(coef)
boots_t4 = np.array(boots_t4)
print(f"  T4 AUS bloc bootstrap: median={np.median(boots_t4):+.5f}, CI95=[{np.percentile(boots_t4, 2.5):+.5f}, {np.percentile(boots_t4, 97.5):+.5f}]")

results["bootstrap_top2"] = {
    "T2_rank_prior": {"median": float(np.median(boots_t2)),
                       "ci_lo": float(np.percentile(boots_t2, 2.5)),
                       "ci_hi": float(np.percentile(boots_t2, 97.5)),
                       "n_boot": int(len(boots_t2))},
    "T4_aus_bloc": {"median": float(np.median(boots_t4)),
                     "ci_lo": float(np.percentile(boots_t4, 2.5)),
                     "ci_hi": float(np.percentile(boots_t4, 97.5)),
                     "n_boot": int(len(boots_t4))},
}

# ============================================================
# Save
# ============================================================
out = ROOT / "outputs" / "comprehensive_stats_2026-05-04.json"
out.parent.mkdir(parents=True, exist_ok=True)
with open(out, "w") as f:
    json.dump(results, f, indent=2, default=str)
print(f"\n=> Wrote {out}")

# Other applicable math (advisory list — not a bug, intentional summary)
print("\n" + "=" * 72)
print("OTHER APPLICABLE MATH (not run; ranked by ROI for this paper)")
print("=" * 72)
advisory = [
    ("Hierarchical Bayes (PyMC)",  "Pool surfer/event REs; recover bias-amplitude posteriors with full uncertainty. HIGH ROI."),
    ("Change-point detection",     "Detect 2018→2026 structural breaks in panel-composition policy (BIC + ruptures lib). HIGH ROI."),
    ("Conformal prediction",       "Distribution-free bands on next-event disputed-prob; tightens 49 SHA-locked priors. HIGH ROI."),
    ("Latent class analysis",      "Classify surfers into bias-treatment classes (stars / mid / outsiders) without prior. MED."),
    ("Copula analysis",            "Quantify tail dependence between rank and score (Spearman misses tail). MED."),
    ("Spectral / FFT",             "Detect periodic round-number patterns across heats / event days. MED."),
    ("Kernel methods (RBF SVR)",   "Non-parametric bias surface vs OLS; sensitivity. LOW (RF already covers)."),
    ("Structural equation model",  "Path: panel-comp → score → seeding → next-panel. LOW unless we ship a causal-graph figure."),
    ("Quantile regression forest", "Bias amplitude across the score distribution (already preview QuantReg). MED."),
    ("Survival analysis",          "Time-to-comeback narrative onset post-low-rank-event. LOW (already explored)."),
]
for name, ev in advisory:
    print(f"  - {name:32s} {ev}")
results["other_applicable_math_advisory"] = [{"method": n, "rationale": e} for n, e in advisory]
with open(out, "w") as f:
    json.dump(results, f, indent=2, default=str)

print("\n" + "=" * 72)
print("DONE")
print("=" * 72)
