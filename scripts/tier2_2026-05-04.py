"""TIER 2 — SBM, distance correlation + MI, NMF on Nielsen matrix, TMLE, wild cluster bootstrap, DFBETAS.

All local. Zero LLM tokens. Writes outputs/tier2_results.json.
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
# T2.9 SBM (community detection on judge-surfer co-occurrence)
# ---------------------------------------------------------------
stamp("T2.9 Stochastic Block Model — judge-surfer co-occurrence (Louvain proxy)")
import networkx as nx
nat_cols = [c for c in JUDGES.columns if c.startswith("judge_") and "nationality" in c]
sn_map = (HEATS.dropna(subset=["surfer_country", "surfer_name_full"])
          .drop_duplicates("surfer_name_full")
          .set_index("surfer_name_full")["surfer_country"].to_dict())
J = JUDGES.dropna(subset=nat_cols).copy()
J["surfer_country"] = J["surfer_name"].map(sn_map)
J = J.dropna(subset=["surfer_country", "surfer_name"])

# Bipartite graph: judge-nationality (full name) ↔ surfer-country (ISO)
G = nx.Graph()
for _, row in J.sample(min(15000, len(J)), random_state=42).iterrows():
    sc = "S_" + str(row["surfer_country"])
    for c in nat_cols:
        jn = row.get(c)
        if pd.notna(jn):
            G.add_edge(sc, "J_" + str(jn))
print(f"  Graph: nodes={G.number_of_nodes()}, edges={G.number_of_edges()}", flush=True)

try:
    from networkx.algorithms.community import louvain_communities, modularity
    parts = louvain_communities(G, seed=42)
    mod = modularity(G, parts)
    print(f"  Communities: {len(parts)}, modularity Q={mod:.4f}", flush=True)
    for i, p in enumerate(sorted(parts, key=lambda s: -len(s))[:5]):
        print(f"    Community {i+1}: {sorted([n for n in p])[:8]}", flush=True)
    results["SBM_louvain"] = {"n_communities": len(parts), "modularity": float(mod),
                              "top_communities": [sorted(list(p))[:10] for p in sorted(parts, key=lambda s: -len(s))[:5]]}
except Exception as e:
    print(f"  Louvain failed: {e}", flush=True)
    results["SBM_louvain"] = {"error": str(e)}

# ---------------------------------------------------------------
# T2.10 Distance correlation (Szekely) + Mutual information
# ---------------------------------------------------------------
stamp("T2.10 Distance correlation + Mutual information")

def dcor_brute(x, y):
    """Brute-force distance correlation (Szekely-Rizzo)."""
    n = len(x); A = np.abs(x[:, None] - x[None, :]); B = np.abs(y[:, None] - y[None, :])
    A -= A.mean(axis=0)[None, :]; A -= A.mean(axis=1)[:, None]; A += A.mean()
    B -= B.mean(axis=0)[None, :]; B -= B.mean(axis=1)[:, None]; B += B.mean()
    dcov_xy = np.sqrt((A * B).mean())
    dcov_xx = np.sqrt((A * A).mean())
    dcov_yy = np.sqrt((B * B).mean())
    if dcov_xx * dcov_yy == 0: return 0.0
    return float(dcov_xy / np.sqrt(dcov_xx * dcov_yy))

# Pairs to test
sub = df.dropna(subset=["surfer_world_rank_at_event_start"]).sample(min(2000, len(df)), random_state=42)
x_rank = sub["surfer_world_rank_at_event_start"].values.astype(float)
y_score = sub["wave_score"].values.astype(float)
x_year = sub["year"].values.astype(float)
x_hm = (sub["surfer_country"] == sub["event_country"]).astype(float).values

dcor_rank = dcor_brute(x_rank, y_score)
pear_rank = float(np.corrcoef(x_rank, y_score)[0, 1])
spear_rank = float(pd.Series(x_rank).corr(pd.Series(y_score), method="spearman"))
print(f"  rank ↔ score: Pearson={pear_rank:+.4f}, Spearman={spear_rank:+.4f}, dCor={dcor_rank:.4f}", flush=True)

dcor_year = dcor_brute(x_year, y_score)
print(f"  year ↔ score: dCor={dcor_year:.4f}", flush=True)

from sklearn.feature_selection import mutual_info_regression
mi_vals = mutual_info_regression(np.column_stack([x_rank, x_year, x_hm]), y_score, random_state=42)
print(f"  MI (rank, year, home_match) → score: {dict(zip(['rank','year','home_match'], np.round(mi_vals, 4).tolist()))}", flush=True)

results["dcor_MI"] = {
    "rank_score_pearson": pear_rank, "rank_score_spearman": spear_rank, "rank_score_dcor": dcor_rank,
    "year_score_dcor": dcor_year,
    "MI": dict(zip(["rank", "year", "home_match"], mi_vals.tolist())),
}

# ---------------------------------------------------------------
# T2.11 NMF on the 5×5 Nielsen contribution matrix
# ---------------------------------------------------------------
stamp("T2.11 NMF on Nielsen 5×5 dev matrix")
score_cols = [c for c in JUDGES.columns if c.startswith("judge_") and c.endswith("_score")]
ISO_NAME = {"AUS":"Australia", "USA":"United States", "BRA":"Brazil",
            "FRA":"France", "ZAF":"South Africa"}
NAME_TO_ISO = {v: k for k, v in ISO_NAME.items()}
top_isos = list(ISO_NAME.keys())

rows = []
for jc, sc in zip(nat_cols, score_cols):
    s = J[[jc, sc, "surfer_country"]].rename(columns={jc: "jnat", sc: "jscore"}).dropna()
    rows.append(s)
LONG = pd.concat(rows, ignore_index=True)
LONG["jiso"] = LONG["jnat"].map(NAME_TO_ISO)
LONG = LONG[LONG["jiso"].isin(top_isos) & LONG["surfer_country"].isin(top_isos)]
gm = LONG["jscore"].mean()
mat = LONG.groupby(["jiso", "surfer_country"])["jscore"].mean().unstack()
mat = mat.reindex(index=top_isos, columns=top_isos)
print("  Mean-score matrix:", flush=True)
print(mat.round(3).to_string(), flush=True)

# Center to dev, then add constant to make non-negative
dev = mat - gm
shift = abs(dev.min().min()) + 1e-3
M = (dev + shift).fillna(shift).values
from sklearn.decomposition import NMF
for k in [1, 2, 3]:
    nmf = NMF(n_components=k, init="nndsvd", random_state=42, max_iter=1000)
    W = nmf.fit_transform(M)
    H = nmf.components_
    err = nmf.reconstruction_err_
    print(f"  NMF k={k}: reconstruction err={err:.4f}", flush=True)
    if k == 2:
        results["NMF_nielsen_k2"] = {
            "W": {iso: W[i].tolist() for i, iso in enumerate(top_isos)},
            "H": {iso: H[:, i].tolist() for i, iso in enumerate(top_isos)},
            "shift_added": float(shift),
            "reconstruction_err": float(err),
        }
        print(f"    Factor 1 (judge-nat scores): {dict(zip(top_isos, np.round(W[:, 0], 3).tolist()))}", flush=True)
        print(f"    Factor 1 (surfer-country):  {dict(zip(top_isos, np.round(H[0, :], 3).tolist()))}", flush=True)
        print(f"    Factor 2 (judge-nat scores): {dict(zip(top_isos, np.round(W[:, 1], 3).tolist()))}", flush=True)
        print(f"    Factor 2 (surfer-country):  {dict(zip(top_isos, np.round(H[1, :], 3).tolist()))}", flush=True)

# ---------------------------------------------------------------
# T2.12 TMLE / Cross-fit doubly-robust ATE on AUS bloc
# ---------------------------------------------------------------
stamp("T2.12 TMLE / cross-fit DR ATE — AUS bloc")
from econml.dr import LinearDRLearner
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
dr = LinearDRLearner(
    model_propensity=RandomForestClassifier(n_estimators=50, max_depth=4, random_state=42, n_jobs=4),
    model_regression=RandomForestRegressor(n_estimators=50, max_depth=4, random_state=42, n_jobs=4),
    cv=5, random_state=42,
)
dr.fit(Y, T, X=Xc.values)
ate = dr.const_marginal_effect(Xc.values)
ci_lo, ci_hi = dr.const_marginal_effect_interval(Xc.values, alpha=0.05)
print(f"  DR ATE: {ate.mean():+.4f}, 95% CI [{ci_lo.mean():+.4f}, {ci_hi.mean():+.4f}]", flush=True)
results["TMLE_DR_aus_bloc"] = {
    "ate": float(ate.mean()), "ci_lo": float(ci_lo.mean()), "ci_hi": float(ci_hi.mean()), "n": len(Y),
}

# ---------------------------------------------------------------
# T2.13 Wild cluster bootstrap (Cameron-Gelbach-Miller)
# ---------------------------------------------------------------
stamp("T2.13 Wild cluster bootstrap — T2 rank prior + T4 AUS bloc")
import statsmodels.api as sm

def wild_cluster_bootstrap(y, X, groups, B=999, seed=42):
    rng = np.random.RandomState(seed)
    res0 = sm.OLS(y, X).fit()
    beta0 = res0.params[1]
    fit0 = res0.fittedvalues; resid0 = y - fit0
    boot_t = []
    g_vals = pd.Series(groups).unique()
    for _ in range(B):
        # Rademacher weights at cluster level
        w = pd.Series(rng.choice([-1, 1], size=len(g_vals)), index=g_vals).reindex(groups).values
        y_b = fit0 + w * resid0
        res_b = sm.OLS(y_b, X).fit()
        boot_t.append(res_b.params[1] / res_b.bse[1])
    boot_t = np.array(boot_t)
    t_obs = beta0 / res0.bse[1]
    p_wcb = float((np.abs(boot_t) >= np.abs(t_obs)).mean())
    return float(beta0), float(t_obs), p_wcb

# T2 rank prior (heat-FE demean)
t2 = df.dropna(subset=["surfer_world_rank_at_event_start"]).copy()
t2["rank"] = t2["surfer_world_rank_at_event_start"].astype(float)
t2["heat_key"] = t2["event_code"].astype(str) + "_" + t2["heat_id"].astype(str)
def wd(s, g): return s - s.groupby(g).transform("mean")
y_t2 = wd(t2["wave_score"], t2["heat_key"]).values
x_t2 = wd(t2["rank"], t2["heat_key"]).values
beta_t2, t_t2, p_wcb_t2 = wild_cluster_bootstrap(
    y_t2, sm.add_constant(x_t2), t2["surfer_id"].values, B=500
)
print(f"  T2 rank prior: beta={beta_t2:+.5f}, t={t_t2:.3f}, wild-cluster-bootstrap p={p_wcb_t2:.4g}", flush=True)

# T4 AUS bloc (no demean)
y_t4 = df["wave_score"].astype(float).values
T4 = ((df["surfer_country"] == "AUS") & (df["event_country"] == "AUS")).astype(float).values
beta_t4, t_t4, p_wcb_t4 = wild_cluster_bootstrap(
    y_t4, sm.add_constant(T4), df["surfer_id"].values, B=500
)
print(f"  T4 AUS bloc: beta={beta_t4:+.5f}, t={t_t4:.3f}, wild-cluster-bootstrap p={p_wcb_t4:.4g}", flush=True)
results["wild_cluster_bootstrap"] = {
    "T2_rank_prior": {"beta": beta_t2, "t": t_t2, "p_wcb": p_wcb_t2},
    "T4_aus_bloc": {"beta": beta_t4, "t": t_t4, "p_wcb": p_wcb_t4},
}

# ---------------------------------------------------------------
# T2.14 DFBETAS — influence on AUS-bloc estimate
# ---------------------------------------------------------------
stamp("T2.14 DFBETAS — leave-one-event-out influence on AUS-bloc estimate")
events = df["event_code"].unique()
sub = df[["wave_score", "event_code"]].copy()
sub["aus_match"] = ((df["surfer_country"] == "AUS") & (df["event_country"] == "AUS")).astype(float)
all_X = sm.add_constant(sub["aus_match"].values)
res_full = sm.OLS(sub["wave_score"].values, all_X).fit()
beta_full = res_full.params[1]; se_full = res_full.bse[1]
inf = []
for ev in events:
    mask = sub["event_code"] != ev
    if mask.sum() < 100 or sub.loc[mask, "aus_match"].sum() < 5: continue
    res_e = sm.OLS(sub.loc[mask, "wave_score"].values, sm.add_constant(sub.loc[mask, "aus_match"].values)).fit()
    dfbeta = (beta_full - res_e.params[1]) / se_full
    inf.append({"event_code": ev, "dfbeta": float(dfbeta), "n_dropped": int((~mask).sum())})
inf = sorted(inf, key=lambda r: -abs(r["dfbeta"]))
print(f"  Top-10 most-influential events on AUS-bloc:", flush=True)
for r in inf[:10]:
    print(f"    {r['event_code']}: DFBETA={r['dfbeta']:+.4f}, n_dropped={r['n_dropped']}", flush=True)
results["DFBETAS_aus_bloc"] = {"beta_full": float(beta_full), "top10_influential": inf[:10]}

# ---------------------------------------------------------------
out = ROOT / "outputs" / "tier2_results.json"
out.parent.mkdir(parents=True, exist_ok=True)
with open(out, "w") as f:
    json.dump(results, f, indent=2, default=str)
print(f"\n=> Wrote {out}", flush=True)
print("\n" + "="*72 + "\nTIER 2 DONE\n" + "="*72, flush=True)
