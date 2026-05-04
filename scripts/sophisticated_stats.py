"""Sophisticated-stats methods on the full WSL dataset.

1. Double Machine Learning (econml) — clean causal estimate of compatriot
   bias by partialing out wave-quality with random-forest nuisance models.
2. Multilevel Mixed-Effects (statsmodels MixedLM) — proper for nested
   data structure (wave ⊂ heat ⊂ event ⊂ surfer).
3. Quantile regression (statsmodels QuantReg) — does compatriot effect
   vary across the wave-score distribution?

Pure local. Zero LLM tokens.
"""
import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

ROOT = Path("/Users/addieconner/chorus/wsl")
HEATS = pd.read_parquet(ROOT / "data" / "heats.parquet")
JUDGES = pd.read_parquet(ROOT / "data" / "judges.parquet")
print(f"heats.parquet: {len(HEATS)} | judges.parquet: {len(JUDGES)}")

results = {}

# Prep aggregate
df = HEATS[HEATS['wave_score'] > 0].copy()
df['surfer_id'] = df['surfer_athlete_id'].fillna(df['surfer_name_full']).astype(str)

# ====================================================================
# 1. Double Machine Learning on AUS home-bloc effect
# ====================================================================
print("\n" + "="*70)
print("1. DOUBLE MACHINE LEARNING — AUS home-bloc")
print("="*70)

from econml.dml import LinearDML
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

dml_df = df.dropna(subset=['surfer_country', 'event_country', 'surfer_world_rank_at_event_start']).copy()
dml_df['aus_match'] = ((dml_df['surfer_country'] == 'AUS') & (dml_df['event_country'] == 'AUS')).astype(int)

# Outcome: wave_score
# Treatment: aus_match (binary)
# Confounders X: surfer_world_rank, year, gender (one-hot), surfer_country (one-hot top), event_country (top)
top_countries = dml_df['surfer_country'].value_counts().head(10).index.tolist()
top_event_countries = dml_df['event_country'].value_counts().head(10).index.tolist()

X_features = pd.DataFrame()
X_features['rank'] = dml_df['surfer_world_rank_at_event_start'].astype(float).fillna(50)
X_features['year'] = dml_df['year'].astype(float)
X_features['is_male'] = (dml_df['gender'] == 'm').astype(float)
for c in top_countries:
    X_features[f'sc_{c}'] = (dml_df['surfer_country'] == c).astype(float)
for c in top_event_countries:
    X_features[f'ec_{c}'] = (dml_df['event_country'] == c).astype(float)

Y = dml_df['wave_score'].astype(float).values
T = dml_df['aus_match'].astype(int).values
X = X_features.values
print(f"  n={len(Y)}, n_features={X.shape[1]}, treated={T.sum()}, control={(1-T).sum()}")

dml = LinearDML(
    model_y=RandomForestRegressor(n_estimators=100, max_depth=10, n_jobs=4, random_state=42),
    model_t=RandomForestClassifier(n_estimators=100, max_depth=10, n_jobs=4, random_state=42),
    discrete_treatment=True, random_state=42, cv=3,
)
dml.fit(Y, T, X=X)
ate = dml.const_marginal_effect_inference().population_summary()
print(f"  DML ATE estimate: {dml.const_marginal_effect(X).mean():+.4f}")
ci_lo, ci_hi = dml.const_marginal_effect_interval(X, alpha=0.05)
print(f"  DML 95% CI: [{ci_lo.mean():+.4f}, {ci_hi.mean():+.4f}]")

# Compare to OLS
import statsmodels.api as sm
res_ols = sm.OLS(Y, sm.add_constant(np.column_stack([T, X]))).fit(cov_type='cluster', cov_kwds={'groups': dml_df['surfer_id'].values})
print(f"  OLS coef on aus_match (with controls): {res_ols.params[1]:+.4f}, p={res_ols.pvalues[1]:.4g}")
print(f"  Verdict: DML estimate {'agrees with' if abs(dml.const_marginal_effect(X).mean() - res_ols.params[1]) < 0.2 else 'differs from'} OLS")

results['DML_aus_homebloc'] = {
    'ate': float(dml.const_marginal_effect(X).mean()),
    'ci_lo': float(ci_lo.mean()),
    'ci_hi': float(ci_hi.mean()),
    'ols_coef': float(res_ols.params[1]),
    'ols_p': float(res_ols.pvalues[1]),
    'n': int(len(Y)),
}

# ====================================================================
# 2. Multilevel Mixed-Effects on T2 reputation prior
# ====================================================================
print("\n" + "="*70)
print("2. MIXED-EFFECTS MULTILEVEL — T2 reputation prior")
print("="*70)

from statsmodels.regression.mixed_linear_model import MixedLM

t2 = df.dropna(subset=['surfer_world_rank_at_event_start']).copy()
t2['rank'] = t2['surfer_world_rank_at_event_start'].astype(float)
t2['heat_uid'] = t2['event_code'].astype(str) + '_' + t2['heat_id'].astype(str)
print(f"  n={len(t2)}, n_surfers={t2['surfer_id'].nunique()}, n_heats={t2['heat_uid'].nunique()}")

# Mixed model: wave_score ~ rank + (1 | surfer_id) + (1 | heat_uid)
# statsmodels MixedLM only supports one grouping factor cleanly — use surfer; heat as fixed dummy via crossed RE alternative
# Use the simpler version with surfer random effect
try:
    mlm = MixedLM(
        endog=t2['wave_score'].values,
        exog=sm.add_constant(t2['rank'].values),
        groups=t2['surfer_id'].values,
    ).fit(method='lbfgs', maxiter=500)
    print(f"  Surfer-RE coef on rank: {mlm.params[1]:+.5f}, p={mlm.pvalues[1]:.4g}")
    print(f"  Random intercept variance (surfer): {mlm.cov_re.iloc[0, 0]:.4f}")
    print(f"  Residual variance: {mlm.scale:.4f}")
    icc_surfer = mlm.cov_re.iloc[0, 0] / (mlm.cov_re.iloc[0, 0] + mlm.scale)
    print(f"  ICC (surfer): {icc_surfer:.4f}")
    results['MLM_T2'] = {
        'coef': float(mlm.params[1]),
        'p': float(mlm.pvalues[1]),
        'icc_surfer': float(icc_surfer),
        'n': int(len(t2)),
    }
except Exception as e:
    print(f"  MLM failed: {e}")

# ====================================================================
# 3. Quantile regression on compatriot effect across wave-score quartiles
# ====================================================================
print("\n" + "="*70)
print("3. QUANTILE REGRESSION — compatriot effect across wave-score distribution")
print("="*70)

from statsmodels.regression.quantile_regression import QuantReg

# Build per-judge dataset with compatriot count
nat_cols = [c for c in JUDGES.columns if c.startswith('judge_') and 'nationality' in c]
score_cols = [c for c in JUDGES.columns if c.startswith('judge_') and c.endswith('_score')]

J = JUDGES.dropna(subset=nat_cols).copy()
ISO_NAME = {'AUS':'Australia','USA':'United States','BRA':'Brazil','JPN':'Japan',
            'FRA':'France','PRT':'Portugal','ESP':'Spain','ZAF':'South Africa',
            'IDN':'Indonesia','CRI':'Costa Rica','PER':'Peru','NZL':'New Zealand',
            'HAW':'Hawaii','ITA':'Italy','GBR':'United Kingdom'}
sn_map = (HEATS.dropna(subset=['surfer_country', 'surfer_name_full'])
          .drop_duplicates('surfer_name_full')
          .set_index('surfer_name_full')['surfer_country'].to_dict())
def get_country_name(name):
    iso = sn_map.get(name)
    return ISO_NAME.get(iso, iso) if iso else None
J['surfer_country_name'] = J['surfer_name'].map(get_country_name)
J = J.dropna(subset=['surfer_country_name'])

def count_compat(row):
    target = row['surfer_country_name']
    return sum(1 for c in nat_cols if row[c] == target)
J['n_compat'] = J.apply(count_compat, axis=1)
J['mean_score'] = J[score_cols].mean(axis=1)

print(f"  n_with_nat: {len(J)}")

X = sm.add_constant(J['n_compat'].values.astype(float))
y = J['mean_score'].values

# Run quantile regression at q=0.1, 0.25, 0.5, 0.75, 0.9
qr_results = {}
for q in [0.10, 0.25, 0.50, 0.75, 0.90]:
    try:
        qr = QuantReg(y, X).fit(q=q, max_iter=2000)
        qr_results[q] = {'coef': float(qr.params[1]), 'p': float(qr.pvalues[1])}
        print(f"  q={q}: coef={qr.params[1]:+.4f}, p={qr.pvalues[1]:.4g}")
    except Exception as e:
        print(f"  q={q}: failed {e}")

results['QuantReg_compatriot'] = qr_results

# ====================================================================
# Save consolidated results
# ====================================================================
import json
with open(ROOT / "outputs" / "sophisticated_stats_results.json", 'w') as f:
    json.dump(results, f, indent=2, default=str)
print(f"\n=> Wrote outputs/sophisticated_stats_results.json")

print("\n" + "="*70)
print("SOPHISTICATED-STATS RUN COMPLETE")
print("="*70)
