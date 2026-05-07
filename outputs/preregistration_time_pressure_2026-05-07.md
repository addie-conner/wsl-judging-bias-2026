# Pre-Registration: Time-Pressure Mechanisms of Round-Number Anchoring in WSL Judging

**Author**: Addie Conner (independent; Chorus Research)
**Time-stamped**: 2026-05-07 (UTC)
**Location of canonical copy**: `wsl-judging-bias-2026/outputs/preregistration_time_pressure_2026-05-07.md`
**Git commit hash at time of writing**: (computed at SHA-lock step — sealed before any confirmatory analysis is run)
**Status**: LOCKED before confirmatory phase. Any deviation must be reported in Methods or Limitations.

---

## Background: discovery analysis (post-hoc, exploratory)

A discovery analysis was conducted on 2026-05-06 in response to a hypothesis volunteered by a former WSL operations contact (J. Suhar, personal communication, 2026-05-06): that round-number anchoring in surf judging is driven by judge time-pressure. The discovery analysis tested four time-pressure proxies on the merged corpus of 49,010 individual judge-score decisions across 2022–2026 men's + women's Championship Tour. Results:

| Proxy | Direction predicted | Result | Effect size on 31% baseline |
|---|---|---|---|
| Wave-density (log seconds since prev wave) | Negative coef | coef −0.026, p = 0.005 | ~1.7 pp Q1↔Q4 |
| Fatigue (heat-N within event) | Positive coef | coef +0.0029, p < 0.001 | ~1.8 pp Q1↔Q4 |
| End-of-heat (last 3 min) | Higher anchoring | 24.0% vs 33.2%, −9.2 pp, p ≈ 0 | ✗ direction reversed |
| Combined logit (with judge-nat FE) | All three | log_gap p = 0.058, EOH p ≈ 0 (wrong sign), fatigue p < 0.001, pseudo-R² = 0.005 | mixed |

**Output saved**: `outputs/time_pressure_anchoring_2026-05-06.json`.

The discovery analysis was post-hoc, exploratory, single-operationalization, and uncorrected for multiple comparisons. The findings are reported in Paper 1's mechanism section as such. **This pre-registration covers a confirmatory analysis on these mechanisms** with predefined hold-out, alternative operationalizations, multiple-comparison correction, and sensitivity tests — sealed before any further analysis is run.

---

## Hypotheses (confirmatory)

### H1 — Wave-density / inter-wave-gap effect
**Claim**: Anchoring rate is monotonically decreasing in time-since-previous-wave. Specifically, the logit coefficient on log(seconds since prev wave) on whole-anchor (score ends in .0) is negative.
**Test**: Logit `whole_anchor ~ log_gap_seconds + C(judge_nat) + C(event_id)`. Outcome: coefficient on `log_gap_seconds`.
**Significance threshold**: BH-FDR-corrected q < 0.05 across the 3 primary tests.
**Falsification**: if coefficient is positive OR p > 0.05 after FDR correction, H1 is rejected.

### H2 — Fatigue (heat-sequence within event)
**Claim**: Anchoring rate is monotonically increasing in heat-sequence-within-event. The logit coefficient on heat_seq is positive.
**Test**: Logit `whole_anchor ~ heat_seq + C(judge_nat) + C(event_id)`. Outcome: coefficient on `heat_seq`.
**Significance threshold**: BH-FDR q < 0.05.
**Falsification**: coefficient ≤ 0 OR q > 0.05.

### H3 — End-of-heat reversal (the surprise)
**Claim**: Anchoring rate is *lower* in the final 3 minutes of a heat than in the preceding minutes. This claim explicitly contradicts the original time-pressure hypothesis and was discovered post-hoc; the confirmatory test is whether the reversal replicates.
**Test**: Two-proportion z-test of whole_anchor rate in last-3-min vs not, plus logit `whole_anchor ~ end_of_heat + C(judge_nat) + C(event_id)`.
**Significance threshold**: BH-FDR q < 0.05; effect size ≥ 5 pp absolute difference.
**Falsification**: rate difference ≤ 5 pp OR coefficient sign flips.

### H4 — Magnitude comparison
**Claim**: All three time-pressure effects, even if statistically detectable, are *substantially smaller* than the round-number anchoring baseline. Specifically: the largest absolute pp shift across all three operationalizations is < 25% of the anchoring excess (anchoring excess = 31% − 10% null = 21 pp; 25% threshold = 5.25 pp).
**Test**: Direct measurement of max absolute pp shift across H1, H2, H3 quartile distributions.
**Significance threshold**: this is a magnitude claim, not a null-hypothesis test. Reported as effect-size summary.
**Falsification**: any single operationalization produces a shift ≥ 5.25 pp **AND** in the predicted direction (note: the H3 reversal qualifies but in a direction that *strengthens* the claim that time-pressure is not the primary driver; the falsification is restricted to predicted-direction shifts of that magnitude).

---

## Hold-out replication

The discovery analysis used 2022–2026. The confirmatory hold-out is the **2026 season only** (men's + women's CT through May 2026).

- Discovery sample: judges.parquet records where `year ∈ {2022, 2023, 2024, 2025}` matched against heats.parquet (estimated n ≈ 32,000 judge-score decisions)
- Hold-out sample: judges.parquet records where `year == 2026` matched against heats.parquet (estimated n ≈ 17,000 judge-score decisions)
- The discovery and hold-out samples are disjoint by construction (split on `year`).
- **All three confirmatory tests must replicate on the hold-out for the original direction-of-effect claim to be considered confirmed.**

---

## Sensitivity / robustness analyses (pre-specified)

These are run on the full 2022–2026 corpus after the hold-out replication, and reported as sensitivity bounds:

### S1 — End-of-heat threshold
The original 3-minute threshold for "end-of-heat" is one of many defensible choices. Re-run H3 at thresholds: **60, 120, 180, 300 seconds**. Report effect size at each.

### S2 — Alternative wave-density operationalizations
Re-run H1 with: (a) seconds since previous wave (current), (b) mean inter-wave gap across the heat, (c) count of waves in the prior 60 seconds. Report each.

### S3 — Alternative fatigue operationalizations
Re-run H2 with: (a) heat-N-within-event (current), (b) heat-position-within-comp-day where derivable, (c) days-since-event-start.

### S4 — Fixed-effects robustness
Re-run H1, H2, H3 with each of: (a) no FE, (b) judge-nationality FE only, (c) event_id FE, (d) judge × event FE.

### S5 — Outlier robustness
Drop top 1% of heats by absolute deviation from the corpus mean anchoring rate. Re-run H1, H2, H3.

---

## Multiple-comparison correction

Primary tests are H1, H2, H3 (3 tests). Apply Benjamini-Hochberg FDR at q = 0.05 across the three. H4 is a magnitude claim, not subject to FDR. The 4 sensitivity-analysis families (S1–S5, ~16 tests) are reported as sensitivity bounds, not as primary-significance tests.

---

## What we will NOT do post-hoc

- Will not introduce new hypotheses about time-pressure mechanisms outside H1–H4.
- Will not introduce new operationalizations beyond S1–S5.
- Will not change significance thresholds or correction methods after seeing results.
- Will not re-define hold-out after seeing it.
- Will not selectively report only the supportive sensitivity analyses — all of S1–S5 are reported.

---

## Reproducibility commit

This file's git commit hash at time of seal is the canonical pre-registration timestamp. Confirmatory analysis script: `scripts/test_time_pressure_anchoring_confirmatory.py` (to be written **after** this file is committed).

Output JSON: `outputs/time_pressure_confirmatory_2026-05-07.json` (to be produced).

Manuscript: `manuscript/paper4_time_pressure.md` (companion paper).

---

## Summary table for the manuscript

| Hypothesis | Discovery (2022–2025) | Confirmatory (2026 hold-out) | Verdict |
|---|---|---|---|
| H1 wave-density | coef −0.026, p = 0.005 | (to be filled in by confirmatory script) | (pending) |
| H2 fatigue | coef +0.0029, p < 0.001 | (pending) | (pending) |
| H3 end-of-heat reversal | −9.2 pp, p ≈ 0 | (pending) | (pending) |
| H4 magnitude bound | max ~9 pp (H3 only); H1/H2 ~2 pp | (filled from confirmatory) | (pending) |
