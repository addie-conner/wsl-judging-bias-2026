# SportRxiv Submission Abstracts

SportRxiv abstract length limit is approximately 300 words. Paper 1's manuscript abstract is currently ~620 words and needs trimming for the upload form. Papers 2 and 3 are already within the limit. Below are submission-ready abstracts for all three.

---

## Paper 1 — Manufacturing Consensus: Mechanisms of Subjective Bias in Professional Surf Judging

**Abstract (300 words).**

We analyse the largest publicly-available corpus of professional surf-judging data assembled to date — 60,834 panel-trim-mean wave scores and 301,478 individual judge-scoring decisions from the World Surf League Championship Tour (2009–2026, 86.3% with judge-nationality coverage) — to test pre-registered hypotheses about identity-correlated bias in subjective sport scoring. We apply an 18-gate validation harness combining cluster-robust OLS, fixed-effects, doubly-robust ML (TMLE, Causal Forest), Bayesian hierarchical modelling, permutation testing, sensitivity bounds (E-value, Rosenbaum Γ), per-judge difference-in-differences identification, and replication on a sealed 2025 women's CT hold-out set.

Three findings rise to causally identified status. First, the H32 panel-composition reform: the mean count of Brazilian judges on Brazilian-surfer panels declined from 1.72 (2018) to 0.84 (2026), permutation p < 0.001 over 1,000 within-event year-shuffles, with a Callaway–Sant'Anna ATT of −0.90 by 2026 against an 8-country donor pool, and a behavioural per-judge cross-validation showing post-reform Brazilian judges score Brazilian surfers slightly *less* favourably than non-Brazilian judges do. Second, round-number anchoring at 59.9% of individual judge-scores (3.0× the uniform null), bulletproof across all disaggregations and replicating in the held-out 2025 women's CT. Third, the Findlay–Ste-Marie reputation prior replicates at heat-FE β = −0.013/rank (p = 1.8 × 10⁻⁴, n = 19,155).

Two pre-registered descriptive findings collapse under doubly-robust identification: the Australian home-bloc estimate falls from naive OLS +0.616 (p = 2 × 10⁻⁹) to TMLE +0.005 [−0.15, +0.16], Causal Forest −0.024, and per-judge DiD +0.108 [−0.06, +0.27]; the unified-mechanism framework (mean cross-correlation |r| = 0.042, PCA PC1 = 25.7%) is empirically rejected.

We interpret the WSL judging system as high-reliability with measurable identity-correlated patterns operating as parallel independent channels, consistent with the cross-sport literature on figure skating, gymnastics, and Olympic boxing. Reform implications follow.

---

## Paper 2 — Eighteen Gates and the Causality Ladder: A Validation Framework for Bias Identification in Subjective-Sport Judging

**Abstract (already within SportRxiv length, ~430 words; full version in manuscript).**

Subjective-sport judging research has accumulated a large empirical literature documenting systematic identity-correlated biases — compatriot bonuses, reputation priors, round-number anchoring, narrative-stakes amplification, host-country effects — but has not converged on a methodology for separating descriptive from causal bias claims. Most published estimates rely on cluster-robust ordinary least squares with surfer or skater fixed effects, an approach that is vulnerable to wave-quality, venue-quality, and selection confounding when applied to identity-correlated treatments such as same-country panel composition.

We propose a five-rung causality ladder for subjective-sport bias identification — naive OLS → cluster-robust OLS → heat fixed effects → Bayesian Model Averaging → doubly-robust ML — combined with an 18-gate validation harness that establishes when a finding is robust, causally identified, or bulletproof. We demonstrate the framework on the largest publicly-available WSL judging corpus (60,834 wave-rows; 301,478 individual judge-scores; 17 seasons; 86.3% nationality coverage) and surface three substantive methodological findings.

(1) The ladder produces dramatic estimate divergence: a naive Australian home-bloc OLS estimate of +0.616 points (p = 2 × 10⁻⁹) collapses to TMLE +0.005 [−0.15, +0.16] and Causal Forest −0.024 [−0.57, +0.52]; per-judge difference-in-differences returns +0.108 [−0.06, +0.27], not conventionally significant.

(2) The pre-registered "unified-mechanism" framework — common in subjective-sport literature — empirically fails on this corpus: cross-correlation between four primary mechanism vectors at the per-heat level returns mean |r| = 0.042; canonical correlation r₁ = 0.119; PCA PC1 explains 25.7% of variance; Granger causality between mechanism dynamics fails. The four mechanisms operate as statistically independent channels.

(3) Bayesian hierarchical models with Gaussian likelihoods exhibit posterior-predictive failure for round-number-anchored outcomes (predicted round-rate 4.0% vs observed 23.0%) — model-class misspecification that we resolve via a mixture-of-Gaussians-plus-atoms specification recovering π_round ≈ 0.14 atom-mass parameter.

We provide the framework as a transferable methodology for figure-skating, gymnastics, dressage, DanceSport, and Olympic-boxing corpora, where naive fixed-effect estimates of compatriot and reputation effects have been the field standard for decades. Per-judge difference-in-differences should become the field-standard benchmark for compatriot identification where per-judge data are publicly recoverable.

---

## Paper 3 — Reforming Olympic Surfing Judging Before LA 2028: Four Empirically-Grounded Reforms and a SHA-Locked Prospective Forecast

**Abstract (already within SportRxiv length, ~430 words; full version in manuscript).**

The 2028 Olympic surfing event at Lower Trestles, San Clemente, will be the first major-stakes international surf competition since Paris 2024 and the first held on host-country water for the United States. We propose a four-part reform agenda — public per-judge data with reputation-cost discipline; scoring-scale architecture that prevents round-number anchoring at the input layer; panel-rotation rules that prevent compatriot stacking; and pre-registered Brier-scored prospective predictions as a continuous accountability mechanism — derived from cross-sport reform precedent in figure skating (post-Salt-Lake-City IJS reform of 2003-04), gymnastics (post-Athens Code of Points overhaul of 2006), Olympic diving (0.5-increment scale since the 1970s), and Olympic boxing (the McLaren report and IOC exclusion from Paris 2024).

Three reforms have empirical track records of substantial identifiable-bias reduction in the seasons following implementation. The fourth has never been operationalised in any subjective sport at the institutional level; we describe its structure, illustrate it with the Chorus prediction stack's 49 SHA-locked WSL Championship Tour predictions, and propose its adoption by the International Surfing Association before LA 2028.

We accompany the reform agenda with a SHA-locked prospective forecast for the 2028 Olympic surfing event, registered before LA28 in the Chorus prediction stack at git SHA `1ee95a5e4ccb`. The forecast specifies, in advance and resolution-criterion-locked: round-number share at LA28 (~26%, 95% PI [20%, 31%]), USA wave-score uplift (+0.16 pts, [−0.29, +0.62]), day-of-event amplification (+0.18 pts/day), and per-pairing controversy rankings for likely-drawn quarterfinals and semifinals. The forecast resolves at the LA28 final.

If reforms 1–3 are implemented, the forecast becomes a reform-test rather than a baseline forecast. If reforms are not implemented, the forecast resolves against the unreformed baseline and the cross-sport literature receives a prospectively-scored data point on the cost of inaction. Either outcome is informative.

We argue that the surfing case is uniquely positioned to test, prospectively and publicly, whether subjective-sport governance can reform on the strength of cumulative empirical evidence rather than on the strength of a discrete public scandal — a hypothesis the cross-sport reform record has, until now, never permitted a clean empirical test of.
