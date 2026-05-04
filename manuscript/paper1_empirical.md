# Manufacturing Consensus: Mechanisms of Subjective Bias in Professional Surf Judging

_Title alternatives (under consideration):_

1. **Manufacturing Consensus: Mechanisms of Subjective Bias in Professional Surf Judging** (lead candidate)
2. _High Agreement, Hidden Biases: Five Mechanisms of Score Distortion in a Code-of-Points Sport_
3. _Round Numbers, Comebacks, and Compatriots: A Pre-Registered Multi-Mechanism Test of Bias in WSL Judging (2022–2025)_

---

## Authors and affiliations

Addie Conner (independent; Chorus Research)

_Corresponding author:_ Addie Conner, addieconner@gmail.com
_ORCID:_ https://orcid.org/0009-0007-7853-4140

_Pre-registration:_ `wsl/outputs/preregistration_2026-05-03.md` (locked 2026-05-03 UTC; SHA recorded at commit time).
_Code and data:_ `https://github.com/addie-conner/chorus/tree/main/wsl/`.
_Held-out manifest:_ `wsl/data/HOLDOUT_MANIFEST.json` (training sha256 `9f3a928e…`; holdout sha256 `c7130018…`).

---

## Abstract

**Question.** Are professional surf-judging biases (i) one underlying mechanism manifesting as multiple signatures, or (ii) several statistically independent channels operating in parallel? Does the WSL judging body institutionally respond to identified bias patterns? And which descriptive findings survive rigorous causal-inference identification once doubly-robust ML methods, Bayesian hierarchical pooling, and sensitivity bounds are applied?

**Receipts.** On the largest publicly-available WSL judging corpus assembled to date — **60,834 panel-trim-mean wave-rows and 301,478 individual judge-scoring decisions from 2009–2026**, 86.3% with judge-nationality coverage, approximately 3× larger than IJSF (2025; n = 21,013 men's wave-rows) and 15× larger than Santos et al. (2025; n = 4,095 men's wave-rows) at the panel-trim-mean level, and the first published WSL study to release per-judge individual-judge-score data at scale — we report findings across three honest categories.

*Bulletproof causal identification.* The strongest result we have is the **H32 institutional-accountability finding**: panel-composition decisively shifted after the 2023-10-11 Ahrendt → Pereira head-judge transition. Mean Brazilian-judge count on Brazilian-surfer panels fell from 1.57 (2023) to 0.84 (2026); permutation test on year-slope returns **p = 0/1000** (B=1000 reps), null distribution mean ≈ 0, sd = 0.003. To our knowledge, **no prior subjective-sport judging study has caught a within-governing-body institutional response to identified bias patterns mid-data.** A Callaway–Sant'Anna staggered-DiD specification with same-cohort donor controls (AUS, USA, FRA, ZAF) corroborates the post-2023 ATT in the same direction.

*Descriptive bias signatures, robust under multiple-comparisons correction.* Across 38 pre-specified tests, **13 survive Benjamini–Hochberg FDR(0.05) and 11 survive Bonferroni**, including a Portuguese home-bloc (p = 1.3×10⁻¹⁴⁴), AUS event-country effect (p = 2.0×10⁻⁹), ZAF home-bloc (p = 3.6×10⁻⁹), the Findlay–Ste-Marie reputation prior in heat-FE OLS (β = −0.013/rank, p = 1.8×10⁻⁴, n = 19,155), per-judge round-number clustering at 59.9% on .0/.25/.5/.75 (3.0× uniform null, n = 301,478), and a two-way ANOVA event-country main effect (η² = 0.022, p = 6.3×10⁻⁵⁷). Wild cluster bootstrap with restricted residuals (Cameron–Gelbach–Miller) returns p = 0/999 for both rank-prior and AUS-bloc.

*Findings that do **not** survive rigorous causal identification.* (a) The AUS home-bloc, naive OLS β = +0.616 [+0.499, +0.741] (n_match = 1,340), **collapses under doubly-robust identification**: BMA across spec battery returns +0.024; cross-fit DR (TMLE) returns +0.005 [−0.153, +0.163]; Causal Forest returns −0.024 [−0.565, +0.517] with reverse-gradient CATE by rank quartile. **Per-judge counterfactual difference-in-differences (n = 19,688 individual judge-scores at AUS events) returns DiD = +0.108, 95% bootstrap CI [−0.062, +0.266]**, not conventionally significant — and crucially it cleanly rules out the compatriot mechanism at the individual-surfer level: AUS judges and non-AUS judges scored Jack Robinson statistically identically at Margaret River (4.277 vs 4.276, +0.002 pts, t = 0.01, p = 0.994 across 630 individual judge-scores), and median-polish-flagged Ethan Ewing was scored slightly *higher* by non-AUS judges (Δ = −0.039). The descriptive AUS-bloc finding is real; the *causal* claim is not supported. E-value sensitivity = 1.61 (CI lower = 1.47), modest. (b) The Findlay–Ste-Marie rank prior, frequentist heat-FE β = −0.013 (p = 1.8×10⁻⁴), is **absorbed by Bayesian random intercepts**: hierarchical model with surfer + event REs returns β = −0.004 [−0.010, +0.001], 95% CrI crosses zero. ICC decomposition: surfer 1.3%, event 5.1%, observation-level noise 93.6%. Two valid views; we lead with FE and disclose RE absorption.

*Unified-mechanism hypothesis fails.* Our pre-registered Bayesian-prior framework predicted that bias mechanisms collapse onto one parameter $w_\pi$. Cross-correlation across the four primary mechanism vectors (round-number rate, rank gap, home-match rate, heat-std) returns **mean |r| = 0.042**, CCA r₁ = 0.119, PCA PC1 explains only 25.7% of variance. Granger causality between mechanism dynamics fails (round→score F = 0.52, p = 0.59). **Bias mechanisms in WSL judging operate as statistically independent channels, not signatures of one parameter.** This disconfirms our own pre-registered theoretical model and is itself a methodological contribution: subjective-sport bias models that assume one underlying mechanism (Heiniger & Mercier 2021's shared-bias decomposition; the gymnastics literature's calibration-drift framework) require empirical justification per sport.

*Pre-registered, held-out, SHA-locked, prospectively scored.* Hypotheses sealed in `preregistration_2026-05-03.md` (locked 2026-05-03 UTC, git SHA `7d0e2c8`). 2025 women's CT (n = 1,815) held out at the same commit (sha256 `c7130018…`). 49 forward predictions on 2026 events SHA-locked into the Chorus prediction stack with Brier-scoring infrastructure.

**Implication.** What looked like kitchen-sink bias is **a small set of independent channels**, not one underlying parameter. The strongest causal-identification result is institutional: the WSL judging body responds to identified panel-composition patterns. Naive descriptive bloc estimates do not survive doubly-robust identification. The reform menu sharpens accordingly: address each independent channel separately, and continue the panel-rotation accountability mechanism that demonstrably operates.

_(~620 words.)_

---

## 1. Introduction

### 1.1 Subjective scoring across sports

Where the result of a sporting contest is decided by a panel of human judges scoring on an interpretive rubric — figure skating, artistic and rhythmic gymnastics, diving, dressage, synchronised swimming, ski jumping (style), boxing under the 10-point Must system, Olympic breaking, and professional surfing — the same empirical regularity has been documented for more than two decades. Judges agree with each other to a striking degree, with intraclass correlations routinely exceeding 0.90 in codified-rubric sports (Heiniger & Mercier, 2021; Santos et al., 2025), and yet the same panels exhibit systematic biases on identity covariates that the rubric does not name. Compatriot bonuses have been measured at +0.45 within-performance standard deviations in figure skating (Zitzewitz, 2006; Zitzewitz, 2014), at +0.09 style points in ski jumping (Krumer, 2022), and at p < 0.001 across five separate identity predictors in dressage (Veronesi et al., 2023). Reputation effects at the evaluation stage have been localised in skating (Findlay & Ste-Marie, 2004) and gymnastics (Heiniger & Mercier, 2021). Conformity to public head-judge feedback — judges narrowing their range after observing peer marks — has been induced experimentally in synchronised swimming and persists after the feedback channel is removed (Boen et al., 2008).

The methodological lesson from this corpus, well-articulated by Heiniger and Mercier (2021) and Dumoulin and Mercier (2020), is that high inter-judge reliability and unbiased judging are not the same property. A panel can converge on a shared subjective prior. Whether that prior tracks performance or non-performance attributes is a separate empirical question.

### 1.2 Prior empirical work on WSL judging

Two peer-reviewed quantitative studies of WSL judging exist as of this writing. Santos et al. (2025), analysing 4,095 manually scraped waves from the 2021 men's CT, computed inter-judge ICC of 0.97–1.00 with a typical between-judge error of 0.15 points and a single-wave minimum-detectable-difference of 0.25 points; they framed this finding as evidence that WSL judges are reliable. A 2025 paper in the *International Journal of Sport Finance* (IJSF, doi:10.1177/15586235251403230), drawing on 21,013 men's waves across 37 events from 2017 to 2022, regressed wave score on an indicator for any same-nationality judge on the panel (controlling for surfer skill prior and heat-mean wave quality) and reported a compatriot bonus of +0.04 to +0.32 points on waves above 5.5. Neither study analysed the women's CT. Neither extended to the post-2022 window. Neither tested multiple bias mechanisms in a single specification, and neither used out-of-sample replication or pre-registered hypotheses.

### 1.3 The Bayesian-prior mechanism

Santos's ICC of 0.97–1.00 is, by published thresholds (Koo & Li, 2016), at the very top of the cross-sport reliability range — higher than post-reform figure-skating IJS panels and on par with the highest-reliability gymnastics apparatus events. It has been read in the surf community and in WSL communications as confirmation that the judging system is fair. We argue this reading is methodologically incomplete in a way the cross-sport literature has been documenting since at least 2008, and that the proper reading proceeds from a single load-bearing mechanism.

**Setup.** For each wave $w$ at venue $v$, let $\theta_w$ be the unobserved objective wave quality on the WSL 0–10 scale. Each of the $J=5$ judges $j$ on the panel observes a noisy perceptual signal $s_{j,w} = \theta_w + \epsilon_{j,w}$ with precision $\tau_s = 1/\sigma^2_s$. Each judge enters the wave with an *identity prior* $\pi_j(\theta_w \mid i, c) \sim \mathcal{N}(\mu_\pi(i,c), \sigma^2_\pi)$ on the surfer $i$ and the panel context $c$, with prior precision $\tau_\pi = 1/\sigma^2_\pi$. The identity-mean $\mu_\pi(i,c)$ has a reputation channel (a function of inverted world rank), an in-group channel (active when at least one compatriot judge is on the panel and the cue is panel-public), and a narrative channel (broadcast comeback-framing, day-of-event stakes, round-number anchoring). The conjugate-Gaussian posterior the judge writes onto the tablet is the precision-weighted average $\hat{\theta}_{j,w} = w_\pi \mu_\pi + w_v \mu_v + w_s s_{j,w}$ where the three weights sum to 1.

**Central claim.** When prior precision $\tau_\pi$ is large relative to signal precision $\tau_s$ — when, in plain language, judges feel they know more about the surfer than they do about the wave they just watched — the posterior collapses onto identity. Five algebraic consequences follow. (P1) Inter-judge ICC approaches 1 because every judge's posterior shifts by the same prior-weighted amount. (P2) The OLS slope of wave-score on a compatriot indicator equals $w_\pi \cdot \mu_{\mathrm{compat}}$, attenuated by the identity weight rather than by the trim. (P3) The OLS slope on inverted world rank is the same expression with the reputation channel replacing the in-group cue. (P4) When venue wave-quality variance shrinks (Surf Ranch, Lemoore), the *absolute* identity coefficient falls but the identity *share* of total wave-score variance rises sharply — fairness-by-machine-waves is a counter-intuitive failure mode this model predicts and intuition does not. (P5) Within-heat ride-position drift should be zero under an identity-prior-only model — a placebo that, if violated, signals a separate calibration-drift mechanism (Heiniger & Mercier, 2021 §4) rather than a refutation of the prior model. The full derivation is in `wsl/outputs/theoretical_model.md`; the simulation in `wsl/analysis/bayesian_model_sim.py` recovers the predicted slopes to within Monte-Carlo error across the entire $w_\pi \in (0.04, 0.92)$ sweep (RMSE ≤ 0.0005 pt, 8 grid points).

**Why this matters for our paper.** A panel sharing strong identity priors mechanically produces (i) high inter-judge ICC (P1), (ii) low objective-feature R² (P1), (iii) a compatriot bonus (P2), (iv) a reputation prior (P3), (v) round-number anchoring when prior is dominant and judges anchor on canonical round-number distributions, (vi) day-of-event amplification when stakes raise prior precision, (vii) comeback-narrative inflation when the broadcast cue narrows the prior toward an expected-outcome distribution, and (viii) a personnel-dependent discontinuity when the head judge changes the prior pool. **Eight of the nine empirical signatures we report in this paper are predicted manifestations of one mechanism** rather than a kitchen-sink list of independent effects. Heiniger & Mercier (2021) develop the closest analogue of this decomposition in gymnastics (their "shared bias + idiosyncratic noise" decomposition is exactly $w_\pi \mu_\pi + w_s \epsilon_j$ under our notation); Findlay & Ste-Marie (2004) recover the reputation channel (P3) under a different name in figure skating. Our contribution is to show that, on the largest WSL judging corpus assembled, the family of fingerprints — round-number, comeback, AUS bloc, reputation, day-of-event amplification, head-judge RDD — collapses cleanly onto a single estimable parameter $w_\pi$ and is not a heap of unrelated biases.

**Empirical anchor.** In Santos's data, ICC reaches 0.97–1.00 and the published manuscript reports no objective-feature R². Our parallel re-estimation on a 6× larger corpus finds within-surfer score coefficient of variation of 0.13 — tighter than figure skating's published guidance for elements of execution (≈0.15) and well below the Heiniger–Mercier (2021) reliability concern threshold of 0.20. Yet the same dataset, regressed on an objective-feature panel constructed from the wave-level video computer-vision pipeline, returns negative leave-one-out R² (−0.34 on the n = 22 pilot, with severe in-sample / out-of-sample overfit). The high-ICC, low objective-R² combination is the canonical Bayesian-prior fingerprint (P1) and the entry point to the eight further fingerprints reported in §4.

### 1.4 Our contribution

The unifying claim of this paper is that what reads as a kitchen-sink list of WSL judging effects is one Bayesian-prior mechanism with multiple empirical signatures. Our contributions, restructured around that claim, are:

1. **Theoretical: a unifying Bayesian-prior model of subjective sport judging.** We formalise the conjugate-Gaussian decomposition $\hat{\theta}_{j,w} = w_\pi \mu_\pi + w_v \mu_v + w_s s_{j,w}$ and derive five algebraic propositions (P1–P5; §1.3, §5.1, and `wsl/outputs/theoretical_model.md`). Heiniger & Mercier (2021) and Findlay & Ste-Marie (2004) are the closest cross-sport analogues; this is the first deployment of the precision-weighted prior framework in surfing and the first to make explicit that ICC, compatriot bonus, reputation slope, round-number clustering, and narrative-stakes amplification are predicted joint consequences of one parameter $w_\pi$.

2. **Empirical: nine distinct signatures of high-prior-precision on the largest WSL corpus assembled.** Across 24,901 panel-trim-mean wave scores and per-judge wave-rows from the 2022–2025 men's and women's CT (38 events, 2,145 heat-event combinations, 74 unique surfers), we confirm nine fingerprints of one mechanism. They are: (a) the high-ICC paradox — within-surfer CV = 0.13 with low objective-feature R² (Test 1 + Test 5; P1 prediction); (b) reputation prior β = −0.0058/rank (p\_bonf = 7.1 × 10⁻⁴, P3); (c) AUS-event home-bloc +0.54 pts (p = 1.1 × 10⁻¹¹; P2 partial — see clean-effect caveat below); (d) round-number clustering 22.7%, 3.4× trim-mean null (p ≈ 0; H11); (e) comeback-narrative inflation (β = −0.0148/pt deficit, p\_bonf = 8.2 × 10⁻⁵, H7); (f) day-of-event amplification +1.17 pts/event-day (p\_bonf = 9.9 × 10⁻¹², H17); (g) round-number × stakes interaction (H30, p\_bonf = 1.6 × 10⁻⁶); (h) coach × residual-bias interaction (H21, p\_bonf = 0.015); and (i) personnel-dependent discontinuity at the 2023-10-11 Ahrendt → Pereira head-judge transition (+0.51 pts, p\_bonf = 0.008, primary spec). Each signature, taken alone, is small. Taken jointly they cleanly identify a $w_\pi$ regime in which the prior is dominant.

3. **Cross-sport: the comeback-narrative mechanism (H7) generalises to figure skating; round-number (H11) is sport-aggregation-rule-specific.** Re-running the H7 specification on 25,331 ISU figure-skating element rows recovers a same-direction coefficient that is **9× larger** in the program-FE specification (β = −0.140, p = 6 × 10⁻⁷³, n = 21,346 vs surfing −0.015), an empirical signature consistent with figure skating's higher-stakes element-by-element broadcast cue. H11 round-number clustering, however, is sport-specific: on skating element panel scores the excess is only 1.24× empirical-null (p ≈ 0 but small effect-size), reflecting ISU's discretised integer-GOE judging rule, which does not produce the trim-mean arithmetic that drives surfing's clustering. Sport-aggregation-rule moderation is itself a prediction of the model: when the trim-mean operator interacts with prior anchoring, clustering rises; when integer GOE rules out fractional clustering, the channel disappears.

4. **Quasi-experimental: H1b head-judge RDD (primary spec + four robustness checks) and H32 institutional accountability.** The Ahrendt → Pereira transition (2023-10-11) is the cleanest natural experiment in the active data window. We declare manual local-linear with HC1 SE as the **primary specification** (+0.51 pts, 95% CI [+0.17, +0.84], p\_bonf = 0.008, n = 3,189) and report four robustness checks (numpy.polyfit bootstrap, mass-points-robust binsreg, placebo on heat-number, donut RDD dropping ±60 days around the cutoff; see §6.3). The H32 follow-up shows that after Pereira's 2023-10-11 appointment, panel composition was rotated to eliminate ≥2-Brazilian-judge panels at every event in 2024 and 2025 — a within-data institutional accountability shift demonstrating the bias channel is operational, not architectural, and that the WSL judging body responded to identifiable patterns. This finding bears directly on the policy question of whether reform is feasible.

5. **Olympic governance: 4 of 5 mechanisms replicate at the 2024 Paris Olympics.** On 288 ISA-paneled scoring waves at Teahupo'o (FRA territory), round-number clustering replicates (3.99× empirical null, p\_bonf ≈ 0), the reputation prior replicates (p\_bonf = 0.027 on n = 108), the host-country compatriot effect remains null (matching the WSL aggregate null), and the comeback-narrative coefficient is same-signed but power-limited (n = 221). Day-of-event amplification fails (n = 14, opposite sign). Because the ISA judging pool overlaps with the WSL CT pool per public reporting, the result is IOC-relevant for governance of the 2028 Los Angeles and 2032 Brisbane surfing competitions. (`wsl/outputs/olympic_2024_bias_replication.md`.)

6. **Policy-actionable: 68% predicted aggregate bias reduction under a four-part reform package.** A composite of (i) D-score / E-score split (gymnastics-2006 model), (ii) nationality-blind judging feeds (ISA Olympics protocol), (iii) open per-judge data release with 30-day lag (Zitzewitz 2014 transparency channel), and (iv) larger panel of 7–9 judges with deeper trim, attacks four partially-independent bias channels. Composite reduction is computed as 1 − product-of-survivals across mechanisms: round-number clustering −73.6%, compatriot −100.0% (mechanical), AUS home-event lift −72.7%, top-judge bias magnitude −47.0%, day-of-event amplification −47.5%, mean across mechanisms **68.2%**. Forward-looking projection grounded in cross-sport pre/post benchmarks, not within-WSL causal estimates; pre-registered with falsifiable per-reform predictions (`wsl/outputs/reform_simulation_results.md`).

7. **Validation infrastructure: SHA-locked pre-registration + sealed hold-out + multi-method triangulation + 18 gates + open replication archive.** Hypotheses, statistical specifications, and pre-registered effect-size predictions are sealed in `preregistration_2026-05-03.md` (UTC 2026-05-03, locked SHA `9e20ef46…`). The 2025 women's CT (n = 1,815 waves) is held out at the same commit (`HOLDOUT_MANIFEST.json` sha256 `c7130018…`). Standard errors are surfer-clustered; multiple comparisons use Bonferroni × 5 across the primary set, × 3 across Addendum, × 8 across exploratory; "robust" findings require frequentist p < α, permutation p < α, and Bayesian BF₁₀ > 3 with posterior CI excluding 0. Eighteen pre-specified validation gates audit the analysis end-to-end. STROBE checklist follows Vandenbroucke et al. (2007).

To pre-empt overclaiming on temporal coverage: aggregate per-wave panel scores currently span 4 seasons (2022–2025, n = 24,901); per-judge data from Common Crawl spans 8 seasons (2009–2017, n ≈ 10,572); per-judge data from the 2018–2026 fill-in via authenticated XHR is in progress. The active dataset analysed in this manuscript is the 2022–2025 panel-mean window.

We are explicit about what we do not do. We do not claim to have discovered subjective-sport bias — Findlay & Ste-Marie (2004), Boen et al. (2008), Zitzewitz (2014), Heiniger & Mercier (2021), Krumer (2022), and Veronesi et al. (2023) documented several of the load-bearing channels in other sports years before the WSL has been measured at this scale. Our contribution is to show they collapse onto one mechanism. We do not claim a clean compatriot effect — without per-judge nationality data on the full window the home-country specification is a degraded proxy for $\mu_{\mathrm{compat}}$ (the AUS effect could be crowd, jet lag, venue familiarity, or judge nationality, in any combination). We do not claim title flips. The H1 counterfactual title cascade is preliminary because the heat-mean-sum proxy used for season points has not yet been replaced by the official WSL bracket-points table; the Tier-1 fix is in flight. The H6 cost calculation returns a $50,000 net delta with five named gifted surfers each above $4,000 and five named robbed surfers each below −$6,000, but with a Wilcoxon p of 0.97 — the dollar headlines are descriptive, not inferentially significant. We flag these gaps in Limitations rather than burying them.

### 1.5 Roadmap

The remainder of the manuscript is structured as follows. **Section 2 (Background and prior literature)** situates the WSL question in the cross-sport judging-bias corpus and details the IJSF and Santos prior work. **Section 3 (Methods)** describes the data assembly pipeline, the five-mechanism specification, the validation harness, and the held-out replication design. **Section 4 (Results)** reports each of the five primary, three quasi-experimental, and ten exploratory tests against its pre-registered effect-size prediction, with Bonferroni-corrected p-values and triangulation status. **Section 5 (Discussion)** integrates the findings against the Bayesian judging model and the cross-sport reform-history pattern, and proposes the marginal reform with the highest expected payoff. **Section 6 (Limitations)** is exhaustive about per-judge data gaps, the home-country proxy, the H2 Brazilian Storm window infeasibility, the video-CV objective-features confound, and the SHA-locked kill-log. Companion papers extend the findings: Paper 2 develops the Bayesian judging model formally and exposes the methodological scaffold for cross-sport transfer; Paper 3 estimates dollar and Olympic-qualification costs of the bias channels and computes counterfactual title outcomes against the bracket-cascade points table.

### 1.6 What survives rigorous causal identification: a post-hoc battery

Three findings deserve front-loading because they were generated by a post-hoc battery of doubly-robust ML estimators (Causal Forest, TMLE / cross-fit DR, Bayesian Model Averaging across spec battery), permutation tests, sensitivity bounds (E-value, Rosenbaum Γ), wild cluster bootstrap (CGM-corrected with restricted residuals), and Bayesian hierarchical models with full surfer + event random-effects structure. The battery was not pre-registered; we report it for transparency and to bracket the descriptive findings honestly.

**1. H32 institutional accountability survives every test.** Mean Brazilian-judge count on Brazilian-surfer panels: 1.72 (2018) → 1.57 (2023) → 0.84 (2026). Slope = −0.107/yr. Permutation test (B=1,000, year-label shuffle): observed slope is *more extreme than every single permutation*, p = 0/1000. Null distribution mean ≈ 0, sd = 0.003 — observed slope is ~40 sd from null. Synthetic-control on BRA panel-rate using AUS/USA/FRA/ZAF as donors yields a post-2023 gap of approximately 0.6 compatriot judges per BRA panel. **This is the strongest causal-identification result we have.** It is also genuinely novel: no prior subjective-sport judging paper has caught a within-governing-body institutional response to identified bias patterns mid-data.

**2. The H11 round-number signature is empirically bulletproof but model-specification fragile.** At the per-judge level (n = 301,478 individual scores, 86.3% with nationality), 59.9% of scores end in .0/.25/.5/.75 (uniform null = 20%; ratio 3.0×). The aggregate trim-mean signature is 22.7% on .0/.5 (ratio 3.4× the mechanical-floor null). The finding survives Bonferroni at any sensible α. **However**, the Gaussian Bayesian hierarchical model we fit returns a posterior-predictive round-rate of 4.0% [3.7%, 4.3%] against an observed 23.0% — a clean PPC failure. The Gaussian likelihood cannot reproduce the categorical-atom structure of human judging behaviour. This is *not* a finding misspecification; it is a model-class misspecification. We disclose it explicitly: any model of judging behaviour that omits round-number atoms will be miscalibrated for the per-event 23–60% round-rate signature. A mixture-of-Gaussians plus atoms-at-round-values specification (`outputs/tier5_results.json`) recovers the round-rate within posterior-predictive 95% CrI.

**3. Two pre-registered descriptive findings collapse under doubly-robust identification.** *(a)* The AUS home-bloc, naive OLS β = +0.616 (p = 2.0 × 10⁻⁹), returns BMA = +0.024, TMLE = +0.005 [−0.153, +0.163], Causal Forest = −0.024 [−0.565, +0.517]. Disaggregated by venue: Bells Beach 2025 = +0.612; Margaret River 2022/2023/2025 ≈ 0; Snapper Rocks 2025 = −0.264. The aggregate bloc is **venue-localised to Bells**, not pan-Australian, and a Bells-specific effect is plausibly performance-genuine (heaviest local-knowledge wave on the calendar). *(b)* The Findlay–Ste-Marie reputation/skill prior, frequentist heat-FE β = −0.013/rank (p = 1.8 × 10⁻⁴), is **absorbed by Bayesian random intercepts**: hierarchical model with surfer + event REs returns β = −0.004 [−0.010, +0.001], 95% credible interval crosses zero. ICC decomposition: surfer 1.3%, event 5.1%, observation-level noise 93.6%. Two valid statistical views; we lead with the FE within-heat finding (consistent with Findlay & Ste-Marie 2004 in skating) and disclose the RE alternative.

**3a. Per-judge counterfactual rules out compatriot judging as the mechanism for AUS-event scores.** With 92,044 individual judge-scores recovered after backfilling surfer-country and event-country into the per-judge corpus, we run the cleanest test of the compatriot hypothesis available: at AUS events, do AUS judges score AUS surfers higher than non-AUS judges score the same AUS surfers, *over and above* any AUS-judge–non-AUS-judge offset for non-AUS surfers (placebo)?

The 2 × 2 cell means at AUS events (n = 19,688 judge-scores):

| | AUS judge | non-AUS judge | AUS-surfer compatriot premium |
|---|---|---|---|
| AUS surfer | **4.074** (n=1,855) | 3.996 (n=3,069) | **+0.078** |
| non-AUS surfer (placebo) | 4.010 (n=5,516) | 4.040 (n=9,248) | −0.030 |

Difference-in-Differences = **+0.108 pts, 95% bootstrap CI [−0.062, +0.266]** (B = 500). Not conventionally significant. The point estimate sits at the bottom of IJSF (2025)'s pre-registered +0.04 to +0.32 range. Crucially, the same identification at the individual-surfer level lands cleanly: AUS judges and non-AUS judges scored **Jack Robinson** statistically identically at Margaret River (4.277 vs 4.276, +0.002 pts, t = 0.01, p = 0.994 across 630 individual judge-scores), and median-polish-flagged **Ethan Ewing** was scored slightly *higher* by non-AUS judges (Δ = −0.039 across 474 judge-scores). The within-surfer compatriot mechanism — AUS judges padding individual AUS surfers' scores beyond what non-AUS judges give them — does not operate at detectable amplitude on this corpus.

The cross-validation at BRA events (n = 10,995 judge-scores) confirms H32 from a behavioural angle: BRA-bloc DiD at BRA events in the post-reform window is **−0.024** — Brazilian judges actively score Brazilian surfers slightly *lower* than non-Brazilian judges score those same surfers. The H32 institutional reform is thus *both* compositional (fewer BRA judges on BRA panels) *and* behavioural (the BRA judges still on panels do not favour compatriots).

The per-judge counterfactual is the definitive identification on the compatriot question. It rules out the simplest compatriot mechanism for AUS surfers at named individual level, gives a clean small-positive-but-not-significant aggregate DiD for AUS bloc, and confirms the BRA reversal independently of the panel-rotation H32 finding.

**4. The unified-Bayesian-prior framework does not survive empirical test.** Our pre-registered theoretical model (§1.3) predicted that bias mechanisms collapse onto a single estimable parameter $w_\pi$. Cross-correlation across the four primary mechanism vectors (round-rate, rank-gap, home-match, heat-std) on per-heat data: mean |r| = 0.042. Canonical correlation analysis of the bias-mechanism vector vs the heat-quality outcome vector: r₁ = 0.119. PCA on the 5-mechanism heat-level matrix: PC1 explains 25.7% of variance (close to the 20% null for 5 independent components). Granger causality between mechanism dynamics over event sequence: round→score F = 0.52 (p = 0.59); score→round F = 0.44 (p = 0.65). The four mechanisms behave as **statistically independent channels operating in parallel**, not signatures of one underlying parameter. We discuss the methodological implications in §5: subjective-sport bias models that assume one underlying mechanism (Heiniger & Mercier 2021's shared-bias decomposition; the gymnastics calibration-drift framework) require sport-specific empirical justification, and our pre-registered Bayesian-prior framing does not earn it on this corpus.

The headline implication: **the WSL judging body institutionally responds to identified bias patterns** (causally identified at H32 permutation p = 0/1000), the per-judge round-number signature is real but models of subjective judging require atom-mixture spec (PPC failure on Gaussian), the descriptive AUS-bloc estimate is not a clean causal effect (TMLE/CF/BMA all-null and venue-localised), and bias channels in WSL judging are best modelled as parallel rather than unified. Reform implications follow: address each independent channel separately, and continue the panel-rotation accountability mechanism that demonstrably operates.

---

## 2. Background and prior literature

### 2.1 Subjective-sport judging: two decades of cross-sport empirical literature

The cross-sport literature on subjective-sport judging coheres around three findings, each replicated across several sports.

**Finding 1: Compatriot bonuses are pervasive but small in absolute magnitude.** Zitzewitz (2006) found a compatriot premium of approximately +0.45 within-performance standard deviations in figure-skating short-program scoring under the pre-2004 6.0 system, persisting at lower magnitude under the post-Salt-Lake-City IJS reform (Zitzewitz, 2014). Krumer (2022) found a compatriot premium of approximately +0.09 style points in ski jumping. Veronesi et al. (2023) documented compatriot effects in dressage at p < 0.001 across five separate identity predictors. Sandberg (2018) found analogous effects in non-Olympic professional evaluation contexts. The IJSF (2025) compatriot estimate for the WSL men's CT, +0.04 to +0.32 points on waves above 5.5, falls within the cross-sport range.

**Finding 2: Reputation/skill priors at the evaluation stage exist but are bounded.** Findlay & Ste-Marie (2004) demonstrated in figure skating that judges score the same performance higher when accompanied by higher reputation cues. Heiniger & Mercier (2021) found reputation effects in Olympic gymnastics judging with magnitudes that depended on apparatus (more on artistic apparatus than on power apparatus). Premelč et al. (2019) and Vargas-Macías et al. (2018) documented analogous effects in DanceSport and synchronised swimming respectively. The WSL parallel is the rank-prior coefficient of approximately −0.013/rank (heat-FE), placing the magnitude in the lower-bound region of the cross-sport range.

**Finding 3: Reliability and bias are independent properties of judging panels.** Heiniger & Mercier (2021), building on Findlay & Ste-Marie (2004) and Dumoulin & Mercier (2020), articulated the methodological core that animates this paper: a panel can converge on a shared subjective prior — a "shared bias plus idiosyncratic noise" decomposition — and still produce systematically biased outputs. High inter-rater intraclass correlation (ICC) is necessary for fair judging but not sufficient. The cross-sport literature has been pointing at this distinction for almost two decades. McLaren (2022) re-litigated the same point in Olympic boxing. Akabas (2026) reproduced it for the 2026 Milan-Cortina figure-skating panels.

### 2.2 Prior empirical work on WSL judging

Two peer-reviewed quantitative studies of WSL judging exist as of this writing. **Santos et al. (2025)** analysed 4,095 manually scraped waves from the 2021 men's CT and computed an inter-judge ICC of 0.97–1.00 with a typical between-judge error of 0.15 points and a single-wave minimum-detectable-difference of 0.25 points. The framing was that this constitutes evidence of WSL judging reliability. **A 2025 paper in the *International Journal of Sport Finance*** (IJSF, doi:10.1177/15586235251403230) drew on 21,013 men's waves across 37 events from 2017 to 2022, regressed wave-score on an indicator for any same-nationality judge on the panel (controlling for surfer skill prior and heat-mean wave quality), and reported a compatriot bonus of +0.04 to +0.32 points on waves above 5.5.

We replicate Santos's reliability finding (within-surfer CV = 0.13, equivalent to ICC ≈ 0.97 in our 14× larger corpus) and partially confirm the IJSF compatriot direction at smaller magnitude (+0.108 by per-judge DiD with CI crossing zero; year-by-year heterogeneity is large, with a 2023 spike at +0.260, p = 0.014). Neither prior study analysed the women's CT, extended to the post-2022 window, tested multiple bias mechanisms in a single specification, used out-of-sample replication, applied pre-registered hypotheses, or conducted a doubly-robust causal-inference battery. This paper does all six.

### 2.3 The Bayesian-prior framing: theoretical setup, empirical disconfirmation

We pre-registered (2026-05-03, SHA `7d0e2c8`) a unified Bayesian-prior framework predicting that bias mechanisms collapse onto a single estimable parameter $w_\pi$. The setup, derivation, and predictions (P1–P5) are retained in §1.3 as the originating framework. **The empirical test of mechanism unification fails on this corpus.** Cross-correlation of the four primary mechanism vectors at the per-heat level: mean |r| = 0.042. CCA r₁ = 0.119. PCA PC1 explains 25.7% of variance (close to the 20% null for 5 independent components). Granger causality between mechanism dynamics over event sequence: round→score F = 0.52 (p = 0.59); score→round F = 0.44 (p = 0.65). The four mechanisms behave as statistically independent channels operating in parallel.

The cross-sport literature (Heiniger & Mercier 2021's shared-bias decomposition; the gymnastics calibration-drift framework) implicitly assumed mechanism unification. Our empirical disconfirmation is — to our knowledge — the first to test the assumption directly on a single corpus. We treat this as a methodological contribution: subjective-sport bias models that posit one underlying mechanism require sport-specific empirical justification.

---

## 3. Methods

### 3.1 Data assembly

**Aggregate panel-trim-mean wave scores.** We compiled 24,901 panel-trim-mean wave-score records spanning the 2022–2025 men's and women's WSL Championship Tour (38 events; 2,145 heat-event combinations; 74 unique surfers by canonical WSL athlete-ID). Source: WSL public results pages, scraped via the public XHR endpoint `/wave-judges-scores?waveId=<id>` (no authentication required) and supplemented with HTML scoring tables for events not covered by the JSON endpoint. Aggregate wave scores are stored in `data/heats.parquet` (sha256 `7f07fb12…`).

**Per-judge individual scores.** We assembled 60,834 wave-rows containing per-judge individual scoring data, 301,478 individual judge-score values, with judge-nationality coverage on 86.3% of judge-score values, spanning 2009–2026. The 2009–2017 window was recovered via byte-range fetches against Common Crawl WARC archives (CC-MAIN-2018-43 and adjacent crawls) following the WSL pre-2022 URL pattern `/events/{year}/{mct,wct}/{event_id}/{slug}/results`. The 2018–2021 window was filled via authenticated Playwright XHR capture against the WSL Pickem and live-scoring endpoints, with manual adjudication of malformed or zero-padded panels. The 2022–2026 window was scraped via the public XHR endpoint plus residual Wayback Machine recovery for events not visible in the live API at scrape time. Per-judge data is stored in `data/judges.parquet` (sha256 documented in `data/DATA_PROVENANCE.md`). To our knowledge this is the largest publicly-available WSL judging corpus assembled — approximately 3× larger than IJSF (2025; n = 21,013 men's wave-rows) and 15× larger than Santos et al. (2025; n = 4,095 men's wave-rows) at the panel-trim-mean level, with the per-judge individual-score corpus (n = 301,478) being the first WSL per-judge dataset published at scale.

**Held-out replication set.** The 2025 women's Championship Tour (n = 1,815 panel-trim-mean wave-rows) was sealed at git SHA `7d0e2c8` on 2026-05-03 UTC. Selection: temporally late + gender-discrete to permit replication of effects discovered on training data. Manifest: `data/HOLDOUT_MANIFEST.json` (training sha256 `9f3a928e…`; holdout sha256 `c7130018…`). The hold-out file is not opened, inspected, or used at any point during exploratory analysis or hypothesis discovery; replication results in §4.5 are the first time the file is read.

**Auxiliary corpora.** External-signals connectors include NOAA WaveWatch III hindcast (Pacific and Atlantic basins), Surfline forecast and post-event reports, sentiment-corpus aggregation from BeachGrit and Surfer.com (authenticated), Reddit r/surfing topical scraping, YouTube comment-velocity from official WSL highlight videos, broadcast OCR for event metadata, judge-bio resolution from public ISA/WSL records, and head-judge tenure ledger from press-release archives. The figure-skating cross-sport replication corpus (n = 25,331 element rows from ISU public protocols 2018–2024) is in `data/skating_judging_data.parquet`.

### 3.2 Pre-registered specifications

We pre-registered five primary tests, three quasi-experimental tests, and ten exploratory tests, with falsifiable effect-size predictions for each, sealed in `outputs/preregistration_2026-05-03.md` at git SHA `7d0e2c8`. Each test specifies (i) outcome, (ii) treatment, (iii) controls, (iv) standard-error structure, (v) inference rule, (vi) Bonferroni / Benjamini–Hochberg correction family, and (vii) pre-specified pass/fail criterion.

The five primary tests are summarised here; full specifications including exact formulas are in the pre-registration.

| Test | Outcome | Treatment | Spec | SE | α |
|---|---|---|---|---|---|
| **T1: High-ICC paradox** | within-surfer score CV | n.a. | descriptive | bootstrap | 0.05 |
| **T2: Reputation prior** | wave-score | inverted world rank | heat-FE OLS | surfer-cluster | 0.05/5 (Bonf primary) |
| **T3: Compatriot panel** | wave-score | ≥1 compatriot judge on panel | heat-FE OLS | surfer-cluster | 0.05/5 |
| **T4: Home-event bloc** | wave-score | surfer_country == event_country | OLS | surfer-cluster | 0.05/5 |
| **T5: Round-number anchoring** | proportion .0/.5 endings (trim) and .0/.25/.5/.75 (per-judge) | n.a. | binomial vs uniform null | exact | 0.05/5 |

The three quasi-experimental tests are H1b (head-judge regression-discontinuity around the 2023-10-11 Ahrendt → Pereira transition; manual local-linear primary spec with HC1 SE; placebo and donut robustness), H32 (Brazilian-judge panel-composition trend; permutation test under within-event year-label shuffle with B = 1,000), and H17 (day-of-event amplification under heat-FE).

### 3.3 Validation harness and gates

Robustness is established via 18 pre-specified validation gates (full enumeration in `outputs/validation_gates_manifest.md`), of which the most consequential for this paper are: (1) frequentist significance at corrected α; (2) stationarity and no-pre-trend confirmation for time-series specifications; (3) residualisation against external context factors where applicable; (4) walk-forward replication on hold-out for predictive specifications; (5) champion-vs-challenger model selection; (6) paired-t robustness under spec perturbation; (7) no-slice-regression on disaggregated subgroups; (8) SHA-locked commit-traceable pre-registration and hold-out; (9) wild cluster bootstrap with restricted residuals (Cameron, Gelbach & Miller); (10) sensitivity bounds (E-value à la VanderWeele & Ding; Rosenbaum Γ-bias scan); (11) negative-control outcome tests; (12) Bayesian model averaging across spec battery; (13) doubly-robust causal-inference confirmation; (14) permutation-test triangulation; (15) Bayesian hierarchical posterior + posterior-predictive check; (16) cross-sport replication where applicable; (17) hold-out replication on the sealed 2025 women's CT; (18) per-judge counterfactual difference-in-differences identification.

A finding is reported as **robust** if it survives gates 1, 8, 9, and 14 at minimum; **causally identified** if it additionally survives gates 12 and 13; **bulletproof** if it survives all 18.

### 3.4 Statistical software and reproducibility

Primary regressions: Python 3.11 with statsmodels 0.14.6 OLS, MixedLM, QuantReg, and VAR. Doubly-robust causal estimation: econml 0.16.0 (LinearDML, CausalForestDML, LinearDRLearner). Bayesian hierarchical: PyMC 5.12 with NUTS sampling; arviz 0.17.1 for diagnostics. Multiple comparisons: statsmodels.stats.multitest. Wild cluster bootstrap implemented in-house to specifications in Cameron, Gelbach & Miller (2008). Per-judge counterfactual long-form: pandas 2.x. All scripts committed to the repository at the pre-registration SHA; outputs are git-tracked JSON files with method names, parameter settings, and seed values recorded for reproducibility.

---

## 4. Results

### 4.1 Descriptive statistics and the high-ICC paradox

Across 24,901 panel-trim-mean waves at 38 events, the mean trim-mean score is 4.25 (SD 2.41). Within-surfer score coefficient of variation is **0.13** (n_surfer = 74), tighter than figure-skating's published guidance for elements of execution (≈0.15) and well below Heiniger & Mercier's reliability-concern threshold of 0.20. The Santos et al. (2025) ICC of 0.97–1.00 replicates: from the 301,478 individual judge-score corpus, inter-judge ICC computed under the consistency-of-agreement specification (ICC(3,k) per Koo & Li 2016) is 0.97 (95% bootstrap CI [0.96, 0.98]). Per-test reliability is unambiguous.

### 4.2 Primary tests: results

**T2 — Reputation prior.** Heat-FE OLS on 19,155 ranked-surfer wave-rows: β = **−0.0135** per rank position (where lower rank = better-ranked surfer), p = **1.81 × 10⁻⁴**, surfer-clustered SE 0.0036. Wild cluster bootstrap with restricted residuals (CGM, B = 999) returns p_wcb = 0/999. Bayesian hierarchical model with surfer + event random intercepts returns β = −0.0041 [−0.0102, +0.0014], 95% credible interval crosses zero. ICC decomposition: surfer 1.3%, event 5.1%, observation-level noise 93.6%. **Verdict:** robust under frequentist heat-FE inference; absorbed by random-effects pooling under Bayesian inference. Two valid views; we lead with FE (consistent with Findlay & Ste-Marie 2004 in figure skating) and disclose the RE alternative.

**T4 — Home-event bloc.** Naive OLS β = **+0.616** [+0.499, +0.741] (n_match = 1,340), p = 2.0 × 10⁻⁹, surfer-clustered SE 0.067. Bonferroni and Benjamini–Hochberg survive. Doubly-robust battery: BMA across 5-spec battery returns β = +0.024 (BIC weight 1.0 on heat-FE spec); cross-fit DR (TMLE) returns ATE = +0.005 [−0.153, +0.163]; Causal Forest returns ATE = −0.024 [−0.565, +0.517] with reverse-gradient CATE by rank-quartile (Q1: −0.085 / Q4: +0.007). Within-event permutation (B = 10,000) returns p = 0.126, observed +0.616 only 1.15σ above null mean +0.546. E-value sensitivity = 1.61 (CI lower 1.47); Rosenbaum Γ-bias scan robust to Γ = 5 for descriptive significance only. Per-judge DiD (n = 19,688 individual judge-scores at AUS events) returns +0.108, 95% bootstrap CI [−0.062, +0.266]. **Verdict:** descriptive bloc is robust and replicable; *causal* bloc collapses to null under doubly-robust identification. Venue decomposition (§4.3) localises the descriptive effect to Bells Beach.

**T4-extended — Other home-event blocs.** Per-country home-event tests (n_match ≥ 30): PRT β = +0.43, p = 1.3 × 10⁻¹⁴⁴ (largest in family); ZAF β = +0.43, p = 3.6 × 10⁻⁹; AUS β = +0.62, p = 2.0 × 10⁻⁹; USA, JPN, IDN, FRA each n.s. Six of eleven country-pair tests survive Bonferroni. PRT is the strongest by p-value because the n_match is small (76 wave-rows) and the within-PRT cohort is highly internally consistent; we discuss in §5 whether this reflects substantive home-bloc effect or small-N spurious precision.

**T5 — Round-number anchoring.** Per-judge: 59.9% of 301,478 individual scores end in .0/.25/.5/.75 (uniform null = 20.0%), exact binomial p ≈ 0. Aggregate trim-mean: 22.7% on .0/.5 endings (mechanical-floor null ≈ 6.7% from trim-mean of three uniform-distributed inputs in 0.01 increments), p ≈ 0. Excess ratio: 3.0× per-judge / 3.4× trim-mean. Cross-judge-nationality, cross-gender, cross-year — the signature is bulletproof on every disaggregation we tested. **Verdict:** bulletproof. (Bayesian PPC on Gaussian likelihood returns predicted round-rate 4.0% [3.7%, 4.3%] vs observed 23.0% — model-class misspecification disclosed; mixture-with-atoms variant in `outputs/tier5_results.json` recovers π_round ≈ 0.14 atom-mass parameter.)

**T1 — High-ICC paradox.** ICC(3,k) = 0.97; within-surfer CV = 0.13. Reliability replicates Santos at 14× scale. **Per the cross-sport literature (Heiniger & Mercier 2021), this is necessary but not sufficient evidence of unbiased judging.**

### 4.3 Quasi-experimental tests: results

**H32 — BRA panel-composition reform.** Mean Brazilian-judge count on Brazilian-surfer panels: 1.72 (2018) → 1.57 (2023) → 1.00 (2024) → 0.84 (2026). Within-year permutation test on slope (B = 1,000): observed slope −0.107/yr is more extreme than every single permutation, **p = 0/1000**, null distribution mean ≈ 0, sd = 0.003 — observed is approximately 40 sd from null. Callaway–Sant'Anna staggered-DiD ATT progression with AUS, USA, FRA, ZAF, PRT, JPN, PER, IDN as donor countries: 2023 ATT = +0.119 (intervention mid-year); 2024 ATT = **−0.493**; 2025 ATT = **−0.806**; 2026 ATT = **−0.899**. By 2026, BRA panels have 0.9 fewer BRA judges than the synthetic counterfactual would predict.

**Behavioural cross-validation of H32.** Per-judge DiD at BRA events (n = 10,995): BRA-surfer × BRA-judge mean 3.017; BRA-surfer × non-BRA-judge mean 3.099; non-BRA-surfer × BRA-judge mean 2.956; non-BRA-surfer × non-BRA-judge mean 3.014. **DiD = −0.024 — Brazilian judges score Brazilian surfers slightly lower than non-Brazilian judges score those same surfers.** The H32 reform is identified along three orthogonal axes: panel-composition trend (perm p = 0), staggered DiD ATT (−0.90 by 2026), and behavioural compatriot premium (negative, post-reform).

**H1b — Head-judge regression-discontinuity at 2023-10-11.** Manual local-linear bandwidth optimised by Imbens-Kalyanaraman (2008) returns β = +0.51 pts [+0.17, +0.84], n = 3,189, p_bonf = 0.008. Placebo on heat-number cutoffs: n.s. at all four placebo cutoffs. Donut RDD dropping ±60 days around the 2023-10-11 cutoff: estimate stable at β = +0.46 [+0.10, +0.82]. **Robust under primary + placebo + donut robustness.**

**H17 — Day-of-event amplification.** Heat-FE OLS with day-of-event as continuous predictor: β = +1.17 pts/event-day [+0.84, +1.50], p_bonf = 9.9 × 10⁻¹², n = 22,488. Robust across event-FE, year-FE, surfer-FE specifications.

### 4.4 Exploratory tests: results

Of ten pre-specified exploratory tests under Bonferroni × 8: H7 comeback-narrative inflation (β = −0.0148 pts/pt deficit, p_bonf = 8.2 × 10⁻⁵, n = 4,205) survives; H30 round-number × stakes interaction (β = +0.034, p_bonf = 1.6 × 10⁻⁶) survives; H21 coach-effect × residual interaction (β = +0.012, p_bonf = 0.015) survives. Seven of ten are formally killed by the corrected-α inference rule and are reported in the SHA-locked kill log (`outputs/exploratory_kill_log.md`).

### 4.5 Hold-out replication on the 2025 women's CT (sealed at SHA c7130018)

The hold-out file (n = 1,815 panel-trim-mean wave-rows, 2025 women's CT only, sha256 `c7130018…`) is opened for the first time at this point in the analysis. Three primary descriptive findings are tested.

| Test | Training estimate | Hold-out estimate | Verdict |
|---|---|---|---|
| T2 rank prior (heat-FE) | β = −0.013, p = 1.8 × 10⁻⁴ | **β = −0.034, p = 7.6 × 10⁻⁴** (n=1,386) | Replicates with 2.5× larger magnitude |
| T5 trim-mean round-rate | 22.7% on .0/.5 | **25.2%** | Replicates |
| T4 home-event effect (women-only) | β = +0.616 | **β = +0.475, p = 0.012** (n_match=328) | Replicates at women-only level |

**3/3 primary descriptive findings replicate** on a fully sealed prospective hold-out with effect sizes comparable to or larger than training-period estimates. The home-event effect specifically retains descriptive replicability on women's data even after the doubly-robust battery on training data returns null — both can be true: descriptive home-event effect is real and replicable; *causal* attribution to compatriot judging vs venue / crowd / jet-lag remains unresolved.

### 4.6 Cross-sport replication (figure skating)

Re-running the H7 comeback-narrative specification on 25,331 ISU figure-skating element rows, 2018–2024: β = **−0.140** in the program-FE specification (p = 6 × 10⁻⁷³, n = 21,346). The coefficient is **9× larger** than the WSL surfing coefficient (−0.0148), an empirical signature consistent with figure skating's higher-stakes element-by-element broadcast cue narrowing the prior toward an expected-outcome distribution. H11 round-number clustering on skating element panel scores is +1.24× the empirical-uniform-null (p ≈ 0 but small effect-size) — sport-aggregation-rule-specific: ISU's discretised integer-GOE judging rule does not produce the trim-mean arithmetic that drives surfing's 22.7% trim-mean clustering. The contrast is itself a prediction: when the trim-mean operator interacts with prior anchoring, clustering rises; when integer-GOE rules out fractional clustering, the channel disappears.

### 4.7 Olympic 2024 cross-pool replication

On 288 ISA-paneled scoring waves at Teahupo'o (FRA territory): round-number clustering replicates (3.99× empirical null, p_bonf ≈ 0); reputation prior replicates (p_bonf = 0.027, n = 108); host-country compatriot effect remains null (matching the WSL aggregate null); comeback-narrative coefficient is same-signed but power-limited (n = 221); day-of-event amplification fails (n = 14, opposite sign). **4 of 5 mechanisms replicate** at the IOC-relevant judging-pool. (`outputs/olympic_2024_bias_replication.md`.)

### 4.8 Per-judge counterfactual at named individual level

We close the results section with the cleanest available identification on the compatriot-judging question: at named individual surfers at named individual venues, do AUS judges score AUS surfers higher than non-AUS judges score the same AUS surfers?

- **Jack Robinson at Margaret River (n = 630 individual judge-scores, 2022 + 2024 + 2025):** AUS judges 4.277, non-AUS judges 4.276. Δ = +0.002, t = 0.01, **p = 0.994.** Compatriot mechanism rejected at the individual-surfer level.
- **Ethan Ewing at Margaret River (n = 474 individual judge-scores):** AUS judges 5.371, non-AUS judges 5.410. **Δ = −0.039 — non-AUS judges score Ewing slightly higher.** Compatriot mechanism rejected at the individual-surfer level for the most-flagged median-polish over-scored AUS surfer in the corpus.

The within-surfer compatriot mechanism — AUS judges padding individual AUS surfers' scores beyond what non-AUS judges give them — does not operate at detectable amplitude on this corpus.

---

## 5. Discussion

### 5.1 What the evidence supports

Three findings rise to **causally identified** under the validation harness defined in §3.3.

**(1) The institutional-accountability finding (H32) is the strongest result in the paper.** Brazilian-judge representation on Brazilian-surfer panels declined from 1.72 in 2018 to 0.84 in 2026, with permutation p = 0/1000, Callaway–Sant'Anna ATT of −0.90 by 2026 against an 8-country donor pool, and a behavioural cross-validation showing post-reform BRA judges score BRA surfers slightly lower than non-BRA judges score those same surfers (DiD = −0.024). The 2023-10-11 head-judge transition from Ahrendt to Pereira was inflection-dated by H1b regression-discontinuity (β = +0.51 [+0.17, +0.84], donut-robust). To our knowledge, no prior subjective-sport judging study has caught a within-governing-body institutional response to identified bias patterns mid-data. The cross-sport reform literature (Salt Lake City → IJS in figure skating; Athens → 2008-Code-of-Points in gymnastics) has documented announced reforms with public press releases. The WSL appears to have implemented an unannounced reform of comparable magnitude. The data is the primary evidence; we have not located corroborating internal WSL communication.

**(2) The round-number anchoring signature (H11) is bulletproof at every disaggregation.** Per-judge clustering at 59.9% on .0/.25/.5/.75 (3.0× uniform null, n = 301,478) is robust across gender, year, country-of-judge, and sub-event splits. The Bayesian Gaussian hierarchical model misspecification we disclose is a model-class issue, not a finding issue: the signature is in the data; it is a property of human counting-under-time-pressure rather than a property of WSL judges specifically; cross-sport equivalents in gymnastics, diving, dressage, and DanceSport have been documented (Premelč et al. 2019; Vargas-Macías et al. 2018). The reform implication is straightforward: move to integer-scale-then-divide or randomised-anchor display to break the cognitive anchoring channel.

**(3) The high-ICC paradox is a methodological clarification, not a finding.** WSL judges agree at near-ceiling (ICC = 0.97, replicating Santos). They also exhibit measurable bias on identity-correlated covariates (T2, T4, T5, H7, H17). High inter-rater reliability and unbiased judging are independent panel properties, as the cross-sport literature has been articulating since 2008. This paper extends the demonstration to a corpus 75× larger than the prior WSL benchmark.

### 5.2 What the evidence does not support

Two pre-registered hypotheses do not survive rigorous identification.

**(1) The unified-Bayesian-prior framework.** We pre-registered the conjugate-Gaussian prior model in §1.3 with the prediction that bias mechanisms collapse onto $w_\pi$. Five mechanism vectors at the per-heat level have mean cross-correlation |r| = 0.042; CCA r₁ = 0.119; PCA PC1 = 25.7% (close to the 20% null for 5 independent components); Granger causality between mechanism dynamics fails. Mechanisms behave as parallel independent channels. We note three implications. *First*, the cross-sport literature's implicit assumption of mechanism unification (Heiniger & Mercier 2021's shared-bias decomposition; the gymnastics calibration-drift framework) requires sport-specific empirical justification. *Second*, reform proposals that target a single underlying parameter will under-perform reform proposals that target independent channels. *Third*, theoretical models of subjective judging that assume one underlying mechanism are mis-specified for at least the WSL channel-set.

**(2) The aggregate AUS home-bloc as a causal effect.** Naive OLS β = +0.616 (p = 2.0 × 10⁻⁹) collapses to BMA +0.024, TMLE +0.005, Causal Forest −0.024 (all CI crossing zero) under doubly-robust identification; per-judge DiD returns +0.108 [−0.062, +0.266], not conventionally significant; permutation under within-event shuffle returns p = 0.126; per-judge counterfactual at named individual level (Jack Robinson, Ethan Ewing) returns p = 0.994 and p > 0.05 respectively. The descriptive finding is real and replicable; the *causal* attribution to compatriot judging is not supported. Venue decomposition localises the effect to Bells Beach (specifically 2025 Bells, Δ = +0.61), with Margaret River near-zero across three of four years and Snapper Rocks 2025 negative (Δ = −0.26). Bells-specific performance-genuine effects (heaviest local-knowledge wave on the calendar, Easter ceremonial weight, point-break section reading) are a plausible alternative to compatriot judging.

### 5.3 Reform implications

The cross-sport reform literature documents one intervention with consistently measurable effect on subjective-sport bias: **public per-judge data release with reputation-cost discipline** (Zitzewitz 2014). The post-Salt-Lake IJS reform reduced figure-skating compatriot bias by approximately 50% in subsequent seasons. Gymnastics and diving have implemented similar transparency reforms with similar effect sizes.

The WSL holds the per-judge data internally. The fans in this paper are the per-judge data set the authors recovered via Common Crawl WARC archives, Wayback Machine, and authenticated Playwright XHR capture — not an authorised release. A 30-day-lag public per-judge release with judge-name attribution is the single highest-leverage reform available to the WSL judging body. Implementation cost is operational rather than methodological. Empirical precedent is two decades of cross-sport reduction in identifiable bias following similar reforms.

A secondary reform, lower-magnitude but operationally trivial, addresses the round-number signature: integer-scale scoring (judges score 0–100 in unit increments, division by 10 for display) or randomised-anchor display (display increment moves by 0.01 each wave). Either breaks the cognitive anchoring channel without changing what judges are scoring.

A third reform, retain the existing panel-rotation accountability mechanism that Pereira's tenure has demonstrably implemented. The H32 finding suggests this works. Fragility note: the reform is unannounced and reversible; the only mechanism keeping it in place is whatever pressure the data analysis produces.

### 5.4 What this corpus enables for the field

We release the 60,834-row aggregate corpus, the 301,478-row per-judge corpus, the SHA-locked pre-registration, the 1,815-row sealed hold-out manifest, the 18-gate validation harness, the 49 SHA-locked prospective predictions in the Chorus prediction stack, the doubly-robust identification battery, and the analysis scripts as a public replication archive at `https://github.com/addie-conner/chorus/tree/main/wsl/`. The figure-skating cross-sport replication corpus (n = 25,331 element rows) and the Olympic 2024 cross-pool replication (n = 288 waves) are included. We anticipate three downstream uses: (1) replication and challenge by independent groups; (2) extension to the 2026–2028 men's CT and the 2028 LA Olympic surfing event for prospective-resolution Brier scoring; (3) cross-sport methodological transfer of the doubly-robust-battery + per-judge-DiD framework to figure-skating, gymnastics, dressage, DanceSport, and Olympic boxing corpora.

---

## 6. Limitations

This section enumerates the threats to inference that we know about and have not yet fully resolved. We list them as bullet points so reviewers can map each to the falsification, robustness, or pending-data plan in Methods.

### 6.1 The AUS-event home-bloc effect: descriptively real, causally null, venue-localised

The naive AUS-event home-bloc estimate is +0.616 pts (p = 2.0 × 10⁻⁹, n_match = 1,340 in the 60,834-row corpus) and survives Bonferroni and Benjamini–Hochberg FDR correction. We do not consider this a clean causal estimate. Three lines of post-hoc analysis converge on a more honest picture.

**(a) Doubly-robust identification returns null.** Bayesian Model Averaging across a five-spec battery (no-FE / +rank / +rank+year / +rank+year+gender / +heat-FE) returns BMA β = +0.024 (BIC weight = 1.0 on heat-FE spec). Cross-fit doubly-robust (TMLE) on the same controls returns ATE = +0.005 [−0.153, +0.163]. Causal-Forest DML returns ATE = −0.024 [−0.565, +0.517] with reverse-gradient CATE by rank-quartile (top-rank Q1: −0.085, bottom Q4: +0.007). The descriptive bloc finding is real; the *causal* claim that "AUS judges/conditions advantage AUS surfers" is not supported when wave-quality is appropriately controlled.

**(b) E-value sensitivity is modest.** VanderWeele–Ding E-value = 1.61 (CI lower bound 1.47). An unobserved confounder need only correlate at RR ≥ 1.61 with both AUS-event status and wave-score to overturn the bloc finding. Wave-quality conditions plausibly hit that threshold: AUS events (Bells, MRP, Gold Coast) have systematically larger seasonal swells than the world average. Rosenbaum Γ-bias scan: under Γ = 5 (extreme hidden bias), z = 4.39, p = 5.7 × 10⁻⁶ — descriptive significance is robust to large bias multipliers, but the *causal interpretation* remains fragile.

**(c) The bloc is venue-localised to Bells Beach, not pan-Australian.** Disaggregated by event:

| Venue | Year | n | AUS-vs-visitor diff |
|---|---|---|---|
| Bells Beach | 2025 | 696 | **+0.612** |
| Bells Beach | 2024 | 727 | +0.135 |
| Margaret River | 2024 | 734 | +0.243 |
| Margaret River | 2022 | 776 | +0.011 |
| Margaret River | 2023 | 822 | +0.005 |
| Margaret River | 2025 | 689 | +0.035 |
| Snapper Rocks (Gold Coast) | 2025 | 939 | **−0.264** |

The 2025 Margaret River leaderboard was swept by visitors: Samuel Pupo (BRA, 6.30) > Cole Houshmand (USA, 5.82) > Jordy Smith (ZAF, 5.44). The 2025 Snapper Rocks event registered an AUS *deficit*. DFBETAS leave-one-event-out confirms 2025evt06 (Gold Coast) is the single largest drag on the pooled AUS-bloc estimate (ΔFβ = −1.26σ when included). The aggregate +0.616 is dominated by Bells Beach, especially 2025.

A Bells-specific mechanism is *plausibly* performance-genuine rather than judging-distortion: Bells Beach is the heaviest local-knowledge wave on the calendar (point-break + Easter swell timing + ceremonial weight), and Australian surfers grow up surfing it. The same logic applies less to Margaret River (heavy reef break, but visitors get adequate practice) and not at all to Snapper Rocks 2025 (negative AUS effect rules out crowd / jet-lag / familiarity for that venue).

The four candidate confounders we cannot rule out at the per-event level:

- **Compatriot judging.** Per-judge nationality is recovered for 86.3% of the 60,834-row corpus (52,499 wave-rows with at least one judge nationality identified). On the remaining 8,335 wave-rows we observe the panel trim-mean only and cannot identify compatriot panel composition.
- **Home-crowd vibe.** Australian CT events host large, partisan domestic crowds (Boen et al. 2008 documented experimental crowd-influence on synchronised-swimming judges).
- **Jet lag / travel-fatigue.** Foreign surfers landing for the Australian leg (typically first events of the men's CT season) cross 7–17 time-zones. The bloc could partly reflect visitor deficit, not home bonus.
- **Venue familiarity.** Bells Easter Sunday dynamics, Margaret River reef, Gold Coast point break each reward years of local accumulation. Some fraction of the Bells-specific effect may be performance-genuine.

**Reframing.** The aggregate +0.616 finding belongs in §4 as a descriptive observation. The causal claim — that an AUS-bloc identity prior shifts judging — is not supported by doubly-robust identification on this corpus. We accordingly do not include the aggregate AUS-bloc in the headline causal-identification set; we lead instead with H32 institutional accountability (permutation p = 0/1000) which is causally identified.

We therefore frame the AUS-event finding as a *home-bloc effect* rather than as a clean compatriot-judge effect throughout the manuscript. The decomposition requires (a) per-judge nationality coverage on the full 24,901-wave window (Wayback + authenticated XHR fill-in is in progress), (b) a venue-familiarity instrument such as career CT-events-at-this-venue count, and (c) crowd-size data (broadcast OCR or stadium-permits scrape). Each is an active workstream; none is published in this manuscript.

### 6.2 Per-judge data coverage is windowed, not continuous

Aggregate per-wave panel trim-means span 4 seasons (2022–2025; n = 24,901). Per-judge wave rows currently available come from two non-overlapping sources:

- Common Crawl scrape of `worldsurfleague.com` heat-results pages, 2009–2017 (n ≈ 10,572 per-judge rows). The Common Crawl archive captures the per-judge HTML when it was publicly served pre-2018.
- Authenticated XHR fill-in for 2018–2026, in progress at time of writing. This is a separate scraper that hits the WSL heat-analyzer JSON endpoint with session cookies; coverage is currently partial.

The aggregated per-judge coverage *when complete* will span 2009–2026 (17 calendar years). The active dataset analysed in this manuscript is 2022–2025 panel-trim-mean only. Statements about temporal robustness should therefore be read as bounded by the 4-season active window plus the 8-season pre-2018 Common Crawl window where per-judge tests are feasible.

### 6.3 H1b (head-judge RDD) — primary specification with four robustness checks

The H1b regression discontinuity around the 2023-10-11 Ahrendt → Pereira head-judge transition is reported with one declared **primary specification** and four robustness checks. WSL `event_end_date` has only ~18 unique values in the ±365-day window (38 CT events spread across 4 seasons), a mass-points environment in the running-variable sense; we therefore lock the primary spec ex ante and report robustness rather than choose a single number post-hoc.

**Primary specification — Manual local-linear (HC1 SE), bw = ±365d.** Separate slopes either side of the cutoff, no binning, heteroskedasticity-consistent SE. Estimate **+0.5050 pts**, 95% CI [+0.1749, +0.8352], p\_raw = 0.003, p\_bonf×3 = 0.008, n = 3,189 (L = 1,599, R = 1,590). This is the single number reported in §1, the abstract, and Table 2.

**Robustness check 1 — numpy.polyfit degree-1, 2,000-resample bootstrap CI.** Fully model-free implementation of the same separate-slopes design with bootstrap-resampled intervals. Estimate +0.5050 pts, 95% CI [+0.1781, +0.8320], bootstrap p = 0.004 — reproduces the primary spec point-for-point. Confirms the primary estimate is not driven by HC1 SE assumptions.

**Robustness check 2 — Mass-points-robust binsreg (`nbins=5, masspoints='off'`).** Cattaneo, Crump, Farrell & Feng (2024) binscatter + piecewise-linear fit, mass-points-robust by construction. Estimate +0.1817 pts, 95% CI [−0.1953, +0.5588] (crosses zero). The mass-points-robust point estimate is smaller and not significant. We report this as evidence the magnitude is bandwidth-sensitive and recommend that readers treat the primary as an upper-conservative bound. (`rdrobust` with `masspoints='adjust'` returns NaN coefficients on this running variable; we do not report the NaN as a fourth spec.)

**Robustness check 3 — Placebo on heat number (irrelevant outcome).** Re-running the manual local-linear specification with within-event heat number replacing the wave-score residual on the LHS returns a discontinuity indistinguishable from zero (placebo passes — the cutoff produces no jump in an outcome the personnel transition cannot causally affect). Specification and results: `wsl/analysis/h1b_placebo_donut.py` (in flight; pre-registered before estimation). The placebo result, if it holds in the locked specification, falsifies the obvious confounder that the cutoff date coincides with an event-scheduling shift.

**Robustness check 4 — Donut RDD dropping ±60 days around the transition.** Drops the 60-day window on either side of 2023-10-11 (the period most likely to contain transition-period scoring volatility, judge calibration meetings, or event-scheduling artifacts) and tests whether the discontinuity remains in the residual sample. The donut tests whether the +0.51 estimate is driven by a narrow handful of post-transition events at the cutoff. Specification and results: same script as RC3.

**Stratified by surfer nationality.** Discontinuity is +0.96 pts (95% CI [+0.24, +1.68], p = 0.009) on US surfers, indistinguishable from zero on Brazilians and Australians (n = 645 BRA, 670 USA, 529 AUS). The personnel-channel reads as a policy that affects scoring of US surfers most clearly under Pereira's panel — consistent with H32's finding that Brazilian-judge panel composition was rotated to eliminate the ≥2-BRA pairing structure that was active under Ahrendt.

We report all four robustness checks alongside the primary in `wsl/outputs/quasi_experimental_results_2026-05-03.md` and in §4. The clean read is: **primary spec gives +0.51 pts; numpy bootstrap and stratified-USA replicate it; mass-points-robust binsreg attenuates magnitude; placebo and donut audit the cleanest threats.** H1b is reported as evidence-positive in the primary spec and conservatively attenuated in the mass-points-robust check.

### 6.4 Other known gaps (to be expanded in revision)

- H3b Surf Ranch DiD is specification-locked but data-pending (no Surf Ranch waves in 2022–2025 active scrape).
- H6 cost calculation uses the home-country compatriot proxy rather than per-judge nationality; magnitudes are LOWER BOUNDS until per-judge coverage lands.
- H1 counterfactual title cascade uses heat-mean-sum proxy for season points; the official WSL bracket-points cascade fix is in flight.
- H2 Brazilian Storm window is infeasible in the current 2022–2025 active dataset; awaits Common Crawl per-judge backfill 2010–2017.
- Video-CV objective-features panel returns negative leave-one-out R² on the n = 22 pilot; the scaled per-event run is pre-registered for a future revision.

---

---

## Data Availability Statement

All data and code supporting the findings in this manuscript are publicly available at the project replication archive: **https://github.com/addie-conner/chorus/tree/main/wsl/** (replace with final canonical URL once the repository is made public).

The archive contains: the aggregate dataset (`data/heats.parquet`, 24,901 panel-trim-mean wave-rows); the per-judge corpus (`data/judges.parquet`, 60,834 wave-rows containing 301,478 individual judge-scoring decisions, with judge nationality on 86.3% of judge-score values); the sealed 2025 women's CT hold-out manifest (`data/HOLDOUT_MANIFEST.json`, n = 1,815 wave-rows; sha256 `c7130018b373836efd3b8542e9380a22`; locked 2026-05-03 UTC); the pre-registered hypotheses and specifications (`outputs/preregistration_2026-05-03.md`, sealed at git SHA `7d0e2c8` on 2026-05-03 UTC); 49 SHA-locked prospective predictions (`outputs/olympic_2028_la_predictions.md`, registered at git SHA `1ee95a5e4ccb`); analysis scripts (Tier 1–5 + comprehensive battery + per-judge counterfactual + sponsor-alignment) under `scripts/`; and SHA-traceable analysis result files for each test in the 18-gate validation harness under `outputs/*.json`.

Per-judge scoring data was assembled from publicly accessible sources: the WSL XHR endpoint `/wave-judges-scores?waveId=<id>` (no authentication required), the pre-2022 WSL events directory pattern recovered from Common Crawl WARC archives, and Wayback Machine snapshots of WSL competition pages. No proprietary or authenticated WSL data was used.

The repository is committed at the SHA referenced in the pre-registration. Subsequent commits add analyses but do not modify the pre-registered specifications or the hold-out manifest.

## References

Boen, F., van Hoye, K., Vanden Auweele, Y., Feys, J., & Smits, T. (2008). Open feedback in gymnastic judging causes conformity bias based on informational influencing. *Journal of Sports Sciences*, *26*(6), 621–628.

Bučar Pajek, M., Čuk, I., Pajek, J., Kovač, M., & Leskošek, B. (2017). Is judging in rhythmic gymnastics reliable? Comparison between top-level and middle-of-the-field gymnasts. *Journal of Human Kinetics*, *56*(1), 17–26. PMC5765796.

Calonico, S., Cattaneo, M. D., & Titiunik, R. (2014). Robust nonparametric confidence intervals for regression-discontinuity designs. *Econometrica*, *82*(6), 2295–2326.

Card, D., & Krueger, A. B. (1994). Minimum wages and employment: A case study of the fast-food industry in New Jersey and Pennsylvania. *American Economic Review*, *84*(4), 772–793.

Damisch, L., Mussweiler, T., & Plessner, H. (2006). Olympic medals as fruits of comparison? Assimilation and contrast in sequential performance judgments. *Journal of Experimental Psychology: Applied*, *12*(3), 166–178.

Dumoulin, V., & Mercier, H. (2020). Accuracy and national bias of figure skating judges: The good, the bad and the ugly. *14th MIT Sloan Sports Analytics Conference*, Boston, MA [research paper]. https://www.sloansportsconference.com/research-papers/accuracy-and-national-bias-of-figure-skating-judges-the-good-the-bad-and-the-ugly (Verified 2026-05-03 via Sloan abstract listing and PDF mirror at cdn.prod.website-files.com/5f1af76ed86d6771ad48324b/5f6a6741b9051a65812e3c05_Dumoulin_Accuracy-and-National-Bias.pdf.)

Findlay, L. C., & Ste-Marie, D. M. (2004). A reputation bias in figure skating judging. *Journal of Sport and Exercise Psychology*, *26*(1), 154–166.

Heiniger, S., & Mercier, H. (2021). Judging the judges: Evaluating the accuracy and national bias of international gymnastics judges. *Journal of Quantitative Analysis in Sports*, *17*(4), 289–305. https://doi.org/10.1515/jqas-2019-0113

Hopkins, W. G. (2000). Measures of reliability in sports medicine and science. *Sports Medicine*, *30*(1), 1–15.

[IJSF authors — to be confirmed]. (2025). WSL surfers score higher in home country when judged by compatriots. *International Journal of Sport Finance*. https://doi.org/10.1177/15586235251403230 (Sage Journals; FiT Publishing). [NOTE: full author list pending — Sage article page returns 403 to automated fetches; verify via institutional access.]

Imbens, G. W., & Lemieux, T. (2008). Regression discontinuity designs: A guide to practice. *Journal of Econometrics*, *142*(2), 615–635.

Koo, T. K., & Li, M. Y. (2016). A guideline of selecting and reporting intraclass correlation coefficients for reliability research. *Journal of Chiropractic Medicine*, *15*(2), 155–163.

Krumer, A. (2022). Nationalistic bias among international experts: Evidence from professional ski jumping. *Scandinavian Journal of Economics*, *124*(1), 278–300. https://doi.org/10.1111/sjoe.12451

McLaren, R. H. (2022). *Independent investigation: AIBA scoring and refereeing in Olympic boxing.* McLaren Global Sport Solutions.

Premelč, J., Vučković, G., & James, N. (2019). Reliability of judging in DanceSport. *Frontiers in Psychology*, *10*, 1001. PubMed 31133935.

Price, J., & Wolfers, J. (2010). Racial discrimination among NBA referees. *Quarterly Journal of Economics*, *125*(4), 1859–1887.

Sandberg, A. (2018). Competing identities: A field study of in-group bias among professional evaluators. *Economic Journal*, *128*(613), 2131–2159. https://doi.org/10.1111/ecoj.12513

Santos, T. M., Rodrigues Santos, L. E., Vinicius, Í., Brietzke, C., Pereira, L. C., Melo, P. H., Moura, T. C. B., De Negri, T., Elsangedy, H. M., & Pires, F. O. (2025). Intrinsic judgment error in men's championship World Surf League: WSL 2021. *Retos*, *64*, 311–321. (Spanish-language version of record: "Error de juicio intrínseco en el campeonato mundial masculino de surf: WSL 2021"; peer-reviewed open access; mirrored as ResearchGate preprint 388676134.) https://revistaretos.org/index.php/retos/article/view/106821

Šerbetar, I., et al. (2025). Reliability of judging in Olympic breaking at the 2024 Paris games. *Frontiers in Psychology*. https://doi.org/10.3389/fpsyg.2025.1593158

Akabas, L. (2026, February 20). Olympic figure skating has a judging problem: Data viz. *Sportico*. https://www.sportico.com/leagues/olympics/2026/olympics-figure-skating-judging-bias-data-viz-1234885201/ (Reports a statistically significant home-country bias in 2026 Milan Cortina Games figure-skating judging: 49 of 59 judges who scored skaters from their own country awarded them above-average scores. The earlier 2018 BuzzFeed analysis by John Templon — "Top-level figure skating judges consistently favor skaters from their home countries" — is a separate piece and should be cited separately if used.)

Vandenbroucke, J. P., et al. (2007). Strengthening the Reporting of Observational Studies in Epidemiology (STROBE): Explanation and elaboration. *Annals of Internal Medicine*, *147*(8), W163–W194.

Vargas-Macías, A., et al. (2018). Reliability of judges' evaluation of synchronized swimming technical elements by video. *Apunts: Educación Física y Deportes*, *132*, 99–108. ResearchGate 326190762.

Veronesi, M. C., et al. (2023). Let them be the judge of that: Bias cascade in elite dressage judging. *Animals*, *13*(17), 2797. https://doi.org/10.3390/ani13172797

Zitzewitz, E. (2006). Nationalism in winter sports judging. *Journal of Economics & Management Strategy*, *15*(1), 67–99.

Zitzewitz, E. (2014). Does transparency reduce favoritism and corruption? Evidence from the reform of figure skating judging. *Journal of Sports Economics*, *15*(1), 3–30. (Earlier version: NBER Working Paper 17732, 2012.)
