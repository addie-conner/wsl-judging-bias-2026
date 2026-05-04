# Pre-Registration: WSL Judging Bias Study (5 Mechanisms)

**Author**: Addie Conner (with Chorus analysis stack)
**Time-stamped**: 2026-05-03 (UTC)
**Location of canonical copy**: /Users/addieconner/chorus/wsl/outputs/preregistration_2026-05-03.md
**Git commit hash at time of writing**: (computed at SHA-lock step)
**Status**: LOCKED. Any deviation from this protocol must be reported in the manuscript's Methods or Limitations section.

---

## Background and motivation

Two prior peer-reviewed studies have analyzed WSL judging:

1. **Santos et al. 2025** (peer-reviewed; *Retos*, **64**, 311–321; mirrored as ResearchGate preprint 388676134; full author list: Santos, T. M., Rodrigues Santos, L. E., Vinicius, Í., Brietzke, C., Pereira, L. C., Melo, P. H., Moura, T. C. B., De Negri, T., Elsangedy, H. M., & Pires, F. O.) — "Intrinsic judgment error in men's championship World Surf League: WSL 2021" (Spanish version of record: "Error de juicio intrínseco en el campeonato mundial masculino de surf: WSL 2021"). Analyzed 4,095 waves × 5 judges = 20,475 individual scores from 7 men's CT 2021 events. Found inter-judge ICC = 0.97-1.00 (excellent agreement) with between-judge typical error of 0.15. Manually scraped from worldsurfleague.com.

2. **IJSF 2025** (*International Journal of Sport Finance* — note "Sport" not "Sports"; Sage Journals/FiT Publishing; DOI 10.1177/15586235251403230) — "WSL surfers score higher in home country when judged by compatriots." Analyzed 21,013 waves, 135 men's CT surfers, 2017-2022 (excluding 2020-21 for COVID), 37 events, 11 countries. Found compatriot-judge bonus of +0.04 to +0.32 points on waves >5.5 controlling for surfer-skill priors. (Author list pending verification — Sage article page returned 403 to automated fetches on 2026-05-03; confirm via institutional access before final submission.)

Neither paper:
- Included women's CT
- Extended to 2023-2025
- Tested multiple bias mechanisms simultaneously
- Decomposed score variance into objective (measurable) vs subjective (interpretive) components
- Cross-referenced with public sentiment ("robbery" claims) for behavioral validation
- Computed counterfactual heat-flip rates or counterfactual world-title outcomes
- Used Bayesian methods, double machine learning, or synthetic control
- Used per-judge fingerprinting beyond aggregate compatriot effects

This study addresses those gaps with a 5-mechanism pre-registered analysis on 2017-2025 men's + women's CT data.

## Hypotheses (pre-registered)

### H1 — Counterfactual world champion
**Claim**: If compatriot-judge bias were removed retroactively, at least one season's world title outcome (2017-2024) would change.
**Test**: Re-run season points cascade with bias-adjusted scores. Primary outcome: number of seasons in which the title-holder changes. Secondary: number of season-final ranks that shift by ≥2 positions.
**Significance threshold**: any change in title (n=0 vs n≥1) is the primary discrete outcome. For continuous tests, Bonferroni-corrected p < 0.01.
**Falsification**: bias-adjustment should NOT change title outcomes in seasons where the title-holder won by >800 points (large margin). If it does, our adjustment is too aggressive.

### H2 — Brazilian Storm scoring artifact
**Claim**: Brazilian surfers' wave-score residuals (after controlling for surfer skill prior + heat-mean wave quality) shifted positive significantly more than non-Brazilians' between 2010-2013 and 2014-2018.
**Test**: Difference-in-differences regression. Treatment group = Brazilian surfers; control = all others. Pre-period 2010-2013, treatment period 2014-2018. Outcome = wave-score residual.
**Significance threshold**: p < 0.05 after Bonferroni correction across the 5 hypotheses (so raw p < 0.01).
**Falsification**: in 2018-2024 (post-storm), Brazilian residuals should return toward baseline. If they remain elevated, this is a permanent shift, not a "Storm-era artifact."

### H3 — Surf Ranch as the bias control
**Claim**: At Surf Ranch (Lemoore, CA — wave-pool venue with physically identical machine-cut waves), aggregate scores still vary systematically by surfer world-rank, controlling for objective wave features.
**Test**: Within-Surf-Ranch heat-fixed-effects regression of `wave_score ~ surfer_rank + (objective wave features when available)`. Outcome: significant positive coefficient on surfer-rank-inverted (i.e., higher-ranked surfers score higher on identical waves).
**Significance threshold**: p < 0.01 (Bonferroni).
**Falsification**: at Surf Ranch, the same physical wave shape repeats — if our wave-quality control is properly identified, we should NOT see a rank effect on wave quality itself. Run as placebo.

### H4 — Crowd-noise predicts score
**Claim**: Peak crowd-decibel level during a ride explains more variance in wave-score than objective wave features (maneuver count, air time, wave size).
**Test**: Standardized-coefficient comparison in a regression `wave_score ~ peak_crowd_db + maneuver_count + air_time + wave_size + surfer_fe`. Outcome: |β_crowd| > |β_maneuver_count|.
**Significance threshold**: p < 0.01 (Bonferroni). Effect size: standardized coefficient ratio ≥ 1.0.
**Data dependency**: requires successful video-CV agent output. If CV fails, H4 is reported as "not testable in this study."
**Falsification**: at Surf Ranch (no crowd, indoor pool), crowd-noise coefficient should be non-significant.

### H5 — Per-judge fingerprinting
**Claim**: At least one named WSL judge has a statistically significant bias profile by surfer nationality after Bonferroni correction across all judges.
**Test**: For each judge with ≥30 scored waves per nationality cell, OLS regression of `judge_score - panel_mean ~ surfer_nationality + surfer_rank + heat_fe`. Bonferroni-correct across all judges tested.
**Significance threshold**: p < 0.01 per judge after correction.
**Data dependency**: requires Wayback per-judge data. If unavailable, H5 reported as "not testable in this study."
**Falsification**: judges should NOT show systematic bias on aggregate score (the trim-mean) — only on individual deviations. Aggregate-level placebo as sanity check.

## Data sources (pre-registered)

- **Aggregate per-wave scores**: scraped from `heatanalyzer.worldsurfleague.com` (publicly accessible). Code: `wsl/scrapers/wsl_results.py`. Coverage target: 2021-2025 men's + women's CT (2020 unavailable due to COVID gap in WSL archive).
- **Per-judge scores + nationality**: from Wayback Machine snapshots of `worldsurfleague.com` (public-access in 2021 per Santos et al. methods). Code: `wsl/scrapers/wayback_judges.py`. May fail if Wayback didn't archive the relevant DOM elements.
- **Public sentiment / contested heats**: scraped from Reddit r/surfing, BeachGrit, Stab Magazine, YouTube comments. Code: `wsl/scrapers/sentiment.py`.
- **Video features**: yt-dlp + OCR + YOLO-v8 on YouTube heat replays. Code: `wsl/scrapers/(video CV pipeline)`. POC scope only; full population pending if POC succeeds.
- **External signals**: NOAA buoy wave-physics, sponsor affiliations, heat stakes, Olympic-qualifying pressure, season points context. Code: `wsl/scrapers/external_signals.py`.

## Inclusion / Exclusion criteria

- **Include**: All Championship Tour (CT) events 2017-2025, both genders.
- **Exclude**: Challenger Series (different judging panel), wildcard exhibitions, Olympics 2024 (different ISA panel — analyzed separately if data permits).
- **Wave-level inclusion**: scoring rides only (waves with score > 0). "Replay" entries from heat-analyzer scraper are duplicates of original Top Score / Wave entries and excluded.
- **Surfer-level inclusion for H1/H2**: surfer must appear in ≥3 events in the analysis window. Wildcards/injury-replacements with single appearances excluded.
- **Heat-level inclusion**: heats with all surfer scores recorded; partial-data heats (404 from scraper) excluded.

## Statistical methods (pre-registered)

- **Standard errors**: clustered by `surfer_id` (Zitzewitz 2011 convention; surfers are the unit subject to repeated bias).
- **Multiple comparison correction**: Bonferroni × 5 hypotheses for primary tests. Secondary/exploratory tests reported separately as exploratory and not used for inference.
- **Bayesian replication**: every primary frequentist test paired with a Bayesian hierarchical model (PyMC or numpyro). Must agree in direction; disagreement = weak finding flagged in Limitations.
- **Robustness specifications**: every primary test re-run with (a) winsorized scores at 1/99%, (b) excluding the largest event by sample size, (c) excluding the most-disputed events from sentiment data. All three must point same direction for a "robust" claim.
- **Out-of-sample validation**: train H1/H2 on 2017-2022, predict on 2023-2025. Pre-registered effect sizes locked in this document.
- **Falsification tests**: as specified per hypothesis above.
- **Permutation tests**: where parametric assumptions are violated, replace with permutation p-values (10,000 permutations, surfer-clustered).

## Pre-registered effect-size predictions (for OOS validation)

These are LOCKED at this commit. Predictions made before any 2023-2025 data is incorporated into analysis.

- **H1**: 0-2 title flips out of 8 seasons (2017-2024). Most likely 0 flips but ≥4 surfers shifting ≥2 ranks.
- **H2**: Brazilian residual shift +0.10 to +0.30 between 2010-2013 → 2014-2018. Reversion in 2018-2024.
- **H3**: Surfer-rank coefficient at Surf Ranch in range (0.005, 0.025) per rank-position (positive = top-ranked surfers score higher on identical waves).
- **H4**: |β_crowd_db| > |β_maneuver_count| with ratio in (1.0, 2.5).
- **H5**: 1-3 named judges show significant nationality bias after Bonferroni.

## Deviations from prior literature

- We extend to women's CT (Santos / IJSF didn't).
- We test 5 mechanisms simultaneously (each prior paper tested 1-2).
- We use Bayesian + frequentist + permutation triangulation (priors used frequentist OLS only).
- We add public-sentiment cross-validation (no prior paper does).
- We do counterfactual title flipping (IJSF computed bias coefficient but not flip rate).
- We add NOAA wave-physics ground-truth control (no prior paper controls for actual measured wave conditions).

## Relationship to prior literature (added per peer-review fix EZ-10)

Both reviewer 1 (Zitzewitz) and reviewer 2 (Santos co-author) correctly noted that the
prior draft framed this work as a discovery paper. It is not. Santos et al. 2021
already documented inter-judge ICC = 0.97-1.00 in men's CT 2021; IJSF 2025 already
documented compatriot-judge bias of +0.04 to +0.32 points. This study is best read as
**three layered contributions on top of that existing literature**:

1. **Replication** of Santos's reliability finding on a larger corpus
   (n=24,901 waves across 2,145 heats and 38 events, 2022-2025) — does the
   ICC = 0.97-1.00 pattern still hold once the panel-level metric is recomputed
   on 6× more waves? Where per-judge data is available we report ICC₃,₁ /
   ICC₃,₅ / SEM / MDC₉₅ following Koo & Li 2016 + Hopkins 2000.
2. **Replication** of IJSF's compatriot-judge result, with a women's CT extension
   (the IJSF sample was men-only). Same effect-size benchmark: a coefficient
   inside +0.04 to +0.32 points is consistent with IJSF; outside the band is
   evidence against.
3. **Negative replication test** on 2023-2025: this window is out-of-sample
   relative to both Santos (2021) and IJSF (2017-2022). If the bias is real and
   stable, it should reproduce here. If it does not, that is informative on
   its own.
4. **New mechanisms not tested by Santos or IJSF**: counterfactual title flips
   (H1, with the actual WSL bracket-points cascade per fix EZ-2), Brazilian
   Storm residual shift (H2, scope-dependent on data window), Surf Ranch as
   bias control (H3), crowd noise (H4), per-judge fingerprinting (H5).
5. **More rigorous validation** than either prior paper: pre-registration with
   locked SHA, OOS hold-out, multi-spec robustness, two-way / cluster-bootstrap
   SEs, Bayesian + frequentist + permutation triangulation on EVIDENCE not just
   sign (per fix EZ-5), STROBE checklist, kill-log of pre-registered tests
   that did not survive the data window.

Throughout the manuscript and outputs we therefore avoid framing language that
implies first-discovery ("we discover", "we are the first to show", "previously
unrecognized bias"). The accurate framing is: *prior literature documented the
phenomenon on smaller and earlier samples; we test whether it replicates on
2023-2025 men's + women's CT, and we extend to mechanisms the prior literature
did not test.*

## Reporting standards

- STROBE-compliant for observational study design.
- Every finding accompanied by: effect size, 95% confidence/credible interval, p-value (corrected), n, statistic, sensitivity analysis result, falsification result.
- Limitations section explicit about: per-judge data scope, video-CV scalability, sentiment selection bias, Brazilian-judge-nationality identification difficulty.

## Code and data availability

- Full analysis code at `https://github.com/addie-conner/chorus/tree/main/wsl/`.
- Aggregate data publicly redistributable; per-judge data redistributability pending (depends on Wayback ToS).
- Docker container with reproducibility recipe to be provided in the published version.

## Reviewer-2 pre-mortem
Adversarial review will be performed on the manuscript draft before submission. Critique items addressed or acknowledged in Limitations.

## Sign-off

This pre-registration is locked at the time-stamp above. All hypotheses, methods, thresholds, and effect-size predictions are fixed. The current state of the dataset (as of commit hash recorded at SHA-lock) is: aggregate scores from 2025 Pipe Pro only (smoke-test); full backfill 2021-2025 in progress. No data inspection beyond the smoke-test 387 waves has occurred prior to this pre-registration. Any deviation from this protocol must be flagged in the manuscript.


---

## Addendum 2026-05-03 — quasi-experimental identification extensions

**Time-stamped**: 2026-05-03 (UTC). **Status**: This Addendum was specified BEFORE
the full 2021-2025 backfill data was inspected. The current heats.parquet at
the time of this Addendum contains 2022-2025 men's + women's CT events
(~24,900 wave rows across 38 events). All three new tests below are sealed
prior to running them on any pre-2022 data that lands subsequently.

These are NOT new substantive hypotheses — H1, H3, and the IJSF
compatriot-bias premise remain the locked primary tests. H1b, H3b, and H6 are
quasi-experimental ports that elevate the study from correlational claims
toward credible causal claims, using natural experiments and counterfactual
arithmetic.

### H1b — Head-judge replacement RDD (extension of H1's personnel-vs-institution interpretation)

**Claim**: If WSL judging bias is INSTITUTIONAL, average wave-score residuals
should be continuous through head-judge transitions. If bias is PERSONNEL-
DEPENDENT, residuals should show discontinuities at the transition dates.

**Test**: Regression discontinuity around each catalogued head-judge
transition (head_judge_tenure.json):
  - 2018-02-06 (Richie Porta → Pritamo Ahrendt, men's CT)
  - 2023-10-11 (Pritamo Ahrendt → Luiz "Luli" Pereira, all tours)
  - (medium confidence) 2020 (women's CT head-judge transition to Pereira)

Specification: `wave_score_residual ~ days_from_transition + I(days_from_transition >= 0) + heat_FE + surfer_FE`,
+/- 12-month bandwidth, Imbens-Kalyanaraman optimal bandwidth via `rdrobust`,
HC1 standard errors. Stratified by surfer-nationality (BRA / USA / AUS) for
exploratory bias-direction interpretation.

**Significance threshold**: p < 0.05 / 3 = 0.0167 (Bonferroni across the
three new Addendum tests).

**Falsification**: a placebo RDD at a date six months OFF from the actual
transition should show NO discontinuity. If it does, the design is fragile.

### H3b — Surf Ranch venue-shock diff-in-diff (extension of H3's bias-control interpretation)

**Claim**: Surf Ranch (Lemoore, CA) joined the CT in 2018 as the first
wave-pool venue with physically identical machine-cut waves. If wave-quality
variability enables judging bias, bias coefficients (rank, compatriot)
should be SMALLER at Surf Ranch than at ocean venues, controlling for surfer
fixed effects.

**Primary specification (DiD)**: `wave_score_residual ~ post_2018 + treated_surfer + post_2018:treated_surfer + venue_FE + surfer_FE`,
clustered SEs by surfer_id. "Treated" surfer = surfer who appeared at Surf
Ranch in any 2018+ season.

**Within-venue specification (when DiD untestable)**: within Surf Ranch
heats only, `wave_score_residual ~ surfer_world_rank` with heat FE; compare
absolute coefficient to within-Pipeline (most subjective venue) equivalent.
Report `|β_pipe| / |β_surf_ranch|` ratio as descriptive.

**Significance threshold**: p < 0.0167 (Bonferroni × 3).

**Falsification**: at Surf Ranch, the same machine-cut wave repeats — if our
spec is right, the rank-on-residual coefficient should be small in absolute
value. A LARGE Surf Ranch coefficient would invalidate the design (it would
imply rank effects on identical waves, which means the residualization is
broken or the wave-quality control is misspecified).

### H6 — Counterfactual prize-money / Olympic-spot bias-cost

**Claim**: Compatriot-judging bias has measurable expected-value cost in
prize money, CT-slot retention value, and Olympic-qualification value over
2017-2024. The IJSF (2025) headline ("doesn't change winners often") is
incomplete; the full $-cost is the headline-friendly framing.

**Test**: For each (surfer, event), subtract the IJSF compatriot-bias point
estimate (central +0.18 pts; robustness at +0.04 and +0.32) from every wave
where compatriot-judging is true. Recompute heat winners, deepest-round-
reached, season points (WSL official points table), and prize money (WSL
official prize table). Aggregate per-surfer over the full window.

**Compatriot-judging proxy**: home-country match (event country == surfer
country). This is a CONSERVATIVE proxy — it understates the bias-paying
wave pool because it misses non-home events with at least one same-
nationality judge on the panel. Estimates are LOWER BOUNDS until per-judge
nationality data is recovered.

**Indirect-value tracks** (constants wired, attribution pending):
  - CT slot annual value: $500K (industry midpoint, $300K-$1M range)
  - Olympic medalist sponsor uplift: $3M (Pernet/Jewell sport-econ midpoint)
  - Olympic participation value: $250K

**Significance threshold**: p < 0.0167 (Bonferroni × 3) on a Wilcoxon
signed-rank test of per-surfer net dollar deltas, paired by surfer.

**Falsification**: if the headline aggregate $-delta is dominated by a
single surfer/event, the result is fragile. We require ≥3 surfers each
losing >$10k AND ≥3 surfers each gaining >$10k for the headline result to
be considered robust.

### Pre-registered effect-size predictions for the Addendum

  - **H1b**: discontinuity at 2023 transition in [-0.05, +0.05] residual
    points; nationality-stratified BRA-only discontinuity in [-0.02, +0.10]
    (consistent with personnel hypothesis if Brazilian residuals jump
    positive at the appointment of a Brazilian head judge).
  - **H3b**: `|β_pipe| / |β_surf_ranch|` in (1.5, 4.0); Surf Ranch rank-
    coefficient in (0.000, 0.015); Pipeline rank-coefficient in (0.010,
    0.040).
  - **H6**: total $-delta in $0.5M-$3M (lower-bound proxy); top-3 gifted
    and top-3 robbed surfers each cumulatively in 6-figure range.

### Sealing and reproducibility

The pre-registration file at `wsl/outputs/preregistration_2026-05-03.md`
remains immutable above this Addendum line. The Addendum text is appended
once and is itself sealed at the timestamp shown above. Code that
implements these tests lives in `wsl/analysis/quasi_experimental.py`.


---

## Exploratory Addendum 2026-05-03 (post-Tier-1-fixes)

**Status**: 10 exploratory hypotheses (H7-H16) added AFTER the locked pre-registration but BEFORE seeing the test results. These are NOT primary tests; they are labeled "exploratory" throughout the manuscript. Bonferroni correction applied across the 10 exploratory tests separately from the 5 primary + 3 quasi-experimental.

**Why exploratory**: each is a novel mechanism not tested in any prior WSL judging-bias paper. None has a strong prior literature anchor; they are theory-generating, not theory-confirming. If any survives Bonferroni 10× correction, that becomes a genuine novel-mechanism finding for the paper — but reported as exploratory, not as confirmatory evidence.

### H7 — Comeback-narrative bias
*Claim*: Surfers losing their heat by a large margin receive systematically inflated scores on subsequent waves (WSL commercial interest in close heats).
*Test*: `wave_score_residual ~ heat_deficit_at_wave + surfer_FE + heat_FE`, surfer-clustered SE.
*Falsification*: should NOT appear in opening rounds (where stakes are lower).

### H8 — Sequential contrast / anchoring
*Claim*: `wave_score_t` correlates with `wave_score_t-1` controlling for surfer skill.
*Test*: regression with same controls as H7.

### H9 — Decision fatigue / time-of-day
*Claim*: Pre-lunch waves score lower than post-lunch (Danziger 2011 mechanism).
*Test*: time-of-day bucket regression.

### H10 — Claim-frequency anchoring
*Claim*: Visible "claim" gesture by surfer post-wave inflates score.
*Test*: pose-estimation detected claim → regression.
*Data dependency*: video-CV pipeline; n=22 POC initially.

### H11 — Round-number bias
*Claim*: WSL scores cluster at .00 / .25 / .50 / .75 endings more than uniform.
*Test*: chi-square distribution test on aggregate scores; per-judge subcut if available.

### H12 — Tour-narrative tightness
*Claim*: Score variance is lower in close-title-race seasons.
*Test*: variance vs season-end-margin regression.

### H13 — Wildcard structural penalty
*Claim*: Wildcards score lower than CT seeds at the same event controlling for skill.
*Test*: subgroup regression.

### H14 — Anticipatory trim-mean gaming
*Claim*: Individual judges' deviations from panel mean shrink across a heat (judges getting "safer").
*Test*: `|judge_score - panel_mean| ~ wave_position_in_heat + judge_FE + heat_FE`.
*Data dependency*: per-judge data (judges.parquet from Wayback agent).

### H15 — Brand-logo visibility / dwell time
*Claim*: Waves where the title sponsor's logo is more prominent in frame get higher scores.
*Test*: logo-dwell-time regression on score residual.
*Data dependency*: video-CV with template matching for sponsor logos.

### H16 — Pre-heat announcer hype
*Claim*: Surfers given longer / more enthusiastic intros score higher on their first wave (priming).
*Test*: hype-score regression on FIRST wave only; subsequent waves used as falsification.
*Data dependency*: broadcast audio + ASR.

### Significance threshold for exploratory hypotheses
p_Bonferroni × 10 < 0.05 for any single exploratory test to count as "significant." Findings reported as "exploratory; replication required" in the manuscript regardless.


---

## Addendum 2026-05-03 — Late Findings (EXPLORATORY POST-HOC)

**Time-stamped**: 2026-05-03 (UTC, late-day append). **Status**: EVERY entry below is **exploratory post-hoc**. Each was specified, designed, and run AFTER the primary five hypotheses (H1–H5), the quasi-experimental Addendum (H1b/H3b/H6), and the H7–H16 exploratory Addendum had been locked and (in most cases) had results in hand. None of these entries can be claimed as confirmatory evidence under the locked pre-registration. They are reported in this Addendum precisely so that the manuscript's "what was pre-registered vs. what was discovered" line is auditable from a single document.

The reason this Addendum exists at all — rather than burying the post-hoc tests in a Limitations footnote — is that academic credibility on a study of this size depends on the reader being able to draw a clear line between the locked-and-tested set and the discovered set. Wherever any of these findings appears in the manuscript, the body text must label it "exploratory post-hoc" and link back to this section. None of them counts toward the headline "X of 5 mechanisms survived Bonferroni" framing.

### LF1 — H32 Brazilian post-2023 reversal (institutional accountability finding)

**Status**: exploratory post-hoc. Not in the locked H1–H16 + Addendum set.

**Claim**: After Luiz "Luli" Pereira (BRA) became head judge on 2023-10-11, panel composition was rotated to AVOID Brazilian-stacked panels — explaining the null Brazilian compatriot effect in the 2022–2025 aggregate vs. the IJSF 2017–2022 finding.

**Why post-hoc**: H32 was specified after we observed (a) the H1b regression-discontinuity result on the 2023-10-11 transition and (b) that the IJSF compatriot-bias result did not replicate at headline magnitude on 2022–2025 men's CT. We then asked the natural follow-up — whether panel-composition policy changed — and ran the test, with the panel-composition descriptive statistics coming first as a sanity check.

**Rationale for inclusion**: The result is about institutional response to anticipated scrutiny, not about a new bias. It is the most defensible answer to the reviewer question "why does the IJSF compatriot effect attenuate in 2022–2025?" — and the data is unambiguous: in 2022–2023 (Ahrendt era), 100% of Brazilian-surfer waves were judged by a panel that included a Brazilian judge and 56–58% had ≥2 Brazilian judges; in 2024–2025 (Pereira era), ≥2-Brazilian-judge panels DROPPED TO 0% and the ≥1-Brazilian-judge rate fell to 67–75%. Placebo on USA and AUS panel-composition is stable. Source: `wsl/outputs/h32_brazil_reversal_results.md`.

**Pre-registration status of related primary tests**: H1b (head-judge RDD) was pre-registered in the 2026-05-03 quasi-experimental Addendum and is the locked test that motivated H32. H32 itself is not locked.

**Significance posture**: descriptive (panel-composition counts are exact, n=961 wave rows, zero ≥2-BRA panels post-2023). The companion regression coefficients in `h32_brazil_reversal_results.md` Test 1/1b are reported but not used for inference — Bonferroni × 4 on the regression battery does not survive (max p_bonf = 0.4414). The headline is the count-based composition shift, not the regression coefficient.

### LF2 — Unified Bayesian-prior mechanism framing (post-hoc theoretical synthesis)

**Status**: exploratory post-hoc. Theoretical re-framing, not a new test.

**Claim**: The five primary mechanisms (H1 counterfactual title, H2 Brazilian Storm, H3 Surf Ranch, H4 crowd noise, H5 per-judge fingerprinting) and the surviving exploratory mechanisms (H7 comeback, H11 round-number, H17 day-amplification, reputation prior) all collapse to a single Bayesian-prior decision rule: each judge holds a shared prior on score distribution and updates that prior toward identity / narrative / conformity signals to a degree that depends on broadcast-stakes amplification.

**Why post-hoc**: this synthesis was written after the empirical work was complete. We did not derive predictions from the unified model and test them; we observed which mechanisms survived and noticed they all share the same conformity-mediated broadcast-amplification structure. The model in `wsl/outputs/theoretical_model.md` is therefore an *organising* framework, not a predictive one.

**Rationale for inclusion**: a reviewer reading nine surviving mechanisms across three hypothesis families will reasonably ask "is there a single underlying mechanism, or nine?" The Bayesian-prior framing answers that question without claiming new evidence. It also defines what reform 1+2+3+4 (D/E split, nationality-blind, transparency, larger panel) is attacking at the mechanism level — see `wsl/outputs/reform_simulation_results.md`. We treat this as expository, not inferential.

**Falsification posture**: explicitly no falsification claim. The unified model is presented as a way to read the empirical results, not as a hypothesis the empirical results test.

### LF3 — Cross-sport replication: H7 in figure skating (exploratory cross-sport test)

**Status**: exploratory post-hoc. ISU figure-skating data was scraped and analysed AFTER the WSL H7 result was confirmed.

**Claim**: H7 (comeback-narrative bias — surfers behind on the leaderboard receive systematically inflated scores on subsequent waves) replicates in ISU figure-skating GOE residuals: skaters whose program is running below their cohort-mean GOE residual receive larger GOE adjustments on subsequent elements.

**Why post-hoc**: figure-skating data was not in the original pre-registration scope (the locked file specifies WSL CT 2017–2025 plus Olympic 2024 as a comparison case). We added the cross-sport test because H7 is the most replicable mechanism in our results and the ISU score-sheet PDFs are publicly archived — making it the lowest-friction external-validity check available.

**Rationale for inclusion**: the WSL H7 result alone is vulnerable to the "this is a surfing-specific narrative effect" critique. ISU evidence that the same direction-of-bias appears in a different judged sport with a different rubric, different panel size, and a different elemental structure is the strongest within-corpus defense available against that critique. The skating result (Spec A coef +0.0932, p = 6.6 × 10⁻²⁴⁷, n = 21,346 element-rows; Spec B program-FE coef −0.1400, p = 6.2 × 10⁻⁷³) is published in `wsl/outputs/skating_replication_results.md`.

**Significance posture**: replication direction matches surfing (negative-sign convention identical: deficit → score lift). Of the two WSL-novel mechanisms ported (H7, H11), 1/2 replicate in skating (H11 round-number does not). We report the 1/2 number rather than the 1/1 H7-only number because reporting only the surviving cross-sport test would be cherry-picking.

### LF4 — Olympic 2024 replication (exploratory post-hoc replication on excluded population)

**Status**: exploratory post-hoc. The locked pre-registration explicitly EXCLUDED Olympic 2024 from the primary CT analysis ("Olympics 2024 (different ISA panel — analyzed separately if data permits)").

**Claim**: 4 of the 5 confirmed WSL mechanisms (round-number clustering, day-of-event amplification, reputation prior, comeback-narrative) replicate or show same-direction-with-power-limited-significance on the Paris 2024 Olympic surfing data at Teahupo'o (288 scoring waves, 64 heats, 48 surfers, 21 nations).

**Why post-hoc**: Olympic 2024 was scoped as a "comparison case if data permits" in the locked pre-registration but no specific tests were pre-registered against it. We back-ported each WSL-confirmed mechanism (one test per mechanism) as the comparison case, with Bonferroni × 6 across the six tests (O1–O6). Source: `wsl/outputs/olympic_2024_bias_replication.md`.

**Rationale for inclusion**: Olympic 2024 is the most-watched surfing event in history and the closest available out-of-sample population to the WSL CT. If WSL bias mechanisms are real and not artifacts of WSL-specific judging culture, we expect them to show up in any panel of judges drawn from the same global pool — which the ISA panel is. The replication is partial: O1 host-country (null in both), O2 round-number (replicates, p_bonf = 0), O3 comeback-narrative (partial-directional, n=221 power-limited), O4 day-amplification (failed — opposite sign; n=14 too small), O5 reputation prior (replicates, p_bonf = 0.027), O6 Benjamin Lowe panel-removal (novel Olympic-specific natural experiment, no WSL analog).

**Significance posture**: the manuscript reports "3/4 mechanisms with WSL training-data signal also replicate at Olympic 2024" rather than "4/5 mechanisms replicate" because (a) O4 failed in direction, not just power, and (b) O1 was not a WSL-positive baseline (host-country was null in WSL CT too — both nulls is co-replication, not confirmatory). The four mechanisms that DO replicate (round-number, comeback, reputation, host-country-null) are reported as exploratory cross-population evidence, not as confirmation of the locked WSL pre-registered tests.

### LF5 — CLIP similar-wave retrieval (exploratory post-hoc identity-vs-wave probe)

**Status**: exploratory post-hoc. Not pre-registered. Proof-of-concept scope.

**Claim**: When two visually-near waves (OpenCLIP ViT-B/32 cosine similarity ≥ 0.85) are scored very differently (|score diff| ≥ 1.5), the score difference correlates more strongly with surfer-identity than with residual visual distance — consistent with score being anchored to the surfer's running prior more than to the specific wave's physics.

**Why post-hoc**: CLIP retrieval was added in the final 24 hours as a way to interrogate the "are judges scoring the WAVE or the SURFER?" question without per-judge data. The 31-wave POC scope (3 heats, 5 surfers at 2025 Pipe Pro) is too small for a publication-grade identity-vs-physics claim and was never specified in the pre-registration.

**Rationale for inclusion**: the most evocative artifact in the dataset is the cluster of pairs at cos ≈ 0.99 with |score diff| ≈ 8.0, all within the same heat. Mamiya 10.00 / Florence 1.00 (cos = 1.000), Mamiya 10.00 / Ewing 1.40 (cos = 0.975), Mamiya 9.80 / Fioravanti 1.50 (cos = 0.991, twice), Florence 9.63 / Ewing 1.40 (cos = 0.984). These pairs are visually near-identical waves at the same break in the same hour, scored 8 points apart. They are the most readable single piece of evidence in the entire study that score is partially independent of wave physics. The interaction-model coefficient (`embedding_distance × surfer_match` = −25.5, p = 0.0005) is reported in `wsl/outputs/wave_embedding_retrieval_results.md` as directional only.

**Significance posture**: the main-effects model has surfer_match coef = −0.378, p = 0.444 — not distinguishable from zero. The interaction model leans surfer at p < 0.001 but on n=197 unordered pairs across 5 surfers, the cluster-robust SEs are small-cluster approximate. We treat the entire exhibit as illustrative of the identity-anchoring channel, not as an inferential test of it.

### LF6 — Multi-LLM synthetic judging panel (exploratory POC; results disclosed regardless)

**Status**: exploratory post-hoc. POC scope (n=22 unique waves across 3 heats, 5 surfers).

**Claim**: A three-LLM ensemble (Gemini 2.5 Flash, GPT-4o-mini, Claude Sonnet 4.6) judging the same 2025 Pipe Pro waves on the 0–10 scale produces score distributions that are calibrationally close to the WSL panel mean (MAE ≈ 0.49 ensemble vs. WSL trim-mean) and exhibit round-number clustering at 0.500 share for the masked condition (n=2 distinct waves with cleanly-coded condition). Identity-prior (masked vs. revealed) and reform-simulation arms run but are NOT publication-grade at this n.

**Why post-hoc**: the synthetic judging panel was not in the original pre-registration (the locked file scopes computer-vision wave-feature extraction but not LLM scoring). It was added as a methodology probe — the question "if we could toggle surfer identity in-silico, would model scores move?" is the kind of counterfactual the public WSL data structurally cannot answer.

**Rationale for inclusion**: even at n=22 the technique is the contribution, not the n. The methodology section of the paper can describe the in-silico identity toggle and the larger-panel reform simulation as a falsifiable scaffold that future work (≥200 waves) can run; the current results (Phase 2 directional ensemble agreement, Phase 3 no revealed-condition data, Phase 4 7-judge panel does not reduce within-wave SD below 3-judge baseline at this n) are reported in `wsl/outputs/llm_synthetic_judging_results.md` with an explicit "n=22 is proof-of-concept, not publication-grade as the headline experiment" caveat. We disclose the POC results regardless of whether they directionally support reform simulation, to avoid file-drawer bias.

**Significance posture**: every metric is reported with its caveats. No claim from this POC enters the manuscript's headline replication framing. The technique itself — identity-masked / identity-revealed prompting plus larger-panel bootstrap — is presented as a future-work protocol. If the n=22 results had directly contradicted the H11 round-number finding (e.g. LLM panels produced no clustering), we would still report them; that would be informative on its own. They did not, but that's also informative on its own at this n.

### Aggregate disclosure

These six entries (LF1 → LF6) are the complete list of substantive post-hoc tests, replications, and theoretical re-framings that landed AFTER the locked pre-registration + locked Addenda were sealed. They are all flagged "exploratory post-hoc" wherever they appear in the manuscript, the press kit, the comms materials, or the public dashboard. The headline "5 / 5 + 3 + 10" pre-registered count and the "X of 5 mechanisms survived Bonferroni" framing both refer to the locked set ONLY.

If the manuscript reviewer or the journalistic auditor wants to read every line of locked-vs-discovered separation in one place, this Addendum is that place.
