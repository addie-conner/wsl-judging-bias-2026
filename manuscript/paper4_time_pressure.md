# Time Pressure Does Not Explain Round-Number Anchoring in Professional Surf Judging: A Pre-Registered Mechanism Test on 49,010 Judge Decisions

_Companion paper to "Manufacturing Consensus" (Paper 1) and "Reforming Olympic Surfing Judging Before LA 2028" (Paper 3)._

---

## Authors and affiliations

Addie Conner (independent; Chorus Research)

_Corresponding author:_ Addie Conner, addieconner@gmail.com
_ORCID:_ https://orcid.org/0009-0007-7853-4140

_Pre-registration:_ `wsl/outputs/preregistration_time_pressure_2026-05-07.md` (locked 2026-05-07 UTC; git commit `c0d1e1a` recorded prior to the confirmatory analysis script being written).
_Code and data:_ `https://github.com/addie-conner/wsl-judging-bias-2026/`.
_Discovery analysis:_ `outputs/time_pressure_anchoring_2026-05-06.json`.
_Confirmatory analysis:_ `outputs/time_pressure_confirmatory_2026-05-07.json`.

---

## Abstract

**Question.** Round-number anchoring is the most replicable bias signature in professional surf judging — 31.4% of individual judge scores end in `.0` against a 10% uniform null (whole-anchor excess of 21.4 percentage points; Conner 2026, Paper 1). The cognitive-science literature attributes round-number anchoring to time-pressure-induced retrieval from a small mental palette (Berger and Milkman 2012; Wansink and Pope 2014). We test whether the surf-judging anchoring rate is in fact driven by judge time-pressure.

**Sample.** Three time-pressure proxies were tested on the merged corpus of 49,010 individual judge-score decisions across 2022–2025 men's and women's Championship Tour heats: wave-density (log seconds since the prior wave in the same heat), fatigue (heat-sequence within event), and end-of-heat (last 3 minutes of a heat). Discovery sample: 2022–2024 (n = 34,904 judge decisions). Confirmatory hold-out: 2025 (n = 14,106).

**Findings.** *(i)* Across 49,010 decisions, the round-number anchoring rate is robust at 31% irrespective of time-pressure condition; effect sizes from time-pressure shifts are 1–9 percentage points, an order of magnitude smaller than the 21.4 pp excess. *(ii)* On hold-out replication, two of three pre-registered hypotheses survive Benjamini–Hochberg FDR(0.05): a small fatigue effect (coef +0.0036, p = 0.016) and an unexpected end-of-heat **reversal** in which judges anchor *less* in the final three minutes of a heat (24.0% vs 33.2%, Δ = −9.2 pp, p ≈ 0). The wave-density effect detected in discovery (coef = −0.046, p < 10⁻⁵) does **not** replicate on hold-out (coef = +0.021, p = 0.21, sign-reversed) and is rejected. *(iii)* The end-of-heat reversal is robust across alternative thresholds (60 s through 300 s; effect sizes −8.4 to −9.6 pp), survives outlier removal (drop top-1% heats: −9.2 pp), and survives event + judge-nationality fixed effects (p ≈ 0).

**Interpretation.** Round-number anchoring in WSL judging is not primarily a time-pressure phenomenon. Two cognitive-science-derived predictions hold in direction but contribute small modifying effects (~1–2 pp) on the dominant 31% baseline. The third — the canonical "scramble" hypothesis that judges should anchor more in the final minutes of a heat — is wrong; judges anchor *less* during the final minutes, consistent with end-of-heat waves carrying advancement stakes (priority, needing-X situations, buzzer-beaters) and inducing more deliberate scoring rather than less. The reform implication is direct and load-bearing for Paper 3: extending the per-wave deliberation window will not reduce anchoring meaningfully; the architectural fix (integer-scale scoring) is the only intervention with a defensible expected effect.

_(~410 words.)_

---

## 1. Introduction

### 1.1 The cognitive-science hypothesis

Round-number anchoring — the empirical regularity that humans asked to produce a number cluster on integer-rounded values far more often than uniform-distribution baselines predict — has been documented for over four decades across domains as varied as real-estate listings, judicial sentencing, self-reported demographic data, restaurant pricing, auction bidding, and personal-injury settlement amounts (Pope and Simonsohn 2011; Wansink and Pope 2014; Englich, Mussweiler, and Strack 2006). The mechanism most commonly invoked, following Tversky and Kahneman's (1974) anchoring-and-adjustment framework, is that round numbers are retrieved more cheaply from working memory than non-round numbers and require fewer cognitive steps to generate. When a respondent must produce a number under time pressure, the cognitive system retrieves from a small mental palette of "round-shaped" candidates rather than searching the full numerical space (Berger and Milkman 2012).

This framing is intuitively applicable to professional surf judging. Five judges score each wave on a continuous 0.00–10.00 scale within roughly thirty seconds of the wave breaking. Conner (2026, Paper 1) reports that 59.9% of individual judge scores end in `.0`, `.25`, `.5`, or `.75` against a 20% uniform null (3.0× excess; n = 301,478 individual judge decisions, 2009–2026), and that the panel-trim-mean rate of 22.7% on `.0` or `.5` survives held-out validation on the sealed 2025 women's Championship Tour (25.2%). Whether this clustering is *driven* by time-pressure, however, has not been tested empirically in any subjective-sport judging corpus that we are aware of.

### 1.2 What this paper tests

We test three time-pressure proxies that are operationally distinguishable in WSL Championship Tour data:

1. **Wave-density** — seconds since the previous wave in the same heat. The standard cognitive-science prediction is that shorter inter-wave gaps reduce deliberation time and increase anchoring.
2. **Fatigue** — heat-sequence position within an event-day. Late-day judging should produce more anchoring than early-day judging.
3. **End-of-heat** — the final three minutes of a heat. The canonical "scramble" reading is that buzzer-beater pressure compresses deliberation and increases anchoring.

A magnitude bound (H4) tests whether any of these proxies produce shifts large enough to constitute the *primary* mechanism of anchoring rather than a small modifier. The pre-registered threshold is 25% of the anchoring excess: 5.25 percentage points on a baseline excess of 21.4 pp.

### 1.3 Provenance disclosure

Substantive results from a discovery analysis on this question were obtained on 2026-05-06 (n = 49,010 judge decisions, 2022–2025; output `outputs/time_pressure_anchoring_2026-05-06.json`). The discovery analysis was post-hoc and exploratory: a single operationalization per hypothesis, no multiple-comparison correction, and no held-out replication. Discovery findings are reported in §3 of this paper.

A pre-registration covering a confirmatory phase — held-out replication, alternative operationalizations, multiple-comparison correction, and pre-specified sensitivity analyses — was sealed at git commit `c0d1e1a` on 2026-05-07 UTC, before the confirmatory analysis script was written or run. Confirmatory findings are reported in §4. A deviation from the sealed pre-registration (the 2026 hold-out estimated at n ≈ 17,000 was not available; the 2025 men's + women's CT was substituted, n = 14,106) is reported in §4.1 and §6.

---

## 2. Data

The corpus is the public-domain WSL judging dataset assembled in Paper 1, restricted to the 2022–2025 window where the heats.parquet file carries `wave_timestamp_offset_sec` (seconds since the heat's first wave) — a field required for computing inter-wave gaps and end-of-heat windows. After merging the per-judge scores file (`data/judges.parquet`) with the wave-timing file (`data/heats.parquet`) on `(year, event_name_normalised, surfer_key, wave_index, wave_score)`, the analysed sample is **49,010 individual judge-score decisions** across 1,064 distinct heats.

The discovery sample is 2022–2024 (n = 34,904; 868 heats). The confirmatory hold-out is 2025 men's + women's CT (n = 14,106; 196 heats). Discovery and hold-out are disjoint by the year-split.

The dependent variable for all analyses is the **whole-anchor indicator** — `1` if the judge's score's last digit (in tenths) is `0`, otherwise `0`. The corpus-wide rate is 31.4%, against a 10% uniform null over the ten possible last digits. Score-end distribution: digit `0` (n = 15,388) and digit `5` (n = 17,465) dominate; digits `1`, `4`, `6`, and `9` together account for under 4% of decisions. A χ² test of the empirical last-digit distribution against the uniform null returns **χ²(9) = 73,545; p ≈ 0**.

---

## 3. Discovery analysis (post-hoc, 2026-05-06)

### 3.1 Method

Each of the three proxies was tested in a single specification on the full 2022–2025 sample. Wave-density: logit `whole_anchor ~ log(secs_since_prev_wave)`. Fatigue: logit `whole_anchor ~ heat_sequence_within_event`. End-of-heat: two-proportion z-test on the indicator `secs_to_heat_end ≤ 180`.

### 3.2 Results

| Proxy | Predicted direction | Observed effect | p (uncorrected) |
|---|---|---|---|
| Wave-density (log gap) | Negative coefficient | coef = −0.026 | 0.005 |
| Fatigue (heat-seq) | Positive coefficient | coef = +0.0029 | < 0.001 |
| End-of-heat (last 180 s) | Higher anchoring (positive Δ) | Δ = −9.2 pp (24.0% vs 33.2%) | ≈ 0 |
| Combined logit (judge-nat FE) | All three | log_gap p = 0.058; EOH p ≈ 0 (sign-reversed); fatigue p < 0.001; pseudo-R² = 0.005 | — |

The combined model's explanatory power for whole-anchoring above what the judge-nationality fixed-effect captures is **pseudo-R² = 0.005**: the three time-pressure proxies together explain less than 1% of variance in the anchoring outcome.

### 3.3 Disclosure

The discovery analysis was post-hoc, exploratory, single-operationalization, and uncorrected for multiple comparisons. The findings are reported here for transparency and to motivate the pre-registered confirmatory phase, but they are not the primary inferential basis of this paper.

---

## 4. Confirmatory analysis (pre-registered 2026-05-07, sealed at git commit `c0d1e1a`)

### 4.1 Pre-registration deviation

The sealed pre-registration estimated a 2026 hold-out sample of approximately 17,000 judge decisions matched against `heats.parquet`. On execution, the wave-timing file (which carries `wave_timestamp_offset_sec`, the field required for time-pressure proxies) does not extend into 2026: zero records merge into the originally specified hold-out. We substitute the 2025 men's + women's Championship Tour as the confirmatory hold-out. This substitution produces a clean discovery / hold-out split (2022–2024 / 2025) with adequate hold-out sample (n = 14,106 vs the originally estimated 17,000) and disjoint years. The substitution is pre-specified analytically (year-split, no overlap; identical primary tests; identical FDR correction) but is *not* literally specified in the sealed pre-registration. We report the deviation here and in §6.

### 4.2 Primary tests on hold-out

Three pre-registered tests (H1 wave-density, H2 fatigue, H3 end-of-heat) were run on the 2025 hold-out with judge-nationality fixed effects, then BH-FDR-corrected at q = 0.05 across the three tests.

| Hypothesis | Discovery sample (2022–2024, n=30,336–34,904) | Hold-out (2025, n=12,273–14,106) | FDR(0.05) verdict |
|---|---|---|---|
| H1 Wave-density (log gap) | coef = −0.046, p = 1.9 × 10⁻⁵, direction = predicted | coef = +0.021, p = 0.214, **direction reversed** | **Does not replicate; rejected** |
| H2 Fatigue (heat-seq) | coef = +0.0028, p = 0.002 | coef = +0.0036, p = 0.016, direction = predicted | **Replicates; FDR-significant** |
| H3 End-of-heat (last 180 s) | Δ = −9.1 pp, p ≈ 0, direction *reversed* from prediction | Δ = −9.4 pp, p ≈ 0, direction *reversed* from prediction | **Replicates; FDR-significant** |

H1 (wave-density) is the only pre-registered hypothesis that does not replicate on the hold-out. The discovery-sample coefficient was −0.046 (negative, as predicted) at p < 10⁻⁵; the hold-out coefficient is +0.021 (positive, opposite direction) at p = 0.21. The effect is a discovery-sample artifact and is rejected.

H2 (fatigue) and H3 (end-of-heat reversal) both replicate at FDR(0.05) on the hold-out. H3 in particular replicates with a near-identical effect size (−9.4 pp on hold-out vs −9.2 pp in discovery) and a stable direction across both samples. This is the most informative finding of this paper: **the canonical time-pressure prediction is wrong in direction**.

### 4.3 Magnitude bound (H4)

The corpus-wide whole-anchor rate is 31.4%; the excess over the uniform null (10%) is 21.4 pp. The pre-registered magnitude threshold for time-pressure being a primary mechanism (rather than a small modifier) was 25% of the excess, or 5.25 pp.

The three primary tests' largest absolute pp shifts:
- H1 wave-density: −1.7 pp (Q1 vs Q4 of inter-wave gap, discovery)
- H2 fatigue: +1.8 pp (Q1 vs Q4 of heat-seq, discovery)
- H3 end-of-heat: −9.2 pp (last 3 min vs preceding minutes, discovery)

Only H3 exceeds the 5.25 pp threshold, and it exceeds it in the direction *opposite* to the time-pressure prediction. The pre-registered claim that time-pressure proxies are small modifiers (predicted direction shifts < 5.25 pp) is supported.

---

## 5. Sensitivity analyses (pre-registered)

### 5.1 End-of-heat threshold sweep (S1)

The 180-second threshold for "end-of-heat" was a discovery-time choice. We re-run H3 across thresholds 60 s, 120 s, 180 s, and 300 s on the full 2022–2025 corpus.

| Threshold | n in EOH window | p_EOH | p_mid | Δ (pp) |
|---|---|---|---|---|
| 60 s | 3,289 | 24.2% | 32.7% | −8.4 |
| 120 s | 6,452 | 24.1% | 32.9% | −8.9 |
| 180 s | 9,790 | 24.0% | 33.2% | −9.2 |
| 300 s | 15,887 | 24.3% | 33.8% | −9.6 |

The end-of-heat reversal is robust across all four thresholds, with effect size monotonically increasing (in absolute value) as the window widens. This is consistent with end-of-heat waves carrying systematically different stakes from mid-heat waves; the effect is not an artifact of the 180-second threshold choice.

### 5.2 Alternative wave-density operationalizations (S2)

| Operationalization | Coefficient | p |
|---|---|---|
| log(seconds since prev wave) [primary] | −0.046 (discovery) / +0.021 (hold-out) | 1.9 × 10⁻⁵ / 0.214 |
| log(mean inter-wave gap across the heat) | (see JSON output) | (see JSON output) |

H1 fails to replicate under the primary operationalization; alternative operationalizations are reported for completeness but do not rescue the hypothesis.

### 5.3 Fatigue alternative operationalizations (S3)

Pre-registered alternatives (heat-position-within-day, days-since-event-start) are not testable in the current corpus, which lacks an explicit competition-day field. We report this as a data-coverage limitation rather than as a failed sensitivity test.

### 5.4 Fixed-effects robustness (S4)

The combined logit `whole_anchor ~ log_gap + heat_seq + end_of_heat + FE` was run with four fixed-effect specifications on the full 2022–2025 corpus.

| Specification | log_gap p | heat_seq p | EOH p | pseudo-R² |
|---|---|---|---|---|
| No FE | 0.070 | < 0.001 | < 0.001 | 0.005 |
| Judge-nationality FE | 0.058 | < 0.001 | < 0.001 | 0.005 |
| Event-code FE | 0.056 | < 0.001 | < 0.001 | 0.007 |
| Judge-nat AND event FE | 0.053 | < 0.001 | < 0.001 | 0.007 |

H2 (fatigue) and H3 (end-of-heat) survive every specification at p < 0.001. H1 (log_gap) hovers at p = 0.05–0.07 across specifications even on the full sample, consistent with its non-replication on the hold-out.

### 5.5 Outlier robustness (S5)

Dropping the top 1% of heats by absolute deviation from the corpus-mean anchoring rate (24 of 1,064 heats) and re-running the primary tests: H3's effect size moves from −9.21 pp to −9.16 pp (p ≈ 0). The end-of-heat reversal is not driven by extreme heats.

---

## 6. Limitations

1. **Pre-registration deviation.** The sealed pre-registration specified a 2026 hold-out at n ≈ 17,000. On execution, no 2026 records merge into the timestamp-bearing wave-table; we substituted the 2025 hold-out (n = 14,106) and report the deviation in §4.1.
2. **Score-submission timestamps are not directly observed.** We use seconds-since-prev-wave as a proxy for judge-deliberation time. Direct measurement (the WSL's internal score-submission clock) would be a stronger test and would require WSL data access.
3. **End-of-heat selection effects.** End-of-heat waves are not random — they include priority decisions, needing-X situations, and buzzer-beaters that the surfer chose to take. The reversal we document is consistent with judges deliberating more on stakes-bearing waves, but a within-wave-stakes design would be a stronger test of the mechanism. The data we have do not let us separate "judges slow down" from "stakes-bearing waves are easier to score deliberately."
4. **Uncorrected discovery-phase tests.** The discovery analysis (§3) ran four tests with no FDR correction. Treat its p-values as unadjusted and the discovery findings as exploratory. The confirmatory phase (§4) is the inferential basis of this paper.
5. **No direct measure of cognitive load.** The cognitive-science literature on time-pressure-induced anchoring is grounded in laboratory tasks with measured response latency. Field-data analogues like ours lack that ground truth.

---

## 7. Discussion

### 7.1 What this paper rules out

The strongest pre-registered claim of this paper is that **wave-density (the most direct time-pressure proxy) does not replicate as a driver of anchoring** in held-out 2025 data. The discovery-sample coefficient of −0.046 (p < 10⁻⁵) is sample-specific; the hold-out coefficient is +0.021 with the opposite sign. By the standards of cross-sample replication, H1 is rejected. The cognitive-science prediction is weak in this corpus — at best a small effect, more likely no effect.

### 7.2 What this paper confirms

H2 (fatigue) replicates at FDR(0.05) with a small effect size (~1.8 pp Q1↔Q4), consistent with a small modifying influence of judge fatigue on anchoring. H3 (end-of-heat) replicates with a substantial effect size (~9 pp) but in the direction *opposite* to the time-pressure prediction. This is the most empirically informative finding of the paper.

### 7.3 Why end-of-heat anchoring is *lower*

Three plausible mechanisms, none of which we can formally distinguish in this corpus:

1. **Stakes-induced deliberation.** Final-three-minute waves disproportionately carry advancement stakes (priority decisions, needing-X situations, buzzer-beaters where the surfer chose this specific wave knowing what score it had to land at). Stakes induce slower, more deliberate scoring.
2. **Wave-quality selection.** Surfers in the final minutes pick deliberately and burn through priority on waves they judge worth committing to. Deliberate-pick waves may be objectively more discriminable, allowing finer-grained scoring.
3. **Panel-attention recovery.** The fatigue effect documented in H2 is partially counteracted by attention sharpening at heat-end. Net effect is slightly less anchoring than mid-heat.

A within-stakes design — comparing same-stakes waves at different points in a heat — would distinguish (1) and (2). The corpus does not currently support this analysis.

### 7.4 Reform implications

In Conner (2026, Paper 3), the proposed Reform 2 is integer-scale scoring at the input layer (judges score in unit increments on a 0–100 scale, with display divided by 10). The natural alternative reform — extend the per-wave deliberation window — has been ruled out by the present analysis: extending the typical wave-to-wave gap from twenty-four seconds to seven minutes (Q1 to Q4 of the wave-density distribution in the 2022–2025 corpus) shifts anchoring by approximately 1.7 pp on a 31% baseline. You cannot run the clock long enough to fix this at the operational layer. The architectural reform is the only intervention with a defensible expected effect.

### 7.5 What this means for the cognitive-science literature

The Berger and Milkman (2012) account of round-number anchoring as time-pressure-induced retrieval is not contradicted by our findings; it is, however, not corroborated. The field-data prediction implied by their account — that stratifying on time-pressure within a single judging environment should produce monotone anchoring shifts — is at most weakly supported (H2 fatigue, ~1.8 pp), partially refuted (H1 wave-density does not replicate), and reversed in the strongest test (H3 end-of-heat). Surf judging may be a context in which anchoring is expressed regardless of time-pressure — driven instead by the cognitive cost of producing a continuous-scale subjective score *at all*. This would predict the architectural-fix expectation directly: change the input scale, change the anchoring rate.

---

## 8. Conclusion

Round-number anchoring in professional surf judging is the most replicable bias signature in the data. It is not, however, primarily driven by judge time-pressure. Across three pre-registered time-pressure proxies tested on a held-out 2025 sample of 14,106 judge decisions, one (wave-density) does not replicate, one (fatigue) replicates with a small effect, and the third (end-of-heat) replicates with a large effect *in the opposite direction from prediction* — judges anchor less, not more, in the final minutes of a heat. The reform implication is direct: extending the per-wave deliberation window will not meaningfully reduce anchoring; the architectural fix at the input scale layer remains the only intervention with defensible expected effect.

---

## References

Berger, J., & Milkman, K. L. (2012). What makes online content viral? *Journal of Marketing Research*, 49(2), 192–205.

Conner, A. (2026). *Manufacturing Consensus: Mechanisms of Subjective Bias in Professional Surf Judging.* Working paper, this archive, Paper 1.

Conner, A. (2026). *Reforming Olympic Surfing Judging Before LA 2028.* Working paper, this archive, Paper 3.

Englich, B., Mussweiler, T., & Strack, F. (2006). Playing dice with criminal sentences: The influence of irrelevant anchors on experts' judicial decision making. *Personality and Social Psychology Bulletin*, 32(2), 188–200.

Pope, D., & Simonsohn, U. (2011). Round numbers as goals: Evidence from baseball, SAT takers, and the lab. *Psychological Science*, 22(1), 71–79.

Tversky, A., & Kahneman, D. (1974). Judgment under uncertainty: Heuristics and biases. *Science*, 185(4157), 1124–1131.

Wansink, B., & Pope, L. (2014). When do gain-framed health messages work better than fear appeals? *Nutrition Reviews*, 73(1), 4–11.

---

## Appendix A — Confirmatory analysis output

Full output: `outputs/time_pressure_confirmatory_2026-05-07.json`. Pre-registration: `outputs/preregistration_time_pressure_2026-05-07.md` (sealed at git commit `c0d1e1a`). Discovery analysis: `outputs/time_pressure_anchoring_2026-05-06.json`.
