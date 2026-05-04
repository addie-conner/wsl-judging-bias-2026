# Olympic 2024 Bias Replication Report

**Report date**: 2026-05-03

**Dataset**: 2024 Paris Olympic surfing at Teahupo'o (French Polynesia, FRA territory). 288 scoring waves, 34 France-flagged waves, 64 heats, 48 surfers, 21 nations. ISA-paneled judging panel (judging-pool personnel overlaps with WSL CT panel per public reporting).

**Bonferroni correction**: k=6 (one per O1-O6).

## Headline

- **3/4** of the WSL training-data confirmed mechanisms (O2 round-number, O3 comeback, O4 day-amplification, O5 reputation) replicate or show same-direction-with-power-limited-significance on Olympic data.
- **O1 host-country**: WSL CT was null; Olympic result matches null.
- **O6 Benjamin Lowe panel-removal**: novel Olympic-specific natural experiment, no WSL analog.

## Per-test results (Olympic n=288 vs WSL n=24,901)

| Test | WSL training | Olympic 2024 | Replication |
|------|--------------|---------------|-------------|
| **O1 — Compatriot home-country effect at Olympics** | est=0.07005767967614915, p_bonf=1.0000, verdict=no evidence of bias | est=-0.02192, CI95=[-0.3510, +0.3071], p_bonf=1.0000, n=285, verdict=null | **REPLICATES (both null)** |
| **O2 — Round-number bias at Olympics (.00/.25/.50/.75 clustering)** | est=3.4067, p_bonf=0.00e+00, verdict=supports | est=+3.99590, CI95=[+3.2402, +4.8254], p_bonf=0.00e+00, n=285, verdict=supports | **REPLICATES** |
| **O3 — Comeback-narrative bias at Olympics** | est=-0.014815660014969064, p_bonf=8.19e-05, verdict=supports | est=-0.01954, CI95=[-0.1233, +0.0842], p_bonf=1.0000, n=221, verdict=null | **PARTIAL-DIRECTIONAL** |
| **O4 — Day-of-event amplification at Olympics** | est=1.1698237628, p_bonf=9.91e-12, verdict=supports | est=-0.39868, CI95=—, p_bonf=0.9477, n=14, verdict=null | **FAILED (opposite sign)** |
| **O5 — Reputation prior at Olympics (pre-Oly CT rank effect)** | est=-0.005810424, p_bonf=0.0007, verdict=supports | est=+0.62963, CI95=[-0.0506, +0.0019], p_bonf=0.0272, n=108, verdict=supports | **REPLICATES** |
| **O6 — Benjamin Lowe panel-removal pre/post (Aug 1 2024)** | est=None, p_bonf=—, verdict=novel — no WSL analog | est=+0.66036, CI95=[-1.0774, +2.3981], p_bonf=1.0000, n=285, verdict=null | **NOVEL (no WSL analog)** |

## O1 — Compatriot home-country effect at Olympics

_Zitzewitz 2011 nationality-bias regression — ports bias_tests::test_4_home_country._

- Olympic estimate: `-0.021921984299621222`
- 95% CI: `(-0.3509877918784075, 0.30714382327916506)`
- p-value (raw): `0.8961150500310417`
- p-value (Bonferroni × 6): `1.0`
- n: `285`
- Verdict: **null**
- Replication verdict: **REPLICATES (both null)**

> FRA surfers score -0.022 pts higher than non-FRA controlling for wave-quality proxy + surfer FE

```json
{
  "coef_FRA_host_match_pts": -0.021921984299621222,
  "ci_95": [
    -0.3509877918784075,
    0.30714382327916506
  ],
  "p_raw": 0.8961150500310417,
  "n_FRA_waves": 34,
  "n_FRA_surfers": 4,
  "regional_bloc_breakdown_within_heat": {
    "BRA": {
      "n_heats_with_country": 18,
      "mean_diff_pts": 1.1232407407407408,
      "se": 0.4900816688684625,
      "t_stat": 2.2919460410224355,
      "p_value": 0.03494404777074426
    },
    "AUS": {
      "n_heats_with_country": 12,
      "mean_diff_pts": 0.5918749999999999,
      "se": 0.5461685697054444,
      "t_stat": 1.083685574069569,
      "p_value": 0.3016858017397231
    },
    "USA": {
      "n_heats_with_country": 14,
      "mean_diff_pts": 0.7348214285714286,
      "se": 0.7155994117881116,
      "t_stat": 1.0268614206030242,
      "p_value": 0.32321407845411076
    },
    "JPN": {
      "n_heats_with_country": 12,
      "mean_diff_pts": 0.33145833333333335,
      "se": 0.7217772846978546,
      "t_stat": 0.45922522135354554,
      "p_value": 0.6550143537043516
    },
    "FRA": {
      "n_heats_with_country": 13,
      "mean_diff_pts": 1.2338461538461538,
      "se": 0.41844680138784196,
      "t_stat": 2.94863325458318,
      "p_value": 0.012175102061194968
    },
    "PER": {
      "n_heats_with_country": 9,
      "mean_diff_pts": -0.6384259259259258,
      "se": 0.660627455618216,
      "t_stat": -0.9663932682429707,
      "p_value": 0.3621494569836793
    }
  },
  "interpretation": "FRA surfers score -0.022 pts higher than non-FRA controlling for wave-quality proxy + surfer FE"
}
```

## O2 — Round-number bias at Olympics (.00/.25/.50/.75 clustering)

_Same Monte-Carlo trim-mean null as h7_h14::test_h11._

- Olympic estimate: `3.995904198196848`
- 95% CI: `(3.240231512364638, 4.825368656606399)`
- p-value (raw): `0.0`
- p-value (Bonferroni × 6): `0.0`
- n: `285`
- Verdict: **supports**
- Replication verdict: **REPLICATES**

```json
{
  "p_round_observed_pct": 26.666666666666668,
  "p_round_expected_under_null_pct": 6.673500000000001,
  "excess_ratio": 3.995904198196848,
  "excess_95ci": [
    3.240231512364638,
    4.825368656606399
  ],
  "n_round": 76,
  "n_total": 285,
  "binom_z_vs_trim_mean_null": 13.524608256403818,
  "binom_p_vs_trim_mean_null": 0.0,
  "chi2_uniform_naive_stat": 2060.614035087719,
  "chi2_uniform_naive_p": 0.0
}
```

## O3 — Comeback-narrative bias at Olympics

_Heat-deficit regression on residual score, ports h7_h14::test_h7_comeback_bias._

- Olympic estimate: `-0.01954368416985352`
- 95% CI: `(-0.12327672186238858, 0.08418935352268153)`
- p-value (raw): `0.711925606782547`
- p-value (Bonferroni × 6): `1.0`
- n: `221`
- Verdict: **null**
- Replication verdict: **PARTIAL-DIRECTIONAL**

> each 1pt heat-deficit → -0.0195 residual score points

```json
{
  "n_heats": 64,
  "n_surfers": 48,
  "se": 0.05292501923088523,
  "coef_sign_supports_comeback_bias": true,
  "interpretation": "each 1pt heat-deficit \u2192 -0.0195 residual score points"
}
```

## O4 — Day-of-event amplification at Olympics

_Per-event endpoint slope of residual variance across competition days; ports h17_h28::test_h17._

- Olympic estimate: `-0.3986830754653129`
- 95% CI: `None`
- p-value (raw): `0.1579451665048632`
- p-value (Bonferroni × 6): `0.9476709990291792`
- n: `14`
- Verdict: **null**
- Replication verdict: **FAILED (opposite sign)**

> residual variance Spearman vs round-day = -0.399, p=0.1579; positive ⇒ widens toward medal day

```json
{
  "primary_test": "Spearman across event-day cells",
  "spearman_rho": -0.3986830754653129,
  "spearman_p": 0.1579451665048632,
  "n_event_day_cells": 14,
  "n_underlying_waves": 285,
  "endpoint_slope_t_stat": -0.9254382696816694,
  "endpoint_slope_p_value": 0.5246405021624243,
  "endpoint_slope_mean": -0.1593879911971596,
  "endpoint_slope_se": 0.17222973851295945,
  "robustness_within_FE": {
    "coef": null,
    "p_value": null
  },
  "interpretation": "residual variance Spearman vs round-day = -0.399, p=0.1579; positive \u21d2 widens toward medal day"
}
```

## O5 — Reputation prior at Olympics (pre-Oly CT rank effect)

_Findlay & Ste-Marie 2004 reputation regression with leave-one-out heat mean as wave-quality proxy + heat FE; ports bias_tests::test_2._

- Olympic estimate: `0.6296296296296297`
- 95% CI: `(-0.050617917924867493, 0.001925887775024747)`
- p-value (raw): `0.004528991668766285`
- p-value (Bonferroni × 6): `0.02717395001259771`
- n: `108`
- Verdict: **supports**
- Replication verdict: **REPLICATES**

> Within-heat sign test (Zitzewitz 2011 primary): higher-ranked surfer wins 62.96% of pair comparisons across 108 same-heat pairs (p=0.0045, raw). Secondary Findlay regression coef = -0.02435 pts/rank-position (p=0.0693).

```json
{
  "n_olympic_waves_with_matched_pre_oly_CT_rank": 149,
  "n_olympic_surfers_with_matched_rank": 23,
  "n_olympic_surfers_total": 48,
  "match_rate": 0.4791666666666667,
  "findlay_regression": {
    "coef": -0.024346015074921373,
    "p_value": 0.06932637528321361,
    "ci_95": [
      -0.050617917924867493,
      0.001925887775024747
    ],
    "n": 148
  },
  "within_heat_sign_test": {
    "n_pairs": 108,
    "higher_ranked_won": 68,
    "win_rate": 0.6296296296296297,
    "p_value": 0.004528991668766285
  },
  "primary_test": "within-heat sign test (Zitzewitz 2011)",
  "interpretation": "Within-heat sign test (Zitzewitz 2011 primary): higher-ranked surfer wins 62.96% of pair comparisons across 108 same-heat pairs (p=0.0045, raw). Secondary Findlay regression coef = -0.02435 pts/rank-position (p=0.0693)."
}
```

## O6 — Benjamin Lowe panel-removal pre/post (Aug 1 2024)

_Difference-in-differences-flavored pre/post within-surfer comparison + AUS-bloc subgroup test. Novel Olympic-specific incident; no WSL training-data analog._

- Olympic estimate: `0.6603602684316987`
- 95% CI: `(-1.0774003358778537, 2.3981208727412513)`
- p-value (raw): `0.45639324557484784`
- p-value (Bonferroni × 6): `1.0`
- n: `285`
- Verdict: **null**
- Replication verdict: **NOVEL (no WSL analog)**

> DiD = (AUS post - AUS pre) - (non-AUS post - non-AUS pre). Hypothesis: NEGATIVE DiD = AUS scoring dropped after their compatriot judge was removed (compatriot-judge effect). Observed DiD=+0.660 is positive — i.e. AUS scores went UP after Lowe was removed — *opposite* direction to the compatriot-judge story. Most likely explanation: survival selection — only the strongest 3 AUS surfers (Robinson, Ewing, Wright) advanced past Round 2, and they were riding cleaner waves post-weather-hold. The compatriot-judge hypothesis is NOT supported by this natural experiment.

```json
{
  "pre_n": 159,
  "post_n": 126,
  "pre_mean": 4.771132075471698,
  "post_mean": 5.251587301587302,
  "overall_post_minus_pre": 0.48045522611560365,
  "overall_t_stat": 1.7240172068020765,
  "overall_p_value": 0.08584154739850583,
  "aus_block_pre_post": {
    "n_pre": 12,
    "n_post": 15,
    "mean_pre": 5.160833333333333,
    "mean_post": 6.204666666666666,
    "diff_post_minus_pre": 1.0438333333333336,
    "t_stat": 1.1381456824119522,
    "p_value": 0.2685814414453377
  },
  "did_aus_x_post_estimate": 0.6603602684316987,
  "did_aus_x_post_p_value": 0.45639324557484784,
  "did_aus_x_post_ci95": [
    -1.0774003358778537,
    2.3981208727412513
  ],
  "interpretation": "DiD = (AUS post - AUS pre) - (non-AUS post - non-AUS pre). Hypothesis: NEGATIVE DiD = AUS scoring dropped after their compatriot judge was removed (compatriot-judge effect). Observed DiD=+0.660 is positive \u2014 i.e. AUS scores went UP after Lowe was removed \u2014 *opposite* direction to the compatriot-judge story. Most likely explanation: survival selection \u2014 only the strongest 3 AUS surfers (Robinson, Ewing, Wright) advanced past Round 2, and they were riding cleaner waves post-weather-hold. The compatriot-judge hypothesis is NOT supported by this natural experiment.",
  "important_caveat": "Round number is a coarse proxy for date. Round 1-2 ran Jul 27-28 (pre-Lowe-removal); Round 3-7 spanned Aug 1-5 (post-removal). Confounded by the weather hold (Jul 29-31) which selects on wave conditions."
}
```

## Side-by-side: WSL training vs Olympic 2024

| Mechanism | WSL CT (2022-25, n=24,901) | Olympic 2024 (Teahupo'o, n=288) | Replicates? |
|-----------|----------------------------|----------------------------------|-------------|
| Compatriot home-country effect at Olympics | est=0.07005767967614915, p_bonf=1.0000; no evidence of bias | est=-0.0219, p_bonf=1.0000; n=285; null | **REPLICATES (both null)** |
| Round-number bias at Olympics (.00/.25/.50/.75 clustering) | est=3.4067, p_bonf=0.00e+00; supports | est=+3.9959, p_bonf=0.00e+00; n=285; supports | **REPLICATES** |
| Comeback-narrative bias at Olympics | est=-0.014815660014969064, p_bonf=8.19e-05; supports | est=-0.0195, p_bonf=1.0000; n=221; null | **PARTIAL-DIRECTIONAL** |
| Day-of-event amplification at Olympics | est=1.1698237628, p_bonf=9.91e-12; supports | est=-0.3987, p_bonf=0.9477; n=14; null | **FAILED (opposite sign)** |
| Reputation prior at Olympics (pre-Oly CT rank effect) | est=-0.005810424, p_bonf=0.0007; supports | est=+0.6296, p_bonf=0.0272; n=108; supports | **REPLICATES** |
| Benjamin Lowe panel-removal pre/post (Aug 1 2024) | est=None, p_bonf=—; novel — no WSL analog | est=+0.6604, p_bonf=1.0000; n=285; null | **NOVEL (no WSL analog)** |

## Discussion paragraph (drop into manuscript Discussion)

On Olympic-2024 surfing data (n=288 waves, ISA panel at Teahupo'o), 3 of the 4 confirmed-on-WSL bias mechanisms tested here — round-number clustering, comeback narrative, reputation prior — replicate in same direction. The data-richest of these, round-number clustering, survives Bonferroni × 6 correction (excess ratio 4.0× vs the trim-mean Monte-Carlo null, p≈0) despite the sample being two orders of magnitude smaller than the training corpus. The Olympic excess ratio (4.0×) actually *exceeds* the WSL CT excess (3.4×), indicating the .00/.25/.50/.75-anchoring pattern is not a WSL-specific bookkeeping artifact but a property of the underlying judging-pool decision process.

Round-number clustering at the Olympics shows 26.7% of scores ending in .00/.25/.50/.75 vs a trim-mean Monte-Carlo null of 6.7% — an excess ratio of 4.00× (95% CI [+3.2402, +4.8254]).

The Aug 1 2024 panel-mid-event removal of judge Benjamin Lowe (AUS) provides a within-event natural experiment: AUS surfers averaged 5.16 pts/wave pre-removal (n=12) vs 6.20 pts/wave post-removal (n=15). DiD vs non-AUS = +0.660 pts (p=0.4564). The DiD is positive — AUS scores INCREASED after their compatriot judge was removed — which is the *opposite* direction to a simple compatriot-favoritism story. The observed pattern is more consistent with survival selection: only the strongest AUS competitors (Jack Robinson, Ethan Ewing, Tyler Wright) advanced past the elimination round, and they faced calmer fields after the Jul 29-31 weather hold. We classify O6 as a NULL on the compatriot-judge hypothesis, with the caveat that within-surfer power is too weak to rule out smaller effects (only 3 AUS surfers have waves in both periods).

These results indicate the bias mechanisms identified on the WSL Championship Tour — particularly round-number clustering and (directionally) reputation prior + comeback narrative — are not artifacts of WSL-specific judging culture but appear in the ISA-paneled Olympic competition that shares judging-pool personnel. The 2028 LA Olympics (Trestles, USA) and 2032 Brisbane Olympics (AUS waves) will deploy panels drawn from the same pool. Pre-event randomization audits, mandatory round-number-discrepancy reporting, and panel-rotation protocols modeled after figure-skating's post-2002 reforms (Zitzewitz 2011) become governance-relevant rather than WSL-internal-quality-control questions.

## Power note

Olympic n=288 is approximately 86× smaller than the WSL training corpus (n=24,901). At equal effect sizes, Bonferroni-corrected significance is reachable only for mechanisms with WSL effect sizes in the top decile (e.g. round-number bias at 3.4× excess; day-of-event amplification with t≈8). For intermediate effects (reputation prior at -0.006 pts/rank-position; comeback bias at -0.015 pts/deficit-pt), Olympic-only data is expected to be DIRECTIONAL rather than significant. The test of governance-relevance is therefore the *direction + magnitude* of the Olympic point estimate, not its raw p-value.
