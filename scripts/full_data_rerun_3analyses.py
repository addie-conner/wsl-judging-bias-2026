"""Re-run heterogeneity + H32 + mechanism cross-corr on new 60K-row dataset.

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
print(f"heats={len(HEATS):,} | judges={len(JUDGES):,}")

results = {}

# ====================================================================
# 1. HETEROGENEITY — per-surfer bias residual (with more power now)
# ====================================================================
print("\n" + "="*70)
print("1. HETEROGENEITY (n=60,834 dataset)")
print("="*70)

df = HEATS[HEATS['wave_score'] > 0].copy()
df['surfer_id'] = df['surfer_athlete_id'].fillna(df['surfer_name_full']).astype(str)

# Compute per-surfer residual = wave_score - heat_mean - surfer_career_mean + global_mean
df['heat_mean'] = df.groupby(['event_code', 'heat_id'])['wave_score'].transform('mean')
df['surfer_career_mean'] = df.groupby('surfer_id')['wave_score'].transform('mean')
gm = df['wave_score'].mean()
df['residual'] = df['wave_score'] - df['heat_mean'] - df['surfer_career_mean'] + gm

# Per-surfer bias residual + bootstrap CI (1000 reps)
np.random.seed(42)
surfer_results = []
for sid, grp in df.groupby('surfer_id'):
    if len(grp) < 50:
        continue
    name = grp['surfer_name_full'].iloc[0]
    country = grp['surfer_country'].iloc[0] if 'surfer_country' in grp.columns else None
    res = grp['residual'].values
    mean_res = res.mean()
    # bootstrap
    boots = []
    for _ in range(1000):
        idx = np.random.choice(len(res), len(res), replace=True)
        boots.append(res[idx].mean())
    boots = np.array(boots)
    surfer_results.append({
        'surfer': name,
        'country': country,
        'n_waves': len(grp),
        'bias_resid': float(mean_res),
        'ci_lo': float(np.percentile(boots, 2.5)),
        'ci_hi': float(np.percentile(boots, 97.5)),
        'sig': bool(np.percentile(boots, 2.5) > 0 or np.percentile(boots, 97.5) < 0),
    })

sdf = pd.DataFrame(surfer_results).sort_values('bias_resid', ascending=False)
sdf.to_parquet(ROOT / "data" / "heterogeneity_full_data.parquet", index=False)
print(f"\nTop-5 OVER-scored (CI excludes zero):")
top_over = sdf[sdf['sig'] & (sdf['bias_resid'] > 0)].head(5)
for _, r in top_over.iterrows():
    print(f"  {r['surfer']} ({r['country']}, n={r['n_waves']}): {r['bias_resid']:+.4f} [CI {r['ci_lo']:+.3f}, {r['ci_hi']:+.3f}]")

print(f"\nTop-5 UNDER-scored (CI excludes zero):")
bot = sdf[sdf['sig'] & (sdf['bias_resid'] < 0)].sort_values('bias_resid').head(5)
for _, r in bot.iterrows():
    print(f"  {r['surfer']} ({r['country']}, n={r['n_waves']}): {r['bias_resid']:+.4f} [CI {r['ci_lo']:+.3f}, {r['ci_hi']:+.3f}]")

results['heterogeneity'] = {
    'n_surfers': len(sdf),
    'n_significant': int(sdf['sig'].sum()),
    'top_over_scored': sdf[sdf['sig']].head(10)[['surfer', 'country', 'n_waves', 'bias_resid']].to_dict(orient='records'),
    'top_under_scored': sdf[sdf['sig']].sort_values('bias_resid').head(10)[['surfer', 'country', 'n_waves', 'bias_resid']].to_dict(orient='records'),
}

# ====================================================================
# 2. H32 BRA-stacked panels — graph-level confirmation on full data
# ====================================================================
print("\n" + "="*70)
print("2. H32 BRA-PANEL ROTATION (full per-judge data)")
print("="*70)

nat_cols = [c for c in JUDGES.columns if c.startswith('judge_') and 'nationality' in c]
J = JUDGES.dropna(subset=nat_cols).copy()
print(f"Per-judge with nationality: {len(J):,}")

# Map ISO → name
ISO_NAME = {'BRA': 'Brazil', 'USA': 'United States', 'AUS': 'Australia', 'JPN': 'Japan',
            'FRA': 'France', 'ZAF': 'South Africa', 'PRT': 'Portugal'}

# Get surfer country
sn_map = (HEATS.dropna(subset=['surfer_country', 'surfer_name_full'])
          .drop_duplicates('surfer_name_full')
          .set_index('surfer_name_full')['surfer_country'].to_dict())
J['surfer_country_iso'] = J['surfer_name'].map(sn_map)

# For BRA surfers, count BRA judges on panel
bra_J = J[J['surfer_country_iso'] == 'BRA'].copy()
def count_bra_judges(row):
    return sum(1 for c in nat_cols if row[c] == 'Brazil')
bra_J['n_bra_judges'] = bra_J.apply(count_bra_judges, axis=1)

print(f"\nBRA surfers in dataset: {len(bra_J):,}")
print("\nBRA-stacked panel rate by year:")
print(f"  Year | n waves | ≥1 BRA judge | ≥2 BRA judges | mean BRA judges")
for yr in sorted(bra_J['year'].dropna().unique().astype(int).tolist()):
    sub = bra_J[bra_J['year'] == yr]
    if len(sub) < 50: continue
    n = len(sub)
    p1 = (sub['n_bra_judges'] >= 1).mean()
    p2 = (sub['n_bra_judges'] >= 2).mean()
    mean = sub['n_bra_judges'].mean()
    print(f"  {yr} | {n:>5} | {p1*100:>5.1f}% | {p2*100:>5.1f}% | {mean:.2f}")
    results.setdefault('h32_bra_panels_by_year', {})[int(yr)] = {
        'n': n,
        'pct_at_least_1_bra': float(p1),
        'pct_at_least_2_bra': float(p2),
        'mean_bra_judges': float(mean),
    }

# AUS placebo
aus_J = J[J['surfer_country_iso'] == 'AUS'].copy()
def count_aus_judges(row):
    return sum(1 for c in nat_cols if row[c] == 'Australia')
aus_J['n_aus_judges'] = aus_J.apply(count_aus_judges, axis=1)

print("\nAUS PLACEBO panel rate by year:")
print(f"  Year | n waves | ≥2 AUS judges | mean AUS judges")
for yr in sorted(aus_J['year'].dropna().unique().astype(int).tolist()):
    sub = aus_J[aus_J['year'] == yr]
    if len(sub) < 50: continue
    p2 = (sub['n_aus_judges'] >= 2).mean()
    mean = sub['n_aus_judges'].mean()
    print(f"  {yr} | {len(sub):>5} | {p2*100:>5.1f}% | {mean:.2f}")

# ====================================================================
# 3. Mechanism cross-correlation matrix — does unification still fail?
# ====================================================================
print("\n" + "="*70)
print("3. MECHANISM CROSS-CORRELATION (60K-row data)")
print("="*70)

# Per-heat 4-mechanism vector
heat_mech = df.groupby(['event_code', 'heat_id']).agg({
    'wave_score': ['mean', 'std', 'count'],
}).reset_index()
heat_mech.columns = ['event_code', 'heat_id', 'heat_mean', 'heat_std', 'heat_n']

# M1: round-number rate
def round_rate(g):
    last = (g['wave_score'] * 100 % 100).astype(int)
    return ((last == 0) | (last == 25) | (last == 50) | (last == 75)).mean()

m1 = df.groupby(['event_code', 'heat_id']).apply(round_rate).reset_index()
m1.columns = ['event_code', 'heat_id', 'M1_round']

# M2: rank-residual gap (does best-ranked surfer outscore worst-ranked?)
def rank_gap(g):
    if g['surfer_world_rank_at_event_start'].notna().sum() < 2:
        return np.nan
    sub = g.dropna(subset=['surfer_world_rank_at_event_start'])
    sub = sub.sort_values('surfer_world_rank_at_event_start')
    if len(sub) < 2: return np.nan
    return sub.iloc[0]['wave_score'] - sub.iloc[-1]['wave_score']
m2 = df.groupby(['event_code', 'heat_id']).apply(rank_gap).reset_index()
m2.columns = ['event_code', 'heat_id', 'M2_rank_gap']

# M3: AUS home-match rate (binary 0/1 per heat)
def aus_match_rate(g):
    if g['event_country'].iloc[0] != 'AUS': return 0
    return (g['surfer_country'] == 'AUS').mean()
m3 = df.groupby(['event_code', 'heat_id']).apply(aus_match_rate).reset_index()
m3.columns = ['event_code', 'heat_id', 'M3_aus_match']

# Merge
mech = heat_mech.merge(m1, on=['event_code', 'heat_id']).merge(m2, on=['event_code', 'heat_id']).merge(m3, on=['event_code', 'heat_id'])
mech_cols = ['M1_round', 'M2_rank_gap', 'M3_aus_match', 'heat_std']
mech_clean = mech[mech_cols].dropna()
print(f"\nHeats with all 4 mechanisms: {len(mech_clean)}")

# Cross-correlation matrix
print("\nPearson correlation matrix:")
corr = mech_clean.corr()
print(corr.round(3))

# PCA
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
X_pca = StandardScaler().fit_transform(mech_clean.values)
pca = PCA(n_components=4)
pca.fit(X_pca)
print(f"\nPCA explained variance ratio: {pca.explained_variance_ratio_.round(3)}")
print(f"PC1 explains: {pca.explained_variance_ratio_[0]*100:.1f}%")

# Verdict
mean_abs_corr = corr.values[np.triu_indices_from(corr.values, k=1)]
mean_abs_corr = np.abs(mean_abs_corr).mean()
print(f"\nMean |off-diagonal correlation|: {mean_abs_corr:.3f}")
if mean_abs_corr > 0.4:
    print("  Verdict: STRONG unification (mechanisms cluster)")
elif mean_abs_corr > 0.2:
    print("  Verdict: MODERATE unification")
else:
    print("  Verdict: WEAK / INDEPENDENT (consistent with previous finding)")

results['mechanism_cross_corr'] = {
    'mean_abs_corr': float(mean_abs_corr),
    'pc1_var_explained': float(pca.explained_variance_ratio_[0]),
    'verdict': 'INDEPENDENT' if mean_abs_corr < 0.2 else ('MODERATE' if mean_abs_corr < 0.4 else 'STRONG'),
}

# Save
with open(ROOT / "outputs" / "full_data_rerun_results.json", 'w') as f:
    json.dump(results, f, indent=2, default=str)

print("\n" + "="*70)
print("DONE — saved to outputs/full_data_rerun_results.json")
print("="*70)
