"""Paper-grade FULL analysis on the new 60,834-row / 301,478-judge-score dataset.

3 components:
  A. Full primary + exploratory tests on FULL data (multi-spec)
  B. DML with tighter hyperparameters (max_depth=4, 30 trees)
  C. Multilevel mixed-effects (statsmodels MixedLM)

Pure local. Zero LLM tokens.
"""
import pandas as pd
import numpy as np
from pathlib import Path
import json
import warnings
warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent.parent
HEATS = pd.read_parquet(ROOT / "data" / "heats.parquet")
JUDGES = pd.read_parquet(ROOT / "data" / "judges.parquet")
print(f"heats.parquet: {len(HEATS)} | judges.parquet: {len(JUDGES)}")

score_cols = [c for c in JUDGES.columns if c.startswith('judge_') and c.endswith('_score')]
nat_cols = [c for c in JUDGES.columns if c.startswith('judge_') and 'nationality' in c]
total_scores = sum(JUDGES[c].notna().sum() for c in score_cols)
total_nat = sum(JUDGES[c].notna().sum() for c in nat_cols)
print(f"Individual judge-scores: {total_scores:,}")
print(f"With nationality: {total_nat:,} ({100*total_nat/total_scores:.1f}%)")

results = {}
df = HEATS[HEATS['wave_score'] > 0].copy()
df['surfer_id'] = df['surfer_athlete_id'].fillna(df['surfer_name_full']).astype(str)

import statsmodels.api as sm
from statsmodels.regression.linear_model import OLS

def within_demean(s, group):
    return s - s.groupby(group).transform('mean')

# ============================================================
# A. PRIMARY TESTS — multi-spec on FULL DATA
# ============================================================
print("\n" + "="*70)
print("A. PRIMARY TESTS on full dataset")
print("="*70)

# T2 reputation prior (multi-spec)
print("\n--- T2 Reputation Prior ---")
t2 = df.dropna(subset=['surfer_world_rank_at_event_start']).copy()
t2['rank'] = t2['surfer_world_rank_at_event_start'].astype(float)
t2['heat_key'] = t2['event_code'].astype(str) + '_' + t2['heat_id'].astype(str)
t2_specs = {}

# S3: heat-FE only (canonical Findlay)
y3 = within_demean(t2['wave_score'], t2['heat_key']).values
x3 = within_demean(t2['rank'], t2['heat_key']).values
X = sm.add_constant(x3)
res = OLS(y3, X).fit(cov_type='cluster', cov_kwds={'groups': t2['surfer_id'].values})
t2_specs['heat_FE'] = {'coef': float(res.params[1]), 'p': float(res.pvalues[1]), 'n': len(t2)}
print(f"  Heat-FE: coef={res.params[1]:+.5f}, p={res.pvalues[1]:.4g}, n={len(t2)}")

# S4: no FE
X = sm.add_constant(t2['rank'].values)
res = OLS(t2['wave_score'].values, X).fit(cov_type='cluster', cov_kwds={'groups': t2['surfer_id'].values})
t2_specs['no_FE'] = {'coef': float(res.params[1]), 'p': float(res.pvalues[1])}
print(f"  No-FE: coef={res.params[1]:+.5f}, p={res.pvalues[1]:.4g}")

results['T2'] = t2_specs

# T4 home-bloc per-country (now richer with more data)
print("\n--- T4 Home-Bloc Per-Country ---")
t4_blocs = {}
for country in ['AUS', 'BRA', 'USA', 'JPN', 'ZAF', 'FRA', 'PRT', 'IDN', 'PER', 'NZL', 'CRI']:
    mask = (df['surfer_country'] == country) & (df['event_country'] == country)
    if mask.sum() < 30:
        continue
    df['ctry_match'] = mask.astype(float)
    X = sm.add_constant(df['ctry_match'].values)
    res = OLS(df['wave_score'].values, X).fit(cov_type='cluster', cov_kwds={'groups': df['surfer_id'].values})
    t4_blocs[country] = {'coef': float(res.params[1]), 'p': float(res.pvalues[1]), 'n_match': int(mask.sum())}
    print(f"  {country}: coef={res.params[1]:+.4f}, p={res.pvalues[1]:.4g}, n_match={int(mask.sum())}")

results['T4_blocs'] = t4_blocs

# H11 round-number bias on FULL per-judge corpus
print("\n--- H11 Round-Number Bias (per-judge) ---")
all_scores = []
for c in score_cols:
    all_scores.extend(JUDGES[c].dropna().tolist())
ajs = pd.Series(all_scores)
last_dec = (ajs * 100 % 100).astype(int)
round_05 = ((last_dec == 0) | (last_dec == 50)).sum()
total_j = len(ajs)
pct = round_05 / total_j
print(f"  Per-judge: {round_05:,}/{total_j:,} = {pct*100:.2f}% on .0/.5 endings")
print(f"  Excess vs uniform (20%): {pct/0.20:.2f}×")
results['H11_per_judge'] = {'pct': float(pct), 'excess': float(pct/0.20), 'n': int(total_j)}

# Compatriot effect — by year (paper-defining longitudinal)
print("\n--- Compatriot effect by year ---")
ISO_NAME = {'AUS':'Australia','USA':'United States','BRA':'Brazil','JPN':'Japan',
            'FRA':'France','PRT':'Portugal','ESP':'Spain','ZAF':'South Africa',
            'IDN':'Indonesia','CRI':'Costa Rica','PER':'Peru','NZL':'New Zealand',
            'HAW':'Hawaii','ITA':'Italy','GBR':'United Kingdom'}
sn_map = (HEATS.dropna(subset=['surfer_country', 'surfer_name_full'])
          .drop_duplicates('surfer_name_full')
          .set_index('surfer_name_full')['surfer_country'].to_dict())
J = JUDGES.dropna(subset=nat_cols).copy()
J['surfer_country_iso'] = J['surfer_name'].map(sn_map)
J['surfer_country_name'] = J['surfer_country_iso'].map(ISO_NAME)
J = J.dropna(subset=['surfer_country_name'])

def cnt(row):
    return sum(1 for c in nat_cols if row[c] == row['surfer_country_name'])
J['n_compat'] = J.apply(cnt, axis=1)
J['mean_score'] = J[score_cols].mean(axis=1)
print(f"  n_with_data: {len(J):,}")

yearly = {}
for yr in sorted(J['year'].dropna().unique().astype(int).tolist()):
    sub = J[J['year'] == yr]
    if len(sub) < 100: continue
    X = sm.add_constant(sub['n_compat'].values.astype(float))
    try:
        r = OLS(sub['mean_score'].values, X).fit(
            cov_type='cluster', cov_kwds={'groups': sub['surfer_name'].astype(str).values})
        yearly[yr] = {'coef': float(r.params[1]), 'p': float(r.pvalues[1]), 'n': len(sub)}
        print(f"  {yr}: coef={r.params[1]:+.4f}, p={r.pvalues[1]:.4g}, n={len(sub):,}")
    except Exception:
        pass
results['compat_by_year'] = yearly

# ============================================================
# B. DML WITH TIGHTER HYPERPARAMETERS
# ============================================================
print("\n" + "="*70)
print("B. DOUBLE MACHINE LEARNING — AUS bloc, tight hyperparameters")
print("="*70)
from econml.dml import LinearDML
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

dml_df = df.dropna(subset=['surfer_country', 'event_country', 'surfer_world_rank_at_event_start']).copy()
dml_df['aus_match'] = ((dml_df['surfer_country'] == 'AUS') & (dml_df['event_country'] == 'AUS')).astype(int)
top_c = dml_df['surfer_country'].value_counts().head(8).index.tolist()
top_ec = dml_df['event_country'].value_counts().head(8).index.tolist()
Xf = pd.DataFrame()
Xf['rank'] = dml_df['surfer_world_rank_at_event_start'].astype(float).fillna(50)
Xf['year'] = dml_df['year'].astype(float)
Xf['is_male'] = (dml_df['gender'] == 'm').astype(float)
for c in top_c: Xf[f'sc_{c}'] = (dml_df['surfer_country'] == c).astype(float)
for c in top_ec: Xf[f'ec_{c}'] = (dml_df['event_country'] == c).astype(float)

Y = dml_df['wave_score'].astype(float).values
T = dml_df['aus_match'].astype(int).values
X = Xf.values
print(f"  n={len(Y):,}, n_features={X.shape[1]}, treated={T.sum()}")

# Tighter: fewer trees, max_depth=4 to constrain
dml = LinearDML(
    model_y=RandomForestRegressor(n_estimators=50, max_depth=4, n_jobs=4, random_state=42),
    model_t=RandomForestClassifier(n_estimators=50, max_depth=4, n_jobs=4, random_state=42),
    discrete_treatment=True, random_state=42, cv=5,
)
dml.fit(Y, T, X=X)
ate = dml.const_marginal_effect(X)
ci_lo, ci_hi = dml.const_marginal_effect_interval(X, alpha=0.05)
print(f"  DML ATE: {ate.mean():+.4f}, 95% CI [{ci_lo.mean():+.4f}, {ci_hi.mean():+.4f}]")
print(f"  DML std across pop: {ate.std():.4f}")
results['DML_aus_bloc_tight'] = {
    'ate': float(ate.mean()), 'ci_lo': float(ci_lo.mean()), 'ci_hi': float(ci_hi.mean()),
    'n': len(Y),
}

# ============================================================
# C. MULTILEVEL MIXED-EFFECTS
# ============================================================
print("\n" + "="*70)
print("C. MULTILEVEL MIXED-EFFECTS — T2 with proper hierarchical structure")
print("="*70)
from statsmodels.regression.mixed_linear_model import MixedLM

# Use a sample for tractability (full would take hours)
sample_size = min(15000, len(t2))
ts = t2.sample(sample_size, random_state=42)
print(f"  n_sample: {sample_size:,}")
try:
    mlm = MixedLM(
        endog=ts['wave_score'].values,
        exog=sm.add_constant(ts['rank'].values),
        groups=ts['surfer_id'].values,
    ).fit(method='lbfgs', maxiter=1000)
    icc = mlm.cov_re.iloc[0, 0] / (mlm.cov_re.iloc[0, 0] + mlm.scale)
    print(f"  Coef on rank: {mlm.params[1]:+.5f}, p={mlm.pvalues[1]:.4g}")
    print(f"  ICC (surfer): {icc:.4f}")
    print(f"  Random intercept var: {mlm.cov_re.iloc[0, 0]:.4f}")
    print(f"  Residual var: {mlm.scale:.4f}")
    results['MLM_T2'] = {
        'coef': float(mlm.params[1]),
        'p': float(mlm.pvalues[1]),
        'icc_surfer': float(icc),
        'n': sample_size,
    }
except Exception as e:
    print(f"  MixedLM failed: {e}")

# Save
output = ROOT / "outputs" / "full_paper_grade_results.json"
with open(output, 'w') as f:
    json.dump(results, f, indent=2, default=str)
print(f"\n=> Wrote {output}")
print("\n" + "="*70)
print("PAPER-GRADE ANALYSIS COMPLETE")
print("="*70)
