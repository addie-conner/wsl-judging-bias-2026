"""Patch wild cluster bootstrap (proper Rademacher) + VAR (column-name fix).

Local. Zero LLM tokens. Writes outputs/patch_yellow_flags_results.json.
"""
import json, warnings
from pathlib import Path
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore")

ROOT = Path("/Users/addieconner/chorus/wsl")
HEATS = pd.read_parquet(ROOT / "data" / "heats.parquet")
df = HEATS[HEATS["wave_score"] > 0].copy()
df["surfer_id"] = df["surfer_athlete_id"].fillna(df["surfer_name_full"]).astype(str)
results: dict = {}

import statsmodels.api as sm

def stamp(t): print(f"\n{'='*72}\n{t}\n{'='*72}", flush=True)

# ---------------------------------------------------------------
# PATCH 1: Wild cluster bootstrap (Cameron–Gelbach–Miller) — correct version
# Bug fix: previous version used a residual under unrestricted model and Rademacher
# weights at cluster level but compared bootstrap t to original t (two-sided).
# Correct approach: impose H0 on residuals (e.g., demean coefficient on null),
# bootstrap residuals * cluster-level Rademacher, refit, collect t under null.
# ---------------------------------------------------------------
stamp("PATCH 1 — Wild cluster bootstrap with restricted residuals (CGM-correct)")

def wild_cluster_bootstrap_restricted(y, X_full, X_null, groups, B=999, seed=42):
    """
    Cameron-Gelbach-Miller wild cluster bootstrap with restricted residuals.

    Args:
      y: outcome
      X_full: full design including treated coef
      X_null: null design (drops the treated coef of interest); residuals from this
              fit are what we wild-bootstrap-perturb.
      groups: cluster id array
      B: bootstrap reps

    Returns: (beta_full, t_full, p_wcb)
    """
    rng = np.random.RandomState(seed)
    res_full = sm.OLS(y, X_full).fit()
    beta_full = res_full.params[1]
    se_full = res_full.bse[1]
    t_full = beta_full / se_full

    # Restricted fit (under H0: coef on treatment = 0)
    res_null = sm.OLS(y, X_null).fit()
    fit_null = res_null.fittedvalues
    resid_null = y - fit_null

    g_unique = pd.Series(groups).unique()
    boot_t = np.zeros(B)
    for b in range(B):
        # Rademacher weights at cluster level
        w_cluster = pd.Series(rng.choice([-1, 1], size=len(g_unique)), index=g_unique)
        w = w_cluster.reindex(groups).values
        y_b = fit_null + w * resid_null
        res_b = sm.OLS(y_b, X_full).fit()
        if res_b.bse[1] > 0:
            boot_t[b] = res_b.params[1] / res_b.bse[1]
        else:
            boot_t[b] = np.nan
    boot_t = boot_t[~np.isnan(boot_t)]
    p_wcb = float((np.abs(boot_t) >= np.abs(t_full)).mean())
    return float(beta_full), float(t_full), p_wcb, len(boot_t)

# T2 rank prior (heat-FE demean)
t2 = df.dropna(subset=["surfer_world_rank_at_event_start"]).copy()
t2["rank"] = t2["surfer_world_rank_at_event_start"].astype(float)
t2["heat_key"] = t2["event_code"].astype(str) + "_" + t2["heat_id"].astype(str)
def wd(s, g): return s - s.groupby(g).transform("mean")
y_t2 = wd(t2["wave_score"], t2["heat_key"]).values
x_t2 = wd(t2["rank"], t2["heat_key"]).values
X_full_t2 = sm.add_constant(x_t2)
X_null_t2 = np.ones((len(y_t2), 1))  # intercept only
b2, t2_, p2, B2 = wild_cluster_bootstrap_restricted(y_t2, X_full_t2, X_null_t2,
                                                    t2["surfer_id"].values, B=999, seed=42)
print(f"  T2 rank prior: beta={b2:+.5f}, t={t2_:.3f}, WCB-p={p2:.4g} (B={B2})", flush=True)

# T4 AUS bloc
y_t4 = df["wave_score"].astype(float).values
T4 = ((df["surfer_country"] == "AUS") & (df["event_country"] == "AUS")).astype(float).values
X_full_t4 = sm.add_constant(T4)
X_null_t4 = np.ones((len(y_t4), 1))
b4, t4_, p4, B4 = wild_cluster_bootstrap_restricted(y_t4, X_full_t4, X_null_t4,
                                                    df["surfer_id"].values, B=999, seed=42)
print(f"  T4 AUS bloc: beta={b4:+.5f}, t={t4_:.3f}, WCB-p={p4:.4g} (B={B4})", flush=True)

results["wild_cluster_bootstrap_corrected"] = {
    "T2_rank_prior": {"beta": b2, "t": t2_, "p_wcb": p2, "B": B2},
    "T4_aus_bloc": {"beta": b4, "t": t4_, "p_wcb": p4, "B": B4},
    "method": "Cameron-Gelbach-Miller restricted-residuals wild cluster bootstrap",
}

# ---------------------------------------------------------------
# PATCH 2: VAR (column-name fix) — explicit DataFrame with exact column labels
# ---------------------------------------------------------------
stamp("PATCH 2 — Vector autoregression on event-level dynamics (column-fix)")
from statsmodels.tsa.api import VAR

ev = df.groupby("event_code").agg(
    mean_score=("wave_score", "mean"),
    round_rate=("wave_score", lambda s: (((s * 100 % 100).astype(int) % 100).isin([0, 25, 50, 75])).mean()),
    heat_std=("wave_score", "std"),
    year=("year", "first"),
).reset_index().sort_values("year").dropna()
data_df = ev[["mean_score", "round_rate", "heat_std"]].reset_index(drop=True)
print(f"  VAR data: n_events={len(data_df)}", flush=True)

try:
    model = VAR(data_df.values)  # use array; columns referenced by integer position
    sel = model.select_order(maxlags=4)
    print(f"  VAR optimal lag (BIC index): {sel.bic}", flush=True)
    fitted = model.fit(maxlags=2)
    print(f"  VAR(2) AIC={fitted.aic:.3f}, BIC={fitted.bic:.3f}", flush=True)
    # Granger via fitted column-index directly (positional)
    # round_rate is column 1; mean_score is column 0
    gc1 = fitted.test_causality(0, [1], kind="f")  # round_rate -> mean_score
    gc2 = fitted.test_causality(1, [0], kind="f")  # mean_score -> round_rate
    print(f"  Granger: round_rate → mean_score: F={gc1.test_statistic:.3f}, p={gc1.pvalue:.4g}", flush=True)
    print(f"  Granger: mean_score → round_rate: F={gc2.test_statistic:.3f}, p={gc2.pvalue:.4g}", flush=True)
    results["VAR_corrected"] = {
        "n_events": len(data_df),
        "lag_bic": int(sel.bic) if sel.bic else None,
        "var2_aic": float(fitted.aic), "var2_bic": float(fitted.bic),
        "granger_round_to_score_p": float(gc1.pvalue),
        "granger_score_to_round_p": float(gc2.pvalue),
        "granger_round_to_score_F": float(gc1.test_statistic),
        "granger_score_to_round_F": float(gc2.test_statistic),
    }
except Exception as e:
    print(f"  VAR failed: {e}", flush=True)
    results["VAR_corrected"] = {"error": str(e)}

# Save
out = ROOT / "outputs" / "patch_yellow_flags_results.json"
with open(out, "w") as f:
    json.dump(results, f, indent=2, default=str)
print(f"\n=> Wrote {out}", flush=True)
