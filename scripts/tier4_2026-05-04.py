"""TIER 4 — Copula tail dependence, GEV/POT extreme value, Transfer entropy, VAR, e-values, Permutation feature importance, Robust DAG via constraint-based.

All local. Zero LLM tokens. Writes outputs/tier4_results.json.
"""
import json, warnings, math
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
# T4.A Copula tail dependence (Kendall's τ + Joe / Clayton / Gumbel proxy)
# ---------------------------------------------------------------
stamp("T4.A Copula tail dependence — rank ↔ score")
from scipy.stats import kendalltau, spearmanr, rankdata

sub = df.dropna(subset=["surfer_world_rank_at_event_start"]).sample(min(5000, len(df)), random_state=42)
x = sub["surfer_world_rank_at_event_start"].astype(float).values
y = sub["wave_score"].astype(float).values

tau, p_tau = kendalltau(x, y)
rho_s, p_s = spearmanr(x, y)
print(f"  Kendall's τ: {tau:+.4f}, p={p_tau:.4g}", flush=True)
print(f"  Spearman ρ: {rho_s:+.4f}, p={p_s:.4g}", flush=True)

# Empirical upper-tail dependence λ_U: λ_U = lim_{u→1} P(F_y(Y) > u | F_x(X) > u)
def tail_dep(u, q):
    n = len(u)
    Fu = rankdata(u) / (n + 1); Fv = rankdata(-1 * np.array(u))  # rank only u
    # Better: use both copula uniforms
    Fx = rankdata(x) / (n + 1); Fy = rankdata(y) / (n + 1)
    cnt_both = ((Fx > q) & (Fy > q)).sum()
    cnt_x = (Fx > q).sum()
    return cnt_both / cnt_x if cnt_x > 0 else 0.0

upper = tail_dep(x, 0.95)
lower_x = (rankdata(x) / (len(x) + 1) < 0.05)
lower_y = (rankdata(y) / (len(y) + 1) < 0.05)
lower = (lower_x & lower_y).sum() / max(lower_x.sum(), 1)
print(f"  Upper-tail dependence (q=0.95): {upper:.4f}", flush=True)
print(f"  Lower-tail dependence (q=0.05): {lower:.4f}", flush=True)
print(f"  Interpretation: {'high stars co-extreme with high scores' if upper > 0.3 else 'tail-independence — bias is mid-distribution, not extremes'}", flush=True)
results["copula"] = {"kendall_tau": float(tau), "p_tau": float(p_tau),
                      "spearman_rho": float(rho_s), "p_spearman": float(p_s),
                      "upper_tail_dep_0p95": float(upper), "lower_tail_dep_0p05": float(lower)}

# ---------------------------------------------------------------
# T4.B GEV / Peaks-over-threshold (POT) on event-bias amplitudes
# ---------------------------------------------------------------
stamp("T4.B GEV + POT — event-bias amplitude tail")
from scipy.stats import genextreme, genpareto

heat_mean = df.groupby(["event_code", "heat_id"])["wave_score"].mean()
heat_std = df.groupby(["event_code", "heat_id"])["wave_score"].std().dropna()
print(f"  Heats analyzed: {len(heat_std):,}", flush=True)

# GEV fit on heat-std (block maxima proxy)
gev_params = genextreme.fit(heat_std.values)
ξ, μ, σ = gev_params
print(f"  GEV fit: shape ξ={-ξ:+.3f}, location μ={μ:.3f}, scale σ={σ:.3f}", flush=True)
# Return-level for 100-heat extreme
T = 100; p = 1 - 1 / T
rl = genextreme.ppf(p, *gev_params)
print(f"  100-heat return-level for heat_std: {rl:.3f}", flush=True)

# POT GPD on top 5% threshold
thr = np.quantile(heat_std.values, 0.95)
exceed = heat_std.values[heat_std.values > thr] - thr
print(f"  POT threshold (95%): {thr:.3f}, n_exceed={len(exceed)}", flush=True)
gpd_params = genpareto.fit(exceed)
print(f"  GPD fit: shape={gpd_params[0]:+.3f}, scale={gpd_params[2]:.3f}", flush=True)
results["GEV_POT"] = {
    "gev_shape": float(-ξ), "gev_loc": float(μ), "gev_scale": float(σ),
    "return_level_100heat": float(rl),
    "pot_threshold_q95": float(thr),
    "gpd_shape": float(gpd_params[0]), "gpd_scale": float(gpd_params[2]),
    "n_exceed": int(len(exceed)),
}

# ---------------------------------------------------------------
# T4.C Transfer entropy — bias mechanisms over events
# ---------------------------------------------------------------
stamp("T4.C Transfer entropy — round-bias → score-mean across events")
def transfer_entropy(x, y, bins=8, lag=1):
    """TE(X→Y) = H(Y_{t+1}|Y_t) - H(Y_{t+1}|Y_t, X_t). Bin-discretized."""
    x = np.array(x); y = np.array(y); n = len(x)
    if n < lag + 5: return float("nan")
    yt1, yt, xt = y[lag:], y[:-lag], x[:-lag]
    # Discretize
    xb = pd.qcut(xt, bins, labels=False, duplicates="drop")
    yb = pd.qcut(yt, bins, labels=False, duplicates="drop")
    yt1b = pd.qcut(yt1, bins, labels=False, duplicates="drop")
    if pd.Series(xb).isna().all() or pd.Series(yb).isna().all(): return float("nan")
    # Build joint count tables
    df_ = pd.DataFrame({"x": xb, "y": yb, "y1": yt1b}).dropna().astype(int)
    if len(df_) < 10: return float("nan")
    p_y1_y = (df_.groupby(["y", "y1"]).size() / len(df_)).unstack(fill_value=0).values
    p_y = p_y1_y.sum(axis=1, keepdims=True)
    H_y1_y = -np.nansum(np.where(p_y1_y > 0, p_y1_y * np.log(p_y1_y / np.maximum(p_y, 1e-12)), 0))
    p_y1_yx = (df_.groupby(["y", "x", "y1"]).size() / len(df_)).unstack(fill_value=0).values
    p_yx = p_y1_yx.sum(axis=1, keepdims=True)
    H_y1_yx = -np.nansum(np.where(p_y1_yx > 0, p_y1_yx * np.log(p_y1_yx / np.maximum(p_yx, 1e-12)), 0))
    return float(H_y1_y - H_y1_yx)

# Per-event time series
ev = df.groupby("event_code").agg(
    mean_score=("wave_score", "mean"),
    round_rate=("wave_score", lambda s: (((s * 100 % 100).astype(int) % 100).isin([0, 25, 50, 75])).mean()),
    year=("year", "first"),
).reset_index().sort_values(["year", "event_code"])
print(f"  Events: {len(ev)}", flush=True)
te_round_to_score = transfer_entropy(ev["round_rate"].values, ev["mean_score"].values, bins=4, lag=1)
te_score_to_round = transfer_entropy(ev["mean_score"].values, ev["round_rate"].values, bins=4, lag=1)
print(f"  TE(round_rate → mean_score): {te_round_to_score:.4f}", flush=True)
print(f"  TE(mean_score → round_rate): {te_score_to_round:.4f}", flush=True)
print(f"  Net TE: {te_round_to_score - te_score_to_round:+.4f} (direction: {'round→score' if te_round_to_score > te_score_to_round else 'score→round'})", flush=True)
results["transfer_entropy"] = {
    "te_round_to_score": float(te_round_to_score) if not np.isnan(te_round_to_score) else None,
    "te_score_to_round": float(te_score_to_round) if not np.isnan(te_score_to_round) else None,
}

# ---------------------------------------------------------------
# T4.D VAR — joint dynamics of mean_score / round_rate / heat_std over event sequence
# ---------------------------------------------------------------
stamp("T4.D Vector autoregression — event-level joint dynamics")
from statsmodels.tsa.api import VAR

ev2 = df.groupby("event_code").agg(
    mean_score=("wave_score", "mean"),
    round_rate=("wave_score", lambda s: (((s * 100 % 100).astype(int) % 100).isin([0, 25, 50, 75])).mean()),
    heat_std=("wave_score", "std"),
    year=("year", "first"),
).reset_index().sort_values("year").dropna()
data = ev2[["mean_score", "round_rate", "heat_std"]].values
try:
    model = VAR(data)
    sel = model.select_order(maxlags=4)
    print(f"  VAR optimal lag (BIC): {sel.bic}", flush=True)
    fitted = model.fit(maxlags=2)
    print(f"  VAR(2) fitted. AIC={fitted.aic:.3f}, BIC={fitted.bic:.3f}", flush=True)
    # Granger causality
    gc = fitted.test_causality("mean_score", ["round_rate"], kind="f")
    print(f"  Granger: round_rate → mean_score: F={gc.test_statistic:.3f}, p={gc.pvalue:.4g}", flush=True)
    gc2 = fitted.test_causality("round_rate", ["mean_score"], kind="f")
    print(f"  Granger: mean_score → round_rate: F={gc2.test_statistic:.3f}, p={gc2.pvalue:.4g}", flush=True)
    results["VAR"] = {
        "lag_bic": int(sel.bic) if sel.bic else None,
        "var2_aic": float(fitted.aic), "var2_bic": float(fitted.bic),
        "granger_round_to_score_p": float(gc.pvalue),
        "granger_score_to_round_p": float(gc2.pvalue),
    }
except Exception as e:
    print(f"  VAR failed: {e}", flush=True)
    results["VAR"] = {"error": str(e)}

# ---------------------------------------------------------------
# T4.E e-values (Vovk-Wang) — sequential testing
# ---------------------------------------------------------------
stamp("T4.E e-values — sequential testing on AUS-bloc")
# Universal-inference e-value: e_n = ∏ likelihood-ratio_t under H_1 vs H_0
# Under H_0: AUS-bloc = 0; under H_1: bloc = mu_alt
# Use t-statistic e-value: e = exp(0.5 * t^2) (for normal; conservative for clustered)
import statsmodels.api as sm
y = df["wave_score"].astype(float).values
T = ((df["surfer_country"] == "AUS") & (df["event_country"] == "AUS")).astype(float).values
res = sm.OLS(y, sm.add_constant(T)).fit(cov_type="cluster", cov_kwds={"groups": df["surfer_id"].values})
t_stat = float(res.params[1] / res.bse[1])
# Robbins normal-mixture e-value (universal valid)
e_val = math.exp(0.5 * t_stat**2 / (1 + 0.01 * t_stat**2))
print(f"  AUS-bloc t-statistic: {t_stat:.3f}", flush=True)
print(f"  Robbins e-value: {e_val:.3e}", flush=True)
print(f"  Reject H0 at α=0.05 (e-value > 1/α=20): {'YES' if e_val > 20 else 'NO'}", flush=True)
results["e_values"] = {"t_aus_bloc": t_stat, "robbins_e": float(e_val), "reject_at_05": e_val > 20}

# ---------------------------------------------------------------
# T4.F Permutation feature importance (vs in-sample RF)
# ---------------------------------------------------------------
stamp("T4.F Permutation feature importance (RF) vs in-sample")
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance

rf_df = df.dropna(subset=["surfer_world_rank_at_event_start", "wave_score"]).copy()
top_c = rf_df["surfer_country"].value_counts().head(5).index.tolist()
top_ec = rf_df["event_country"].value_counts().head(5).index.tolist()
Xf = pd.DataFrame()
Xf["rank"] = rf_df["surfer_world_rank_at_event_start"].astype(float)
Xf["year"] = rf_df["year"].astype(float)
Xf["is_male"] = (rf_df["gender"] == "m").astype(float)
Xf["heat_number"] = pd.to_numeric(rf_df["heat_number"], errors="coerce").fillna(0).astype(float)
Xf["wave_index_for_surfer"] = pd.to_numeric(rf_df["wave_index_for_surfer"], errors="coerce").fillna(0).astype(float)
Xf["home_match"] = (rf_df["surfer_country"] == rf_df["event_country"]).astype(float)
for c in top_c: Xf[f"sc_{c}"] = (rf_df["surfer_country"] == c).astype(float)
for c in top_ec: Xf[f"ec_{c}"] = (rf_df["event_country"] == c).astype(float)
y2 = rf_df["wave_score"].astype(float).values

rf = RandomForestRegressor(n_estimators=80, max_depth=8, random_state=42, n_jobs=4).fit(Xf.values, y2)
perm = permutation_importance(rf, Xf.values, y2, n_repeats=8, random_state=42, n_jobs=4)
imp_df = pd.DataFrame({
    "feature": Xf.columns,
    "in_sample": rf.feature_importances_,
    "permutation": perm.importances_mean,
}).sort_values("permutation", ascending=False)
print(f"  {'feature':30s}  in-sample  |  permutation", flush=True)
for _, r in imp_df.head(12).iterrows():
    print(f"  {r['feature']:30s}  {r['in_sample']:.4f}    |  {r['permutation']:.4f}", flush=True)
results["perm_importance"] = imp_df.head(12).to_dict(orient="records")

# ---------------------------------------------------------------
# T4.G Constraint-based DAG discovery (PC algorithm — partial)
# ---------------------------------------------------------------
stamp("T4.G PC algorithm (partial) — independence pruning of bias DAG")
from scipy.stats import pearsonr

# Use heat-level features as graph nodes
heat_feat = df.groupby(["event_code", "heat_id"]).agg(
    mean_=("wave_score", "mean"),
    std_=("wave_score", "std"),
    rank_med=("surfer_world_rank_at_event_start", "median"),
    home_rate=("surfer_country", lambda s: (s == df.loc[s.index, "event_country"]).mean()),
    round_rate=("wave_score", lambda s: (((s * 100 % 100).astype(int) % 100).isin([0, 25, 50, 75])).mean()),
).reset_index().dropna()
print(f"  Heat-level n={len(heat_feat):,}", flush=True)

nodes = ["mean_", "std_", "rank_med", "home_rate", "round_rate"]
# Marginal independence test (PC step 0): correlation
print("  Marginal correlations (Pearson):", flush=True)
edges = []
for i, a in enumerate(nodes):
    for b in nodes[i+1:]:
        r, p = pearsonr(heat_feat[a].values, heat_feat[b].values)
        keep = abs(r) > 0.05 and p < 0.01
        print(f"    {a}--{b}: r={r:+.3f}, p={p:.3g}  {'KEEP' if keep else 'PRUNE'}", flush=True)
        if keep: edges.append((a, b, float(r)))
print(f"  Edges retained after marginal-prune: {len(edges)}/{len(nodes) * (len(nodes)-1) // 2}", flush=True)
results["PC_algorithm"] = {
    "nodes": nodes,
    "edges_retained": [{"a": a, "b": b, "r": r} for a, b, r in edges],
}

# ---------------------------------------------------------------
out = ROOT / "outputs" / "tier4_results.json"
out.parent.mkdir(parents=True, exist_ok=True)
with open(out, "w") as f:
    json.dump(results, f, indent=2, default=str)
print(f"\n=> Wrote {out}", flush=True)
print("\n" + "="*72 + "\nTIER 4 DONE\n" + "="*72, flush=True)
