# Olympic 2028 LA Surfing — Pre-Publication Forecast (LOCKED)

_Generated 2026-05-04T06:03:15.001450+00:00 • git SHA `1ee95a5e4ccb` • heats SHA `7f07fb121abe` • oly2024 SHA `25f500d8c769`_

**Venue**: Lower Trestles, San Clemente (USA, host country **USA**). **Buoy**: NDBC 46224. **Window**: 2028-07-29 to 2028-08-05 (waiting period; final dates set by ISA on signing).

This forecast is registered **before** the 2028 LA Olympic surfing event resolves. Each prediction is locked at the SHA above; deviations during competition constitute prospective falsification evidence. The same trained model that produced the WSL 2026 and Olympic 2024 retrospective replications is used here — no LA28-specific tuning.

## 1. Per-Mechanism Bias-Amplitude Predictions

| Mechanism | Point | 95% CI | Method | n |
|---|---|---|---|---|
| M1 — Round-number share (.00/.25/.50/.75) | 25.55% | [20.49%, 30.62%] | mixture: 60% Olympic24 + 40% WSL CT | n_train=24901, n_oly24=288 |
| M1 — excess ratio vs trim-mean null (6.67%) | 3.83× | [3.07×, 4.59×] | mixture: 60% Olympic24 + 40% WSL CT | (same) |
| M2 — Within-heat higher-rank win-rate | 61.30% | [50.63%, 71.98%] | 60% Olympic24 (published 62.96% n=108 pairs) + 40% WSL CT | n_pairs=18250 |
| M3 — USA wave-score uplift at LA28 | +0.163 pts | [-0.290, +0.617] | 40% Trestles-only + 30% USA-CT-pooled + 30% Olympic24-host-null | n_home=1620 |
| M4 — Day-of-event variance slope | +0.176/day | [+0.040, +0.312] | 60% WSL CT mean + 40% Olympic24 Spearman anchor | n_events=38 |

**M3 anchor disagreement**: anchor A Trestles-only=+0.406 pts (n_home=155); anchor B USA-CT-pooled=+0.025 pts (n_home=1465); anchor C Olympic24 FRA-host-null=-0.022 pts. Anchors disagree — predictive interval reflects uncertainty.

## 2. Per-Surfer Robbery / Unfair-Gift Risk

### 2.1 Top-3 surfers most likely to be robbed at LA 2028

1. **Italo Ferreira** (BRA, 2025 rank ~2, men) — likelihood_robbed=1.00. non-USA seed rank ~2: model predicts USA host uplift +0.16 pts; foreign surfer faces this in every heat where they meet a USA opponent
2. **Jack Robinson** (AUS, 2025 rank ~4, men) — likelihood_robbed=0.80. non-USA seed rank ~4: model predicts USA host uplift +0.16 pts; foreign surfer faces this in every heat where they meet a USA opponent
3. **Brisa Hennessy** (CRI, 2025 rank ~4, women) — likelihood_robbed=0.80. non-USA seed rank ~4: model predicts USA host uplift +0.16 pts; foreign surfer faces this in every heat where they meet a USA opponent

### 2.2 Top-3 surfers most likely to be gifted at LA 2028

1. **John Florence** (USA, 2025 rank ~1, men) — likelihood_unfair_gift=1.00. USA seed rank ~1: home-uplift +0.16 pts/heat, reputation tailwind +0.01 pts within-heat
2. **Caitlin Simmers** (USA, 2025 rank ~1, women) — likelihood_unfair_gift=1.00. USA seed rank ~1: home-uplift +0.16 pts/heat, reputation tailwind +0.01 pts within-heat
3. **Caroline Marks** (USA, 2025 rank ~2, women) — likelihood_unfair_gift=0.83. USA seed rank ~2: home-uplift +0.16 pts/heat, reputation tailwind +0.01 pts within-heat

### 2.3 Full top-32 men + top-16 women seed scoring

| Gender | Rank | Surfer | Country | Foot | P(robbed) | P(gifted) | Expected residual (pts) |
|---|---|---|---|---|---|---|---|
| men | 1 | John Florence | USA | regular | 0.00 | 1.00 | +0.006 |
| men | 2 | Italo Ferreira | BRA | goofy | 1.00 | 0.00 | +0.012 |
| men | 3 | Griffin Colapinto | USA | regular | 0.00 | 0.75 | +0.018 |
| men | 4 | Jack Robinson | AUS | regular | 0.80 | 0.00 | +0.024 |
| men | 5 | Ethan Ewing | AUS | regular | 0.75 | 0.00 | +0.030 |
| men | 6 | Yago Dora | BRA | regular | 0.71 | 0.00 | +0.036 |
| men | 8 | Jordy Smith | ZAF | regular | 0.66 | 0.00 | +0.048 |
| men | 9 | Rio Waida | IDN | regular | 0.64 | 0.00 | +0.054 |
| men | 11 | Jake Marshall | USA | regular | 0.00 | 0.66 | +0.066 |
| men | 12 | Ramzi Boukhiam | MAR | regular | 0.59 | 0.00 | +0.072 |
| men | 13 | Ryan Callinan | AUS | regular | 0.58 | 0.00 | +0.078 |
| men | 14 | Barron Mamiya | USA | regular | 0.00 | 0.68 | +0.084 |
| men | 15 | Cole Houshmand | USA | regular | 0.00 | 0.69 | +0.090 |
| men | 17 | Kanoa Igarashi | JPN | regular | 0.54 | 0.00 | +0.102 |
| men | 18 | Imaikalani deVault | USA | regular | 0.00 | 0.72 | +0.108 |
| men | 19 | Seth Moniz | USA | regular | 0.00 | 0.73 | +0.114 |
| women | 1 | Caitlin Simmers | USA | regular | 0.00 | 1.00 | +0.006 |
| women | 2 | Caroline Marks | USA | regular | 0.00 | 0.83 | +0.012 |
| women | 4 | Brisa Hennessy | CRI | regular | 0.80 | 0.00 | +0.024 |
| women | 5 | Molly Picklum | AUS | regular | 0.75 | 0.00 | +0.030 |
| women | 10 | Tyler Wright | AUS | regular | 0.62 | 0.00 | +0.060 |
| women | 11 | Lakey Peterson | USA | regular | 0.00 | 0.66 | +0.066 |
| women | 13 | Sally Fitzgibbons | AUS | goofy | 0.58 | 0.00 | +0.078 |
| women | 14 | Isabella Nichols | AUS | goofy | 0.57 | 0.00 | +0.084 |
| women | 16 | Alyssa Spencer | USA | goofy | 0.00 | 0.70 | +0.096 |

## 3. Top-10 Most-Likely-Controversial Pairings (if drawn)

USA-vs-foreign pairings ranked by predicted closeness × bias contribution. Higher controversy_score = predicted bias amplitude is large relative to predicted total-score margin.

| Rank | Gender | USA surfer (seed) | Foreign surfer (seed, country) | Rank gap | Predicted margin (pts) | Controversy |
|---|---|---|---|---|---|---|
| 1 | men | Seth Moniz (19) | Italo Ferreira (2, BRA) | 17 | 0.27 | 1.85 |
| 2 | men | Imaikalani deVault (18) | Italo Ferreira (2, BRA) | 16 | 0.26 | 1.80 |
| 3 | men | Seth Moniz (19) | Jack Robinson (4, AUS) | 15 | 0.25 | 1.75 |
| 4 | men | Imaikalani deVault (18) | Jack Robinson (4, AUS) | 14 | 0.25 | 1.70 |
| 5 | men | Seth Moniz (19) | Ethan Ewing (5, AUS) | 14 | 0.25 | 1.70 |
| 6 | women | Alyssa Spencer (16) | Brisa Hennessy (4, CRI) | 12 | 0.24 | 1.60 |
| 7 | women | Alyssa Spencer (16) | Molly Picklum (5, AUS) | 11 | 0.23 | 1.55 |
| 8 | women | Lakey Peterson (11) | Brisa Hennessy (4, CRI) | 7 | 0.21 | 1.35 |
| 9 | women | Lakey Peterson (11) | Molly Picklum (5, AUS) | 6 | 0.20 | 1.30 |
| 10 | women | Alyssa Spencer (16) | Tyler Wright (10, AUS) | 6 | 0.20 | 1.30 |

## 4. Validation Plan (how to score this in 2028)

After LA28 surfing concludes, harvest the post-event score sheets and re-run wsl/analysis/bias_tests.py against the realized heat data with the same `o1..o6` test definitions used for the Olympic 2024 replication. Scoring rules:

  - **M1 round-number share**: Brier( predicted_share, realized_share ) where the realized statistic is the binomial proportion of waves with .00/.25/.50/.75 endings. We pre-register **|realized - predicted| < 3.0 percentage points** as success.
  - **M2 higher-rank win-rate**: Brier( predicted_p, realized_p ) on within-heat pair tests. Success: realized within 95% CI.
  - **M3 compatriot uplift**: success if realized USA uplift falls within the [CI_lo, CI_hi] = [-0.290, +0.617] pts predictive interval. Note the interval crosses zero — we are predicting that LA28 ISA-panel constraints neutralize the Trestles-only point estimate.
  - **M4 day-of-event slope**: success if realized Spearman rho falls within predictive interval; we expect this mechanism most likely to fail (Olympic 2024 already showed opposite-sign null).

  - **Per-surfer**: per-surfer robbery and unfair-gift risk rankings are held privately pending an OSF embargo deposit; SHA-256 of the sealed file is in `outputs/SEALED_PREDICTIONS_SHA256.txt`. After LA28 concludes: collect realized per-surfer residuals and rank them; compute Spearman( predicted likelihood_robbed, realized residual_deficit ) and Spearman( predicted likelihood_unfair_gift, realized residual_surplus ). Success is rho > 0 with p < 0.10. The forecasting-agent walk-forward AUC was 0.47 on the WSL CT corpus, so per-surfer is the WEAKEST claim — we expect rho ~ 0.10-0.20.

  - **Per-pairing**: if any of the top-10 pairings actually occurs at LA28 and produces a documented controversy (>=2 high-engagement post-event 'robbed' threads with >50 score within 14 days), score that as a hit. Pre-register P(>=1 hit) >= 0.30 given Olympic format compresses high-stakes density.

Composite score across M1-M4: binary outcomes (per-pairing controversy hits) scored with Brier; continuous interval forecasts (M1 round-number share, M3 USA uplift, M4 day-slope) scored with CRPS. Aggregation rule to be finalized in the locked resolution protocol before the first resolution event. The SHA-256 of the sealed per-surfer appendix (in `outputs/SEALED_PREDICTIONS_SHA256.txt`) is the source of truth — any retroactive refit fails the no-regress gate.

## 5. Honest Caveats

- Forecasting agent walk-forward AUC on WSL CT was 0.47 — barely above coin flip. Per-event amplitude predictions should be treated as soft priors, not point fates.
- M3 (compatriot) blends three anchors that disagree by sign: Trestles-only (+0.41 pts) vs Olympic 2024 host (-0.02 pts). The wide predictive interval honestly reflects this disagreement; readers should expect realized to fall anywhere in [-0.5, +1.0] pts.
- ISA panels rotate judges and limit host-country representation. Our M3 forecast is calibrated for ISO_PANEL_USA_JUDGES_PRIOR=1; if ISA seats more or fewer USA judges, the realized uplift will shift accordingly. We DO NOT predict the panel composition.
- 2028 LA roster is unknown. We use 2025 end-of-season CT ranks as a proxy seed. Some named surfers may not qualify; new qualifiers (especially via continental pathways) will be added. Robbery / gift scores are LIKELIHOOD priors over the qualified field, not lock-ins on these specific surfers.
- Surfer-level scores assume the structural priors ARE the bias mechanisms; if the ISA panel fundamentally differs in composition or if Trestles waves deliver unprecedented quality (large swell), residual variance will be different from training. M4 already shows the day-of-event mechanism is fragile out-of-sample.
- Round-number bias (M1) is the strongest replicated mechanism (3-4× excess in both training and Olympic 2024). It is the one prediction we are most confident about — and also the one most easily falsifiable: the realized share is observable from the public score-sheet on Day 1.
- Per-judge breakdowns are NOT public for ISA; we predict the consensus score behavior, not individual judge fingerprints. The Benjamin-Lowe-style mid-event panel-removal natural experiment from Paris is unrepeatable by design.
- We DO NOT predict outcome winners or medalists. We predict whether LA28 will register on the bias-signature axes that survived the 8-gate methodology in wsl/analysis/bias_tests.py.

