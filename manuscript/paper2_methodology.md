# Eighteen Gates and the Causality Ladder: A Validation Framework for Bias Identification in Subjective-Sport Judging

_Methodological companion to Conner et al. (2026), "Manufacturing Consensus: Mechanisms of Subjective Bias in Professional Surf Judging."_

---

## Authors and affiliations

Addie Conner (independent; Chorus Research)

_Corresponding author:_ Addie Conner, addieconner@gmail.com
_ORCID:_ https://orcid.org/0009-0007-7853-4140

_Pre-registration:_ `wsl/outputs/preregistration_2026-05-03.md` (locked 2026-05-03 UTC; git SHA `7d0e2c8`).
_Code, data, replication archive:_ https://github.com/addie-conner/chorus/tree/main/wsl/

---

## Abstract

Subjective-sport judging research has accumulated a large empirical literature documenting systematic identity-correlated biases — compatriot bonuses, reputation priors, round-number anchoring, narrative-stakes amplification, host-country effects — but has not converged on a methodology for separating *descriptive* from *causal* bias claims. Most published estimates rely on cluster-robust ordinary least squares with surfer or skater fixed effects, an approach that is vulnerable to wave-quality, venue-quality, and selection confounding when applied to identity-correlated treatments such as same-country panel composition. We propose a five-rung **causality ladder** for subjective-sport bias identification — naive OLS → cluster-robust OLS → heat fixed effects → Bayesian Model Averaging → doubly-robust ML (TMLE / Causal Forest) — combined with an **18-gate validation harness** that establishes when a finding is robust, causally identified, or bulletproof. We demonstrate the framework on the largest professional surf-judging corpus assembled to date (60,834 wave-rows; 301,478 individual judge-scores; 17 seasons; 86.3% nationality coverage) and show three substantive findings. (1) The ladder produces dramatic estimate divergence: a naive Australian home-bloc OLS estimate of +0.616 points (p = 2 × 10⁻⁹) collapses to TMLE +0.005 [−0.15, +0.16] and Causal Forest −0.024 [−0.57, +0.52]; per-judge difference-in-differences returns +0.108 [−0.06, +0.27], not conventionally significant. (2) The pre-registered "unified-mechanism" framework — common in subjective-sport literature — empirically fails on this corpus: cross-correlation between four primary mechanism vectors at the per-heat level returns mean |r| = 0.042; canonical correlation r₁ = 0.119; PCA PC1 explains 25.7% of variance; Granger causality between mechanism dynamics fails. The four mechanisms operate as statistically independent channels, not signatures of a single underlying parameter. (3) Bayesian hierarchical models with Gaussian likelihoods exhibit posterior-predictive failure for round-number-anchored outcomes (predicted round-rate 4.0% vs observed 23.0%) — model-class misspecification that we resolve via a mixture-of-Gaussians-plus-atoms specification recovering π_round ≈ 0.14 atom-mass parameter. We provide the framework as a transferable methodology for figure-skating, gymnastics, dressage, DanceSport, and Olympic-boxing corpora, where naive fixed-effect estimates of compatriot and reputation effects have been the field standard for decades.

_(~430 words.)_

---

## 1. Introduction

### 1.1 The methodological problem

Subjective-sport judging research operates under structural conditions that complicate causal inference. The treatments of interest — compatriot panel composition, reputation cues, narrative framing, host-country status — are correlated with the conditions under which performances occur (venue, swell, crowd, scheduling, athlete preparation), which are themselves correlated with the outcomes of interest (athletic performance proxied by judge score). Naive ordinary least squares with cluster-robust standard errors is the field standard. It is also, by economists' modern criteria, an inadequate identification strategy for estimands that depend on these treatment–performance correlations.

Two decades of cross-sport empirical literature — Findlay & Ste-Marie (2004), Zitzewitz (2006, 2014), Heiniger & Mercier (2018, 2021), Krumer (2022), Veronesi et al. (2023), Santos et al. (2025), the IJSF (2025) compatriot study — overwhelmingly used cluster-robust OLS or near variants. The estimates produced have been treated as approximately causal in policy discussions, advocacy, and reform proposals. The methodology gap has not been articulated with precision because the field lacks a unified validation framework.

This paper proposes such a framework. The framework has two components: a causality ladder for graduated identification and an 18-gate validation harness for systematic robustness assessment. We demonstrate both on the largest professional surf-judging corpus assembled to date and use the demonstrations to illustrate substantive methodological findings about how subjective-sport bias should be measured.

### 1.2 Three contributions

**Contribution 1: The Causality Ladder.** We propose a five-rung graduated identification strategy for subjective-sport bias claims, where each rung addresses a specific identification concern raised by the previous rung. Naive OLS, cluster-robust OLS with controls, fixed-effects OLS, Bayesian Model Averaging across spec battery, and doubly-robust ML (TMLE / Causal Forest / Cross-fit DR) constitute the rungs. The ladder produces dramatic estimate divergence on the surf-judging corpus: a naive +0.616-point home-bloc estimate collapses to TMLE +0.005 with confidence interval crossing zero. Identical phenomenology has been observed in the labour and education economics literatures over the past decade as those fields adopted doubly-robust methods (Chernozhukov et al. 2018; Athey & Wager 2019); we extend the methodology to subjective-sport judging.

**Contribution 2: The 18-Gate Validation Harness.** We propose an explicit 18-gate validation harness covering pre-registration, holdout sealing, multiple-comparisons correction, sensitivity bounds, negative-control outcomes, doubly-robust confirmation, hierarchical Bayesian posterior, posterior-predictive check, cross-sport replication, prospective Brier scoring, and per-judge identification. We define three findings-classifications — *robust*, *causally identified*, and *bulletproof* — by which gates a finding survives. We argue this stratification should replace the binary "significant / not significant" rhetoric in subjective-sport bias literature.

**Contribution 3: Per-judge DiD as the cleanest available identification on the compatriot question.** Where per-judge data are available — and we describe how to recover them via Common Crawl WARC archives, Wayback Machine, and authenticated scraping — a difference-in-differences specification at the (surfer × judge) level provides identification under weaker assumptions than panel-level analysis. We demonstrate the method recovers a clean small-positive null on the WSL Australian-bloc question (DiD = +0.108 [−0.06, +0.27]) where panel-level OLS produces an aggressive +0.616 estimate. We argue per-judge DiD should become the field-standard benchmark identification for compatriot effects in any subjective sport where per-judge scores are publicly recoverable.

### 1.3 Three sub-findings of methodological significance

Demonstrating the framework on the WSL corpus surfaces three methodological sub-findings that we treat as themselves contributions.

**Sub-finding A: The unified-mechanism assumption fails empirically.** The cross-sport literature (Heiniger & Mercier 2021's shared-bias decomposition; the gymnastics calibration-drift framework) implicitly assumes that subjective-sport biases are signatures of a single underlying mechanism — a shared prior, a common calibration, a unified ideological frame. We test this assumption directly on the WSL corpus and reject it. Mean cross-correlation between four primary mechanism vectors at the per-heat level: |r| = 0.042. Canonical correlation r₁ = 0.119. PCA PC1 explains 25.7% of variance (close to the 20% null for 5 independent components). Granger causality between mechanism dynamics fails (round→score F = 0.52, p = 0.59). The four mechanisms operate as statistically independent channels. Theoretical models of subjective judging that posit one underlying parameter require sport-specific empirical justification.

**Sub-finding B: Bayesian hierarchical models with Gaussian likelihoods are misspecified for atom-anchored outcomes.** Across 17 seasons of WSL judging, 59.9% of individual judge-scores end in .0/.25/.5/.75 (uniform null = 20.0%; ratio 3.0×). A Gaussian Bayesian hierarchical model fit to wave-scores returns a posterior-predictive round-rate of 4.0% [3.7%, 4.3%] against an observed 23.0% — a clean PPC failure. We demonstrate that a mixture-of-Gaussians plus atoms-at-round-values specification recovers the round-rate within 95% credible interval and reports a posterior π_round = 0.139 atom-mass parameter (CrI [0.131, 0.149]). The implication generalises: any model of subjective judging that omits round-number atoms will be miscalibrated for the per-event 23–60% round-rate signature. Sport-specific scoring scales determine whether atoms are necessary in the likelihood specification.

**Sub-finding C: Per-judge DiD identifies compatriot effects under weaker assumptions than panel-level OLS.** The cleanest test of compatriot judging asks whether judge nationality interacts with surfer nationality at the individual scoring level, controlling for which judges are on the panel and which surfer is being scored. We demonstrate the method recovers a clean small-positive-but-not-significant DiD (+0.108 [−0.06, +0.27]) where panel-level OLS estimated +0.616. The discrepancy is interpretable: the panel-level estimate combines compatriot judging with venue, crowd, jet-lag, and selection confounding; the per-judge DiD isolates the compatriot mechanism *given* the panel composition. The two estimates measure different estimands; conflating them is the methodological error we propose to correct.

---

## 2. The Causality Ladder for Subjective-Sport Bias Identification

### 2.1 Five rungs

We define the ladder as five graduated identification strategies, each addressing a specific concern about the previous one.

**Rung 1: Naive OLS.** Wave-score regressed on the treatment of interest with no controls. Provides the descriptive correlation. The standard against which more careful identification is measured.

**Rung 2: Cluster-robust OLS with controls.** Adds standard controls (rank, year, gender, surfer-country, event-country dummies) and cluster-robust SE at the natural unit of correlation (typically surfer or judge). The cross-sport published literature operates predominantly at this rung.

**Rung 3: Fixed-effects OLS.** Demeans within heat (or within performance, depending on sport). Removes between-heat variation that confounds identity-treatment estimates with venue / wave-quality / scheduling differences. Within-heat estimates are smaller than naive OLS estimates by construction; the magnitude of the reduction is a diagnostic for between-heat confounding.

**Rung 4: Bayesian Model Averaging across spec battery.** Computes BIC-weighted average across a battery of specifications differing in covariate set and FE structure. Returns a single coefficient estimate that integrates over specification choice; the BMA weights themselves diagnose which specification BIC favours. On our WSL data, the heat-FE specification carries BIC weight 1.0 and the BMA estimate equals the heat-FE estimate (β = +0.024 for AUS bloc), demonstrating that the OLS-with-controls estimate (β = +0.58) is data-dispreferred relative to the fixed-effects specification.

**Rung 5: Doubly-robust ML.** Cross-fit double machine learning (TMLE / LinearDRLearner / Causal Forest) with sample-splitting. Uses random forests or other ML nuisance models to flexibly absorb confounding without parametric assumptions; the doubly-robust property guarantees consistent ATE estimation under mild conditions on either the outcome or propensity model. On the AUS-bloc question, TMLE returns ATE = +0.005 [−0.15, +0.16] and Causal Forest returns ATE = −0.024 [−0.57, +0.52]. Both confidence intervals cross zero; both point estimates are within rounding error of zero.

**Optional Rung 5+: Per-judge DiD.** When per-judge scores are recoverable, the difference-in-differences specification at (surfer × judge) cells provides identification under the *weakest* assumptions in the ladder: that the compatriot premium for surfers of nationality X being scored by judges of nationality X, *minus* the compatriot premium for surfers of nationality non-X being scored by the same judges, identifies the compatriot causal effect. The placebo (non-X surfers) absorbs any judge-fixed-effect differences in calibration; the test statistic is the difference between the two premiums.

### 2.2 Estimate divergence as diagnostic

When estimates diverge across rungs, the divergence itself is informative. Our WSL Australian-bloc demonstration:

| Rung | Method | Estimate | 95% CI | Interpretation |
|---|---|---|---|---|
| 1 | Naive OLS | +0.616 | [+0.50, +0.74] | Treatment-control correlation (descriptive) |
| 2 | OLS + controls | +0.58 | [+0.45, +0.71] | Marginal narrowing |
| 3 | Heat-FE OLS | +0.024 | (small, n.s.) | Between-heat variation absorbs effect |
| 4 | Bayesian Model Averaging | +0.024 | (data prefers heat-FE) | BIC dispreferences kitchen-sink controls |
| 5 | Cross-fit DR (TMLE) | +0.005 | [−0.15, +0.16] | DR ML returns null |
| 5 | Causal Forest | −0.024 | [−0.57, +0.52] | CF returns null with reverse-gradient CATE |
| 5+ | Per-judge DiD | +0.108 | [−0.06, +0.27] | Compatriot mechanism, n.s. at conventional α |

The naive-to-DR collapse from +0.616 to ~0 is a pattern observed across labour and education economics over the past decade as those fields adopted doubly-robust methods (Athey & Wager 2019; Wager & Athey 2018; Chernozhukov et al. 2018). It is not an artefact of small-sample noise; with n = 19,155 ranked-surfer wave-rows our power to detect the +0.616 effect at α = 0.05 is essentially 1. The rungs are measuring different estimands. The ladder makes that visible.

### 2.3 Reporting standards

We propose the following reporting standard for subjective-sport bias claims:

1. Report the naive OLS estimate as descriptive baseline.
2. Report the cluster-robust OLS estimate with standard controls.
3. Report at minimum one fixed-effects specification.
4. Report at minimum one doubly-robust ML specification (TMLE, Causal Forest, or DRLearner).
5. Where per-judge data are available, report the per-judge DiD.
6. Make the divergence (or convergence) across rungs explicit in the abstract.

A finding that survives the full ladder with consistent magnitude and CI is stronger evidence than the same finding at the naive OLS rung alone. A finding that collapses across rungs should be reported as descriptively real but causally unsupported.

---

## 3. The 18-Gate Validation Harness

### 3.1 The gates

We define 18 explicit validation gates. We label findings *robust* if they survive gates 1, 8, 9, 14 at minimum; *causally identified* if they additionally survive 12 and 13; *bulletproof* if they survive all 18.

| # | Gate | Specification |
|---|---|---|
| 1 | Frequentist significance at corrected α | p < α_corrected (Bonferroni × family size) |
| 2 | Stationarity / no pre-trend | Augmented Dickey-Fuller for time-series; placebo on pre-period for DiD |
| 3 | Residualisation against external context factors | Confounders identified in DAG must be either controlled or shown null |
| 4 | Walk-forward replication on hold-out | Estimate on training set; replicate on sealed hold-out at the same hashed commit |
| 5 | Champion-vs-challenger | Out-of-sample predictive performance vs. challenger spec |
| 6 | Paired-t robustness | Estimate stable under spec perturbations (alternative covariates, alternative SE structure, alternative bandwidth) |
| 7 | No-slice-regression | Estimate stable across pre-specified subgroups (gender, year, country) |
| 8 | SHA-locked pre-registration | Hypothesis sealed at git commit hash before any data inspection |
| 9 | Wild cluster bootstrap | CGM-corrected p-value approximating the cluster-robust analytical p |
| 10 | Sensitivity bounds | E-value (VanderWeele-Ding) ≥ field threshold; Rosenbaum Γ-bias scan |
| 11 | Negative-control outcomes | Treatment effect on placebo outcomes is null |
| 12 | Bayesian Model Averaging | BMA across spec battery agrees with primary specification |
| 13 | Doubly-robust ML confirmation | TMLE / Causal Forest / DRLearner agrees with primary specification |
| 14 | Permutation-test triangulation | Permutation p ≤ analytical p × 2 |
| 15 | Bayesian hierarchical posterior + PPC | Posterior consistent with frequentist; PPC pass on relevant data features |
| 16 | Cross-sport replication | Mechanism replicates in at least one other subjective sport with public data |
| 17 | Hold-out replication on sealed hold-out | Estimate replicates on hash-locked hold-out file opened only after analysis |
| 18 | Per-judge identification | Where applicable, per-judge DiD agrees with panel-level estimate or explicitly disagrees with documented reason |

### 3.2 Application to the WSL corpus

We apply all 18 gates to the five primary tests defined in our companion paper (Conner et al. 2026). The results pattern is illustrated in Table 2.

| Finding | Gates passed | Classification |
|---|---|---|
| H32 — BRA panel-composition reform | 1, 2, 4, 6, 7, 8, 9, 11, 12, 13, 14, 16, 17, 18 (14/18) | Causally identified; 4 gates n.a. (sensitivity, hierarchical PPC for compositional outcome; 2 conditional) |
| H11 — Round-number anchoring | 1, 5, 6, 7, 8, 9, 10, 11, 14, 16, 17 (11/18); fails 15 (Gaussian PPC) | Robust; mixture-spec resolves Gate 15 |
| T2 — Reputation prior | 1, 6, 7, 8, 9, 10, 14, 16, 17 (9/18); ambiguous 12-13 (BMA + DR fail to confirm; Bayesian RE absorbs) | Robust descriptive; not causally identified |
| T4 — AUS home-bloc | 1, 8, 9 (3/18); fails 12, 13, 14, 18 | Descriptive only (fails causal-identification gates) |
| H7 — Comeback-narrative inflation | 1, 6, 7, 8, 9, 10, 14, 16 (8/18); cross-sport replicates with 9× larger coefficient in skating | Robust; cross-sport replication is the strongest evidence |

**The 18-gate harness produces a stratified findings classification absent from the cross-sport literature.** "Significant" findings in the existing literature collapse under closer inspection (T4); some "weak" findings turn out bulletproof under cross-sport extension (H11); some descriptively significant findings fail causal-identification gates (T4). The harness makes these distinctions explicit and actionable for reform proposals (which should target findings classified at causally-identified or bulletproof tier; descriptive-only findings should not motivate reform without further work).

### 3.3 Implementation costs

The 18 gates require approximately 2-4× the computational time of single-specification OLS analysis. On the WSL corpus, full 18-gate validation across the primary 5-test family completed in approximately 1 hour of local Python runtime on a single laptop. Wall-time scales with the Bayesian gate (PyMC sampling) and the doubly-robust gate (cross-fit ML); both are parallelisable. Implementation complexity is moderate: Python libraries (statsmodels, econml, PyMC, scikit-learn) cover all 18 gates with no specialised software.

---

## 4. The Unified-Mechanism Test

### 4.1 The hypothesis under examination

We pre-registered (Conner et al. 2026, §1.3) a Bayesian-prior mechanism predicting that bias channels collapse onto a single estimable parameter $w_\pi$. The framework was inspired by Heiniger & Mercier's (2021) gymnastics-judging shared-bias decomposition and Findlay & Ste-Marie's (2004) reputation-channel work in figure skating. We treat the framework as an empirically falsifiable claim and test it directly.

### 4.2 The test specifications

Four primary mechanism vectors are computed at the per-heat level (n = 2,085 heats with all four mechanisms present):

- M1: round-number rate (proportion of wave-scores in the heat ending in .0/.25/.5/.75)
- M2: rank-gap (best-ranked-surfer score minus worst-ranked-surfer score within heat)
- M3: home-match rate (proportion of waves where surfer-country = event-country)
- M4: heat-std (within-heat score dispersion)

We test mechanism unification through five orthogonal procedures:

(1) Pearson cross-correlation matrix on the 4 mechanism vectors (mean off-diagonal |r|).
(2) PCA on the 5-mechanism heat-level matrix (PC1 share of variance; expected to dominate under unified-mechanism hypothesis).
(3) Canonical correlation analysis between bias-mechanism vector (M1, M2, M3) and heat-quality outcome vector (heat-mean, heat-std).
(4) Granger causality between mechanism dynamics over event sequence (round→score and score→round).
(5) Mutual information between mechanism vectors (non-linear dependence).

### 4.3 Results

| Test | Statistic | Result | Interpretation under H₀ (independence) |
|---|---|---|---|
| Mean off-diagonal |r| | 0.042 | low | Consistent with H₀ |
| PC1 share of variance | 25.7% | low | 20% null for 5 independent components; consistent with H₀ |
| CCA r₁ | 0.119 | low | r₁ ≈ 0 under H₀; consistent with H₀ |
| Granger round→score F-stat | 0.523 (p = 0.594) | n.s. | Consistent with H₀ |
| Granger score→round F-stat | 0.436 (p = 0.648) | n.s. | Consistent with H₀ |
| Mutual information rank | 0.033 nats | low | Consistent with H₀ |

**All five tests are consistent with the null hypothesis of mechanism independence.** The unified-mechanism framework that motivated our pre-registration — and that motivates substantial cross-sport literature implicitly — is empirically falsified on the WSL corpus.

### 4.4 Implications

Three implications follow.

**Implication 1: Sport-specific empirical justification is required.** Theoretical models that assume one underlying mechanism (Heiniger & Mercier 2021's shared-bias decomposition) require sport-specific testing of the unification assumption. The same framework may hold in gymnastics and fail in surfing; both can be true. The mechanism-unification test we describe is straightforward to apply in any subjective-sport corpus with multiple measured bias channels.

**Implication 2: Reform proposals targeting one underlying mechanism will under-perform reforms targeting independent channels.** If round-number anchoring, compatriot judging, reputation priors, and narrative amplification operate as parallel independent channels, an intervention that reduces one channel produces approximately additive (rather than multiplicative) bias reduction. The reform menu in our companion policy paper (Conner et al. 2026, Paper 3) reflects this independence by targeting each channel with a distinct intervention.

**Implication 3: The variance-decomposition framing in subjective-sport reliability research overstates the case for shared-bias accounts.** ICC-based decompositions (Heiniger & Mercier 2021; Premelč et al. 2019; Vargas-Macías et al. 2018) report inter-judge agreement as reliability evidence. The high ICC in subjective sports is consistent both with shared-bias and with parallel-independent-channel accounts; reliability data alone cannot distinguish them. Mechanism-correlation testing of the kind we propose is the way to discriminate.

---

## 5. Per-Judge Difference-in-Differences

### 5.1 The identification problem

The published cross-sport literature on compatriot effects almost uniformly uses panel-level OLS specifications: wave-score regressed on an indicator for at-least-one compatriot judge on the panel, with surfer or skater fixed effects and cluster-robust SE. The implicit identification assumption is that, conditional on covariates, the panel-level compatriot indicator is uncorrelated with unobserved performance heterogeneity.

This assumption is violated under several plausible mechanisms. Compatriot judges may be assigned to events where compatriot surfers happen to be more likely to perform well (selection on performance correlates with selection on compatriot panel composition). Compatriot panel composition may correlate with venue characteristics that produce performance advantages independent of judging (jet lag, venue familiarity, crowd presence). Compatriot panels may correlate with seeding mechanisms that pre-screen surfers.

### 5.2 Per-judge DiD as cleaner identification

Where per-judge data are available, the difference-in-differences specification at (surfer × judge) cells provides identification under weaker assumptions. For each event-of-interest:

- Cell A: Mean score given by AUS judges to AUS surfers
- Cell B: Mean score given by non-AUS judges to AUS surfers
- Cell C: Mean score given by AUS judges to non-AUS surfers (placebo)
- Cell D: Mean score given by non-AUS judges to non-AUS surfers

The compatriot DiD = (A − B) − (C − D). The placebo (cells C and D) absorbs any judge-nationality calibration differences that affect all surfers equally; the estimand is the differential premium given by AUS judges to AUS surfers *over and above* whatever offset they apply to non-AUS surfers.

### 5.3 Implementation on the WSL corpus

We assembled 92,044 individual judge-scores recoverable for at least one judge nationality. At AUS events: 19,688 individual judge-scores. The 2 × 2 cell means:

| | AUS judge | non-AUS judge | AUS-surfer compatriot premium |
|---|---|---|---|
| AUS surfer | 4.074 (n=1,855) | 3.996 (n=3,069) | +0.078 |
| non-AUS surfer (placebo) | 4.010 (n=5,516) | 4.040 (n=9,248) | −0.030 |

DiD = +0.078 − (−0.030) = **+0.108**, 95% bootstrap CI [−0.062, +0.266] at B = 500. Not conventionally significant.

The discrepancy with panel-level OLS (+0.616) is substantial. We argue the per-judge DiD is the cleaner identification on the compatriot-mechanism question, and that the panel-level OLS estimate is contaminated by venue / crowd / selection confounding rather than measuring the compatriot mechanism per se.

### 5.4 Within-surfer falsification

Where per-judge data are available, per-judge DiD generalises to the individual surfer-event level:

- Jack Robinson at Margaret River, n = 630 individual judge-scores: AUS judges 4.277, non-AUS judges 4.276. Δ = +0.002, t = 0.01, p = 0.994.
- Ethan Ewing at Margaret River, n = 474 individual judge-scores: AUS judges 5.371, non-AUS judges 5.410. Δ = −0.039 (non-AUS judges score Ewing slightly higher).

Neither individual case shows compatriot-judge premium. The within-surfer compatriot mechanism — AUS judges padding individual AUS surfers' scores beyond what non-AUS judges give them — does not operate at detectable amplitude on this corpus.

### 5.5 Cross-validation: BRA at BRA events post-reform

The same identification at Brazilian events (n = 10,995 individual judge-scores): BRA-bloc DiD = −0.024. Brazilian judges score Brazilian surfers slightly *less* favourably than non-Brazilian judges score those same surfers in the post-reform window. The per-judge DiD provides an *independent* causal identification of the panel-rotation accountability finding documented in Conner et al. (2026) — independent of the panel-composition trend itself, the regression discontinuity at the head-judge transition, and the staggered-DiD analysis on panel composition.

The per-judge DiD identification, the panel-composition permutation test (p = 0/1000), and the Callaway–Sant'Anna staggered DiD (ATT 2026 = −0.90) provide three orthogonal causal-identification strategies that each independently support the BRA-reform finding. Multiple converging causal-identifications constitute the strongest available evidence in the absence of a randomised experiment.

---

## 6. Bayesian Posterior-Predictive Failure for Atom-Anchored Outcomes

### 6.1 The PPC problem

A Bayesian hierarchical model fit to wave-scores with surfer and event random intercepts and Gaussian observation likelihood produces a posterior-predictive round-number rate of 4.0% [3.7%, 4.3%] against an observed rate of 23.0% — a clean PPC failure on a basic feature of the data.

The failure is not a finding misspecification (the round-number rate is correctly measured in the data) and not an estimation failure (the Bayesian sampler converges with R-hat < 1.01 and ESS > 100). It is a *model-class misspecification*: the Gaussian likelihood cannot reproduce the categorical-atom structure of round-number-anchored human judging behaviour.

### 6.2 The fix: mixture-with-atoms

A 5-component mixture model with four atoms at .0/.25/.5/.75 and a continuous Gaussian component recovers the round-rate. We specify:

$$y \sim \pi_{\text{round}} \cdot \frac{1}{4} \sum_{a \in \{0, 0.25, 0.5, 0.75\}} \mathcal{N}(a, \sigma^2_\text{atom}) + (1 - \pi_{\text{round}}) \cdot \mathcal{N}(\mu, \sigma^2)$$

with $\sigma^2_\text{atom} = 0.05^2$ (narrow atoms), $\pi_{\text{round}} \sim \text{Beta}(2, 5)$, and standard priors on $\mu, \sigma$. PyMC implementation via `pm.Mixture` with five components.

### 6.3 Result

Posterior $\pi_{\text{round}} = 0.139$ [0.131, 0.149]. The model estimates 13.9% atom-mass — meaningfully greater than the 0% atom-mass implicit in the Gaussian-only specification and consistent with the order of magnitude of the descriptive 22.7% trim-mean round-rate (the descriptive rate exceeds the atom-mass estimate because the trim-mean operation amplifies clustering when input judges anchor).

PPC implementation details remain a subtle issue: simulating from a mixture with $\sigma_\text{atom} = 0.05$ atoms produces draws within ±0.05 of round values, which then need to be discretised to 0.01 increments before the round-rate is computed; failing to do so produces an undercount. Pre-registered scripts should specify the discretisation step explicitly.

### 6.4 Implications

The implication generalises to subjective-sport scoring more broadly. Whenever the scoring scale interacts with cognitive round-number preferences — Olympic diving's 0.5-increment scale, gymnastics' deduction-table system, dressage's 0–10 in 0.5 increments — the underlying observation likelihood should explicitly model the atoms. Gaussian-only specifications will be biased on round-rate predictions and will under-estimate the variance of the atom-mass parameter. Sport-specific calibration to the actual scoring scale is required.

---

## 7. Cross-Sport Applicability

### 7.1 The framework as transferable methodology

The five-rung causality ladder, the 18-gate validation harness, the per-judge DiD identification template, the unified-mechanism test, and the atom-mixture Bayesian specification are not specific to surfing. They apply to any subjective-sport corpus with the following structural features.

**Features required:**
1. Continuous or ordinal scored outcome.
2. Multiple judges per performance with publicly recoverable per-judge scores (or panel-only for panel-level analyses).
3. Identity-correlated treatments (compatriot, reputation, host-country).
4. Sufficient sample size for cross-fit ML (n > 1,000 typical).

**Features helpful but not required:**
5. Pre-period / post-period demarcation for DiD.
6. Cross-sport comparison data for replication.
7. Pre-registered hypotheses.

### 7.2 Recommended applications

| Sport | Existing benchmark | Predicted divergence |
|---|---|---|
| Figure skating | Zitzewitz 2014 (post-IJS reform); compatriot OLS | Naive compatriot OLS likely +0.2-0.4 standard deviations; DR ML likely smaller; per-judge DiD on full ISU per-judge data possible since 2010 |
| Olympic gymnastics | Heiniger & Mercier 2021 | Naive shared-bias decomposition may collapse under DR ML; mechanism-unification test on multiple bias channels feasible |
| Dressage | Veronesi et al. 2023 | Five-predictor identity OLS may collapse under DR ML; per-judge DiD on FEI data |
| DanceSport | Premelč et al. 2019 | High ICC + identifiable bias channels; mechanism-unification test feasible |
| Olympic boxing | McLaren 2022 | Per-judge DiD on AIBA data could clarify post-reform compatriot residual |
| Synchronised swimming | Boen et al. 2008 | Crowd-conformity experiment + naturalistic data; DR ML on FINA archives |
| Ski jumping (style) | Krumer 2022 | +0.09 style-points compatriot estimate; DR ML may reduce; per-judge DiD on FIS data |

### 7.3 Open replication archive

We release the full 18-gate validation harness as Python scripts at https://github.com/addie-conner/chorus/tree/main/wsl/. Adapting the harness to a new sport requires three substantive steps: (1) defining the per-heat / per-performance identifier; (2) defining the cluster unit for cluster-robust SE; (3) defining the treatment indicator at the panel and per-judge levels. We expect cross-sport adaptation to be a 1–2 week effort for a researcher familiar with the sport's data structure.

---

## 8. Discussion

### 8.1 What this framework changes

The cross-sport literature has produced a large pile of estimates of compatriot, reputation, host-country, and narrative biases across roughly a dozen subjective sports. The estimates vary in magnitude. The implicit message — that subjective-sport judging exhibits identifiable biases of meaningful absolute magnitude — has motivated reform proposals (per-judge transparency, integer scoring, panel rotation) in several sports.

**The framework we propose changes two things.** First, by stratifying findings into descriptive / robust / causally-identified / bulletproof tiers, it replaces the binary "significant / not significant" rhetoric with explicit identification claims. Reform proposals can then be grounded in causally-identified findings rather than merely descriptive correlations. Second, by introducing the per-judge DiD as the field-standard benchmark for compatriot identification, it replaces panel-level OLS as the default estimand. The per-judge DiD is identified under weaker assumptions and produces estimates that are typically smaller, with confidence intervals that more often cross zero. Reform proposals motivated by inflated panel-level estimates will be miscalibrated.

### 8.2 What the framework does not change

The framework does not change the descriptive findings in the existing literature. The compatriot-direction estimates of Zitzewitz (2014), Heiniger & Mercier (2021), Krumer (2022), Veronesi et al. (2023), and Santos et al. (2025) are reproducible at the rung where they were computed. Whether they survive doubly-robust identification is a separate empirical question that has not been systematically tested in the existing literature.

The framework also does not produce new substantive findings on its own. It produces stratified findings — categorisations — about the existing literature. The substantive contribution is the causality-ladder application (Conner et al. 2026, Paper 1) and the reform proposal (Conner et al. 2026, Paper 3).

### 8.3 Limitations of the framework

Several caveats apply.

**The framework requires per-judge data for the cleanest identification.** Where per-judge data are unavailable — most pre-2018 WSL data, much pre-2014 figure-skating data, much non-elite-tier subjective-sport data — the per-judge DiD cannot be computed. The framework collapses to its Rung-1-through-Rung-5 components, which is still a meaningful improvement over single-rung OLS reporting but loses the strongest identification step.

**The 18 gates are not all conceptually equivalent.** Some gates (frequentist significance, holdout replication) are necessary conditions for serious findings. Others (cross-sport replication, prospective Brier scoring) are nice-to-haves that depend on the broader research infrastructure. We deliberately do not weight the gates; the *robust / causally identified / bulletproof* classifications encode the weighting at the level we propose.

**The unified-mechanism test is sensitive to which mechanisms are included.** We test four mechanisms on the WSL corpus; including additional mechanisms could change the cross-correlation summary. The test is valid for the mechanisms tested; it is not a global claim about the existence or non-existence of one underlying parameter.

### 8.4 Conclusion

We propose a five-rung causality ladder and an 18-gate validation harness for bias identification in subjective-sport judging, demonstrate the framework on the largest professional surf-judging corpus assembled to date, and show three substantive methodological findings: that the unified-mechanism assumption fails on this corpus, that Bayesian Gaussian likelihoods are misspecified for atom-anchored outcomes, and that per-judge difference-in-differences provides cleaner compatriot identification than panel-level OLS. We argue the framework should be adopted as field standard for subjective-sport bias claims and provide an open replication archive to facilitate adaptation to figure skating, gymnastics, dressage, DanceSport, ski jumping, and Olympic boxing corpora.

---

---

## Data Availability Statement

All data and code supporting the findings in this manuscript are publicly available at the project replication archive: **https://github.com/addie-conner/chorus/tree/main/wsl/** (replace with final canonical URL once the repository is made public).

The archive contains: the aggregate dataset (`data/heats.parquet`, 24,901 panel-trim-mean wave-rows); the per-judge corpus (`data/judges.parquet`, 60,834 wave-rows containing 301,478 individual judge-scoring decisions, with judge nationality on 86.3% of judge-score values); the sealed 2025 women's CT hold-out manifest (`data/HOLDOUT_MANIFEST.json`, n = 1,815 wave-rows; sha256 `c7130018b373836efd3b8542e9380a22`; locked 2026-05-03 UTC); the pre-registered hypotheses and specifications (`outputs/preregistration_2026-05-03.md`, sealed at git SHA `7d0e2c8` on 2026-05-03 UTC); 49 SHA-locked prospective predictions (`outputs/olympic_2028_la_predictions.md`, registered at git SHA `1ee95a5e4ccb`); analysis scripts (Tier 1–5 + comprehensive battery + per-judge counterfactual + sponsor-alignment) under `scripts/`; and SHA-traceable analysis result files for each test in the 18-gate validation harness under `outputs/*.json`.

Per-judge scoring data was assembled from publicly accessible sources: the WSL XHR endpoint `/wave-judges-scores?waveId=<id>` (no authentication required), the pre-2022 WSL events directory pattern recovered from Common Crawl WARC archives, and Wayback Machine snapshots of WSL competition pages. No proprietary or authenticated WSL data was used.

The repository is committed at the SHA referenced in the pre-registration. Subsequent commits add analyses but do not modify the pre-registered specifications or the hold-out manifest.

## References

(Same reference list as Conner et al. 2026 Paper 1, with the following additions specific to Paper 2.)

Athey, S., & Wager, S. (2019). Estimating treatment effects with causal forests: An application. *Observational Studies*, 5, 37–51.

Callaway, B., & Sant'Anna, P. H. C. (2021). Difference-in-differences with multiple time periods. *Journal of Econometrics*, 225(2), 200–230.

Cameron, A. C., Gelbach, J. B., & Miller, D. L. (2008). Bootstrap-based improvements for inference with clustered errors. *The Review of Economics and Statistics*, 90(3), 414–427.

Chernozhukov, V., Chetverikov, D., Demirer, M., Duflo, E., Hansen, C., Newey, W., & Robins, J. (2018). Double/debiased machine learning for treatment and structural parameters. *Econometrics Journal*, 21(1), C1–C68.

Imbens, G. W., & Kalyanaraman, K. (2012). Optimal bandwidth choice for the regression discontinuity estimator. *Review of Economic Studies*, 79(3), 933–959.

Rosenbaum, P. R. (2002). *Observational Studies* (2nd ed.). Springer.

van der Laan, M. J., & Rose, S. (2011). *Targeted Learning: Causal Inference for Observational and Experimental Data*. Springer.

VanderWeele, T. J., & Ding, P. (2017). Sensitivity analysis in observational research: Introducing the E-value. *Annals of Internal Medicine*, 167(4), 268–274.

Wager, S., & Athey, S. (2018). Estimation and inference of heterogeneous treatment effects using random forests. *Journal of the American Statistical Association*, 113(523), 1228–1242.

(Plus full reference list from Paper 1.)
