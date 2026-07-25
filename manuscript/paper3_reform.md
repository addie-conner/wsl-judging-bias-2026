# Reforming Olympic Surfing Judging Before LA 2028: Four Empirically-Grounded Reforms and a SHA-Locked Prospective Forecast

_Policy companion to Conner et al. (2026) Papers 1 and 2 — "Manufacturing Consensus" (empirical) and "Eighteen Gates and the Causality Ladder" (methodology)._

---

## Authors and affiliations

Addie Conner (independent; Chorus Research)

_Corresponding author:_ Addie Conner, addieconner@gmail.com
_ORCID:_ https://orcid.org/0009-0007-7853-4140

_Pre-registered prospective forecast:_ `outputs/olympic_2028_la_predictions.md` (locked 2026-05-04 UTC; git SHA `1ee95a5e4ccb`; heats SHA `7f07fb121abe`).
_Code, data, replication archive:_ https://github.com/addie-conner/wsl-judging-bias-2026

---

## Abstract

The 2028 Olympic surfing event at Lower Trestles, San Clemente, will be the first major-stakes international surf competition since Paris 2024 and the first held on host-country water for the United States. We propose a four-part reform agenda — public per-judge data with reputation-cost discipline; scoring-scale architecture that prevents round-number anchoring at the input layer; panel-rotation rules that prevent compatriot stacking; and pre-registered Brier-scored prospective predictions as a continuous accountability mechanism — derived from cross-sport reform precedent in figure skating (post-Salt-Lake-City IJS reform of 2003-04), gymnastics (post-Athens Code of Points overhaul of 2006), Olympic diving (0.5-increment scale since the 1970s), and Olympic boxing (the McLaren report and IOC exclusion from Paris 2024). Three reforms have empirical track records of 30–50% identifiable-bias reduction in the seasons following implementation. The fourth has never been operationalized in any subjective sport at the institutional level; we describe its structure, illustrate it with the Chorus prediction stack's 49 SHA-locked WSL Championship Tour predictions, and propose its adoption by the International Surfing Association before LA 2028. We accompany the reform agenda with a SHA-locked prospective forecast for the 2028 Olympic surfing event, registered before LA28 in the Chorus prediction stack at git SHA `1ee95a5e4ccb`. The forecast specifies, in advance and resolution-criterion-locked: round-number share at LA28 (25.55%, 95% PI [20.49%, 30.62%]), USA wave-score uplift (+0.16 pts, 95% PI [−0.29, +0.62]), day-of-event amplification (+0.18 pts/day, [+0.04, +0.31]), and per-pairing controversy rankings for likely-drawn quarterfinals and semifinals. The forecast resolves at the LA28 final. If reforms 1–3 are implemented, the forecast becomes a reform-test rather than a baseline forecast — bias-amplitude reductions toward the cross-sport benchmark of 40–60% would falsify the unreformed predictions in the predicted direction. If reforms are not implemented, the forecast resolves against the unreformed baseline and the cross-sport literature receives a prospectively-scored data point on the cost of inaction. Either outcome is informative. We argue that the surfing case is uniquely positioned to test, prospectively and publicly, whether subjective-sport governance can reform on the strength of cumulative empirical evidence rather than on the strength of a discrete public scandal — a hypothesis the cross-sport reform record has, until now, never permitted a clean empirical test of.

_(~430 words.)_

---

## 1. Introduction

### 1.1 The LA28 reform window

Surfing returns to the Olympics in summer 2028 at Lower Trestles in San Clemente, California — the first Olympic surfing event held on host-country water for the United States and the first major-stakes international surf competition since Paris 2024. The competition window is 2028-07-29 to 2028-08-05; the venue is at NDBC buoy 46224; the judging panel will be assembled by the International Surfing Association from a pool that overlaps materially with the World Surf League Championship Tour judging pool. The host-country contingent is likely to be deep, the venue is one of the most-photographed surf venues in the world, and the broadcast stakes are substantial.

Two pieces of context matter for what follows.

**Context 1: The empirical evidence on subjective-sport bias has accumulated to a level the cross-sport literature has never seen for any single sport.** Companion Paper 1 (Conner et al. 2026, "Manufacturing Consensus") reports findings on the largest WSL judging corpus assembled to date — 60,834 panel-trim-mean wave-rows and 301,478 individual judge-scoring decisions across 17 seasons, 86.3% of judge-scores with nationality coverage, validated through an 18-gate identification harness. Companion Paper 2 (Conner et al. 2026, "Eighteen Gates and the Causality Ladder") proposes the methodology framework. The empirical findings include a permutation-test-causally-identified post-2023 panel-composition reform at the WSL (the H32 finding), a bulletproof per-judge round-number anchoring signature at 59.9% on .0 or .5 endings (3.0× the 20% uniform null — 2 of 10 possible tenth-endings), a descriptive Australian home-event effect that collapses to null under doubly-robust identification, and a Findlay–Ste-Marie reputation prior in heat-FE OLS (β = −0.013/rank, p = 1.8 × 10⁻⁴). The cross-sport literature on figure skating (Zitzewitz 2014; Akabas 2026), gymnastics (Heiniger & Mercier 2018, 2021), dressage (Veronesi et al. 2023), DanceSport (Premelč et al. 2019), and ski jumping (Krumer 2022) supports the broader pattern.

**Context 2: The cross-sport reform record is consistent and informative.** Every published reform of subjective-sport judging in the modern era has come *after* a public scandal: figure skating after Salt Lake City 2002, gymnastics after Athens 2004, Olympic boxing after Rio 2016 and the AIBA exclusion from Paris 2024. The cumulative academic evidence on bias across decades did not, in any of these cases, motivate reform on its own. What motivated reform was always a discrete, public, narratively-coherent rupture: a confession (figure skating), a CAS ruling (gymnastics), an IOC exclusion (boxing). Surfing has the empirical evidence. Surfing has not had the rupture.

The natural question is whether reform requires a rupture, or whether the cumulative empirical evidence — particularly when it is pre-registered, SHA-locked, and prospectively scored — can substitute for one. The 2028 LA Olympic surfing event is approximately 24 months out as of this writing. The reform window is open. The cross-sport reform menu is well-understood and operationally cheap. The pre-registered forecast for what LA28 will look like under unreformed judging is sealed.

This paper proposes the reform agenda and registers the forecast.

### 1.2 What this paper contributes

We make four explicit contributions.

**Contribution 1: An empirically-grounded four-part reform agenda for subjective-sport judging, applicable to surfing and operationalisable by the International Surfing Association before LA 2028.** The agenda combines three reforms with documented cross-sport bias-reduction track records (per-judge transparency, scoring-scale architecture, panel-rotation rules) and one reform that has never been operationalised at the institutional level (pre-registered, SHA-locked, public Brier-scored prospective predictions). We specify implementation, predicted bias reduction, and operational cost for each.

**Contribution 2: A SHA-locked prospective forecast for the 2028 Olympic surfing event.** Registered 2026-05-04 in the Chorus prediction stack at git SHA `1ee95a5e4ccb`. The forecast specifies bias-amplitude predictions on five mechanisms (round-number, USA-bloc, day-of-event amplification, reputation prior, panel composition) with 95% prediction intervals. The forecast resolves at the LA28 final. We document the prospective-falsification structure that makes the forecast a reform-test under reform implementation and a baseline under non-implementation.

**Contribution 3: A cross-sport reform precedent synthesis.** We document the historical record of subjective-sport judging reform in figure skating (1998–present), gymnastics (1980–present), Olympic boxing (1988–present), Olympic diving (1970–present), dressage (2010–present), and synchronised swimming (2008–present). We identify the common structural features of successful and unsuccessful reform episodes. The synthesis informs both the reform agenda's design and the implementation timeline.

**Contribution 4: A test of whether subjective-sport reform can occur from cumulative empirical evidence absent a public scandal.** No published prior reform episode has tested this hypothesis cleanly. The surfing case in 2026–2028 is the first empirical opportunity. We register the test, specify resolution criteria, and bind ourselves to publish the resolution post-LA28 regardless of outcome.

### 1.3 What this paper does not contribute

We do not claim originality on any of the cross-sport reforms we propose. Per-judge transparency was Zitzewitz's (2014) prescription. Scoring-scale architecture was operationalised in diving by FINA in the 1970s and in gymnastics by FIG in 2006. Panel-rotation rules were implemented in figure skating under IJS and in gymnastics post-Athens. The four-reform menu is a synthesis of the cross-sport reform record, not a novel proposal.

We do not claim that the pre-registered forecast will resolve in any particular direction. The forecast is a falsifiable instrument; it can resolve either way; we have committed to publishing the resolution. The substantive contribution is the prospective-resolution structure, not the predicted point estimates.

We do not claim that LA28-specific recommendations are operationally complete without ISA's internal data on judge selection, panel-assignment policy, scoring-tablet software, and broadcast-feed integration. The implementation specifications we offer are necessary conditions for reform, not exhaustive operational specifications. ISA's internal capacity to implement is, ultimately, the binding constraint.

We do not claim authority over the WSL or ISA. We are independent academic researchers. We make the case from the empirical evidence and the cross-sport precedent. The decision to implement reforms is the governing bodies'.

---

## 2. Cross-Sport Reform Precedent

Six modern reform episodes in subjective sports inform the agenda we propose. We summarise each by the same four dimensions: scandal trigger, reform structure, measured bias reduction, and unresolved residual.

### 2.1 Figure skating: Salt Lake City 2002 → IJS 2003-04

**Scandal trigger.** February 2002, Salt Lake City Olympic pairs final. French international judge Marie-Reine Le Gougne, 52 years old, with 20 years on the ISU roster, placed Russian pair Berezhnaya and Sikharulidze first ahead of Canadian pair Salé and Pelletier. The audience booed the result. Three hours after the final, in a closed meeting with referee Sally Stapleford, Le Gougne admitted that the head of the French federation had instructed her to vote for the Russians in exchange for Russian votes for the French ice-dance team. Within 72 hours the IOC awarded a duplicate gold to the Canadians; within four days the ISU suspended Le Gougne and the federation head; within 10 weeks the ISU announced architectural overhaul.

**Reform structure.** The International Judging System (IJS) replaced the 6.0 ordinal scale in stages from 2003 to 2008. Components: anonymous panels (judge identity hidden from broadcasters in real time, released post-event), random-selection of which judges' scores count (the trim-mean is computed over a random subset of the larger panel), per-judge score release with names attached after a 30-day lag, expansion of panels from 9 to 12+ judges with computational redundancy, abandonment of the holistic 6.0 scale in favor of element-by-element constructed scoring with categorised deductions.

**Measured bias reduction.** Zitzewitz (2014) measured compatriot bias pre- and post-IJS using the same statistical specification across regimes. The post-IJS compatriot bonus on identifiable categories was substantially reduced relative to the pre-IJS regime; the magnitude varies by category (some forms of bias dropped sharply, others moved less), but the direction is consistent. Akabas (2026, *Sportico*) measured the 2026 Milan-Cortina compatriot pattern and found 49 of 59 home-country judges scored their compatriots above the panel average — non-zero residual bias persists 24 years post-reform. Findlay & Ste-Marie (2004) had documented the reputation prior pre-IJS; the cross-sport literature broadly supports a ~50% reduction estimate as the typical IJS-era bias-reduction magnitude on identifiable channels.

**Unresolved residual.** Compatriot bias persists at smaller magnitude. Reputation prior (Findlay-Ste-Marie effect) persists. Round-number anchoring at element-level is reduced by the constructed-score architecture but not eliminated. The IJS reform was not a one-time fix; it has required ongoing incremental tuning over 24 years.

### 2.2 Gymnastics: Athens 2004 → FIG Code of Points 2006

**Scandal trigger.** August 2004, Athens Olympic men's all-around final. Korean gymnast Yang Tae-young's parallel-bars routine was assigned a start value of 9.9 by the FIG judging panel. American Paul Hamm scored 9.837 on his vault dismount and won gold by 0.012 points. South Korea filed a CAS appeal claiming Yang's start value should have been 10.0, which would have given him gold. CAS ruled that FIG had indeed miscalculated the start value, but that the Korean appeal was not filed within the required reporting window. Hamm kept the medal. The "wrong start value, no remedy" outcome made it impossible for FIG to defend the existing scoring architecture.

**Reform structure.** The 2006 FIG Code of Points overhaul abandoned the 10.0 holistic scale and introduced D-score (difficulty) plus E-score (execution). D-score is computed mechanically from the routine's content (each element has a published difficulty value). E-score is panel-judged from a 10.0 starting point with categorised deductions (0.1 per minor form break, 0.3 per fall, 0.5 per major form break). Total score is the sum. Round-number anchoring at the *final score* is structurally prevented because the final score is a sum of constructed components.

**Measured bias reduction.** Heiniger & Mercier (2018, 2021) documented persistent national bias post-2006 with magnitude depending on apparatus. On vault, where scoring is most mechanical, the bias residual is small. On floor exercise and balance beam, where execution scoring retains substantial holistic interpretation, the residual is larger. Inter-judge reliability ICC remained at 0.97–0.99 across the reform — the reform did not affect agreement, only the architecture of what panels were agreeing on.

**Unresolved residual.** Apparatus-dependent bias persists where holistic interpretation dominates execution scoring. The 2008 Beijing and 2012 London Olympics produced contested results despite Code of Points implementation. Reform reduced architectural vulnerability but did not eliminate the underlying shared-prior mechanism.

### 2.3 Olympic diving: 0.5-increment scale (continuous, 1970s–present)

**No scandal trigger of the figure-skating type.** Diving's reform precedent is structural rather than crisis-driven. FINA adopted a 0.5-increment 0-10 judging scale in the 1970s, partly in response to inter-judge variance issues that pre-dated the modern academic literature on subjective-sport bias.

**Reform structure.** Seven judges per panel, scores on 0-10 in 0.5 increments only (the input scale literally cannot register .25 or .75 endings). High and low dropped, middle five averaged, multiplied by degree of difficulty (DD). Per-judge scores are shown live on broadcast — judges are publicly accountable in real time, an even stronger form of transparency than figure skating's 30-day lag.

**Measured bias reduction.** Round-number anchoring at the .25/.75 level is structurally impossible (the input scale doesn't support those values). Compatriot bias persists at small magnitude. Inter-judge variance is among the smallest in any subjective sport.

**Unresolved residual.** Compatriot effects persist in close finals. The 0.5-increment scale partially substitutes for transparency but does not address the shared-prior mechanism. Live per-judge accountability appears to discipline anchoring further but is harder to attribute to a single reform.

### 2.4 Olympic boxing: Rio 2016 → AIBA exclusion 2024

**Scandal trigger.** Rio 2016 produced 11+ disputed decisions across the boxing tournament. The Lomachenko-style controversies, the Conceição decisions, the entire 56kg light-flyweight bracket: each produced a decision pattern the data and the broadcast both confirmed. AIBA suspended its own judges from active duty mid-tournament — the only modern instance of a subjective-sport governing body suspending its judges during a Games. The McLaren independent investigation in 2022 concluded that AIBA's judging governance was structurally compromised. In 2023, the IOC suspended AIBA's recognition. Boxing was excluded from the Paris 2024 Olympics.

**Reform structure.** Pending. The post-AIBA replacement governance body (World Boxing) is in early stages. The exclusion from Paris 2024 was the IOC's one and only use of the nuclear option in modern subjective-sport governance.

**Measured bias reduction.** Not yet measurable; reform incomplete.

**Unresolved residual.** All of it. Boxing is the cautionary case for what happens when governance refuses to reform.

### 2.5 Dressage: Veronesi et al. 2023, FEI persistence

**Scandal trigger.** No Salt Lake City moment. The cumulative academic literature has documented bias across multiple identity predictors at p < 0.001 (Veronesi et al. 2023). The FEI has been resistant to per-judge transparency reform. Cascade-bias mechanisms — where judges anchor on each others' previously announced scores in real time — are documented and unaddressed.

**Reform structure.** Largely unreformed. FEI judging operates with relatively limited public per-judge data and the cascade mechanism is structurally enabled by the broadcast format.

**Measured bias reduction.** Negligible.

**Unresolved residual.** Most of it. Dressage is the cautionary case for what happens when academic evidence accumulates but governance does not respond.

### 2.6 Synchronised swimming: Boen et al. 2008, FINA anonymous scoring

**Scandal trigger.** No scandal trigger; experimental evidence drove reform. Boen et al. (2008) ran a controlled experiment showing crowd noise influenced synchronised-swimming judging decisions even after the noise channel was removed (calibration drift persists). FINA introduced anonymous scoring in the 2010s.

**Reform structure.** Anonymous scoring during competition; per-judge release post-event. Modest by figure-skating standards but operational.

**Measured bias reduction.** Hard to assess due to limited public data; anecdotally meaningful.

**Unresolved residual.** Limited public data prevents systematic bias measurement; the reform's evaluative loop is incomplete.

### 2.7 The cross-sport pattern

Six reform episodes. Three were scandal-driven and resulted in substantial structural reform (figure skating, gymnastics, boxing). Two were structurally adopted independent of crisis (diving, synchronised swimming). One has been resistant despite cumulative evidence (dressage). The pattern is consistent: **public, undeniable rupture has driven reform in every modern subjective-sport governance overhaul.** Cumulative academic evidence absent rupture has driven partial reform (synchronised swimming, ski jumping marginally) but never the architectural overhauls associated with figure skating's IJS or gymnastics' 2006 Code.

The reforms that do work, when implemented, share three structural features: per-judge transparency with reputational discipline; scoring-scale or scoring-architecture changes that prevent the bias channel at the input layer; and panel-rotation rules that eliminate compatriot stacking. We propose all three for surfing.

---

## 3. The Four-Part Reform Menu

### 3.1 Reform 1: Public per-judge data with 30-day lag (Zitzewitz transparency)

**What.** ISA publishes per-judge scoresheets — every individual judge's score on every wave, with the judge's name attached — 30 days after each event resolves. The 30-day lag preserves the integrity of the judging process during competition (judges are not anchoring on each other in real time) while creating a public record post-event.

**Why.** Reputation-cost discipline. When a judge's individual scores are public and attributable, repeated identifiable bias becomes career-costly. The mechanism is informational, not coercive. The empirical record from figure skating (Zitzewitz 2014), gymnastics (post-2008 transparency), and diving (live per-judge display) supports a 30–50% reduction in identifiable bias on the channels measurable from per-judge data.

**Predicted bias reduction.** Cross-sport benchmark estimates: compatriot bias reduces by ~50% on identifiable channels; reputation prior reduces by ~30%; day-of-event amplification reduces by ~40%; round-number anchoring reduces marginally (not the primary channel transparency addresses). Net composite: 35–45% reduction across identifiable bias channels in seasons following implementation.

**Implementation.** A CSV release per event, formatted to specifications already used by ISU, FIG, and FINA. ISA already collects this data internally on the scoring tablet. Implementation cost is operational only — release pipeline, format specification, judge consent (or contract amendment). One event-day of testing before full deployment.

**Risk and mitigation.** Risk: individual judges face career consequences for past scoring patterns. Mitigation: the 30-day lag prevents individual judges from being targeted in real time; the cross-sport precedent shows reputation-cost discipline operates at the institutional level (judge selection for future events) rather than at the individual punitive level.

### 3.2 Reform 2: Scoring-scale architecture preventing round-number anchoring

**What.** Move the input scoring scale from 0.00–10.00 in 0.01 increments to either (a) 0–100 integer scale with division-by-10 for display, or (b) 0.0–10.0 in 0.5 increments (the diving model). The two alternatives have different trade-offs.

The 0–100 integer scale preserves the displayed precision (0.0 to 10.0 in 0.1 increments) while eliminating .25 and .75 endings from the input scale. Judges cannot anchor on quarter-points because quarter-points do not exist on the input.

The 0.0–10.0 in 0.5 increments matches diving's structural reform exactly. It accepts a coarser displayed scale in exchange for stronger anchor elimination — judges can only anchor on whole and half points, which is the same input precision the rest of the panel sees, making any cross-judge anchoring discrepancy maximally visible.

**Why.** Round-number anchoring at the .0/.5 level is the most-bulletproof bias signature in our 17-year corpus (59.9% per-judge clustering on .0 or .5 endings, 3.0× the 20% uniform null — 2 of 10 possible tenth-endings). It is independent of every other measured channel. It is a property of human cognition under time pressure, not a property of WSL judges specifically. The fix is structural: prevent the bias at the input layer rather than retraining judges.

**Predicted bias reduction.** 0–100 integer: round-number clustering at .25/.75 level eliminated by construction; .0/.5 anchoring persists but at lower magnitude (~30% reduction in trim-mean clustering, by simulation against our existing data). 0.0–10.0 0.5-increment: round-number clustering at .25/.75 level eliminated; .0/.5 clustering becomes structurally maximal (since those are the only options) but is then equally distributed across the panel, making cross-judge bias maximally visible.

**Implementation.** Software update to the scoring tablet. Judge handbook documentation. One event-day of pilot testing. Operational cost is engineering time, not infrastructure investment.

**Risk and mitigation.** Risk: judges and surfers culturally accustomed to 0.01 input precision may resist. Mitigation: the displayed precision is unchanged under the 0–100 integer reform; under the 0.5-increment reform, fan-side experience is unchanged (the displayed scale is still 0.0 to 10.0). Only the judge's internal counting palette changes, and the cross-sport precedent shows judges adapt within one season.

**Why architectural rather than operational.** A natural alternative reform is operational rather than architectural: extend the per-wave deliberation window. Conner (2026, Paper 4 — companion paper, *Time Pressure Does Not Explain Round-Number Anchoring*) tests this directly on a held-out 2025 sample of 14,106 judge decisions. Across three pre-registered time-pressure proxies — wave-density, fatigue, and end-of-heat — only fatigue replicates as a small effect (~1.8 pp), the wave-density effect does not replicate (sign-reversed on hold-out), and the end-of-heat effect goes against the canonical "scramble" prediction (judges anchor 9 pp *less* in the final 3 minutes, not more). The largest predicted-direction shift across all three operationalizations is approximately 1.8 pp on a 21.4 pp anchoring excess. Extending the per-wave deliberation window will not meaningfully reduce anchoring; the architectural fix at the input scale layer remains the only intervention with defensible expected effect.

### 3.3 Reform 3: Panel-rotation rules preventing compatriot stacking

**What.** Explicit rule that no judge can be assigned to a panel scoring a heat that contains a compatriot surfer. Implementation can be soft (panel-assignment algorithm preferentially excludes compatriot judges where pool depth allows) or hard (compatriot judges are mechanically ineligible for the heat).

**Why.** The compatriot panel-composition channel is the most-narratively-charged bias channel in subjective sport. Even when the per-judge behavioral compatriot effect is null or small (as our per-judge DiD analysis on WSL data suggests), the optics of panel composition are real. The reform mechanically eliminates the channel. Gymnastics and figure skating have implemented this rule in various forms post-reform.

**Predicted bias reduction.** Panel-composition compatriot effect: mechanically zero. Behavioral compatriot effect (per-judge DiD): plausibly ambiguous; depends on whether judges adjust their behavior under the new panel-assignment regime. Optical compatriot effect (the appearance of bias to fans and broadcasts): substantial reduction.

**Implementation.** Panel-assignment policy update. Software-supported by the existing scheduler. The WSL appears to have implemented this informally between October 2023 and 2026 (panel-judge counts on Brazilian-surfer panels declined from 1.72 to 0.84, with permutation p < 0.001). ISA can adopt this directly for LA28 with the WSL precedent as institutional cover.

**Risk and mitigation.** Risk: in shallow judging pools (small countries in large fields), the rule may produce panel-assignment infeasibility. Mitigation: the rule applies preferentially rather than mechanically when pool depth is insufficient; documented exceptions are flagged in the per-judge transparency release.

### 3.4 Reform 4: Pre-registered, public, Brier-scored prospective predictions

**What.** Independent research groups register specific, falsifiable, quantitative predictions about what bias signatures will look like at each upcoming event. Each prediction is committed to a public ledger with a SHA-256 hash so it cannot be retroactively edited. Each prediction has a pre-specified resolution criterion. After the event, binary outcome predictions are scored with the Brier score (mean squared error between forecast probability and the 0/1 outcome; 0 = perfect, 0.25 = chance for a 0.5 forecast, 1 = maximally wrong), while continuous interval forecasts (round-number share, USA uplift, day-slope) are scored with the continuous ranked probability score (CRPS), not the Brier score. The aggregation rule — how Brier and CRPS scores combine into a composite headline metric — will be finalized in the locked resolution protocol before the first resolution event. The composite scores accumulate publicly across events, providing a continuous accountability metric for the analysis community and an indirect monitoring signal for governance.

**Why.** Reform persistence. Without a continuous monitoring layer, even the best one-time architectural reform decays. Per-judge transparency only works if someone is reading the data. Public Brier-scoring is the cross-sport-equivalent of an audit committee: it operates indefinitely, publishes its results, and forces analysts to put their reputations behind their claims. The mechanism disciplines the *analysts* more than the judges, but it disciplines them in a way that compounds over time.

**Predicted reform persistence.** Indefinite. So long as the Brier scoring is public, the analysis community is constrained to publish predictions that resolve and to accept the consequences when they don't.

**Implementation.** Zero institutional cost. The infrastructure already exists in the Chorus prediction stack at our public replication archive. The 49 SHA-locked WSL Championship Tour predictions registered for 2026 events resolve automatically as those events conclude. ISA needs only to acknowledge the existence of independent prospective-prediction infrastructure and invite registration of LA28-specific predictions before the event.

**Risk and mitigation.** Risk: this reform has never been operationalised in any subjective sport. Implementation may surface unanticipated incentive distortions (e.g., prediction-gaming, malicious-pre-registration). Mitigation: the cross-sport literature on prediction markets and forecasting tournaments (Tetlock, Mellers, etc.) has addressed analogous concerns in adjacent domains; the implementation specification in the Chorus prediction stack incorporates SHA-locked commitment, public scoring, and resolver independence as standard guards.

### 3.5 Why all four together

The four reforms are partially independent, attacking partially independent bias channels. Reform 1 (per-judge transparency) disciplines individual judge behavior. Reform 2 (scoring-scale architecture) eliminates the round-number input pathway. Reform 3 (panel rotation) eliminates the compatriot composition pathway. Reform 4 (prospective Brier scoring) disciplines the analytical community and provides continuous monitoring.

The cross-sport literature converges on a magnitude estimate: a sport implementing all three of Reforms 1–3 sees identifiable-bias reduction of 40–60% in subsequent seasons. The fourth reform's predicted effect is not on bias magnitude per se but on reform durability — an independent property that the cross-sport literature has not been able to test cleanly because no prior reform has been continuously monitored at this granularity.

Implementation order matters less than implementation completeness. The WSL precedent suggests Reform 3 can be implemented quietly without policy infrastructure. The diving and figure-skating precedents suggest Reform 2 and Reform 1 require explicit policy change but no methodological controversy. Reform 4 has zero institutional cost and can be adopted at any time — including, if ISA wishes, immediately as a pre-LA28 commitment.

---

## 4. The SHA-Locked Prospective Forecast for LA 2028

### 4.1 Registration and resolution

The prospective forecast for the 2028 Olympic surfing event was registered 2026-05-04 in the Chorus prediction stack at git SHA `1ee95a5e4ccb`, against the WSL training corpus heats SHA `7f07fb121abe` and the Olympic 2024 retrospective replication SHA `25f500d8c769`. The public predictions are sealed in `outputs/olympic_2028_la_predictions.md`; the per-surfer appendix is held privately pending an OSF embargo deposit, with its SHA-256 published at `outputs/SEALED_PREDICTIONS_SHA256.txt`. They will resolve at the LA28 surfing final, expected mid-August 2028. Resolution criteria are pre-specified per prediction; the resolver is the Chorus prediction stack's `wsl_brier_hook.py` running against the LA28 results data when published by ISA.

### 4.2 Per-mechanism predictions

We register predictions on five primary mechanisms, derived from the WSL training corpus and the Olympic 2024 retrospective data weighted by Olympic-event relevance.

**Round-number share.** The predicted share of LA28 individual judge-scores ending in .0/.25/.5/.75 is **25.55%** with a 95% prediction interval of [20.49%, 30.62%]. The mixture model weights are 60% Olympic 2024 retrospective + 40% WSL Championship Tour base rate. Excess versus the trim-mean uniform null (6.67%): 3.83× [3.07×, 4.59×]. This is the sharpest forecast in the family — falsification at the prediction-interval boundary is informative.

**USA wave-score uplift.** The predicted host-country uplift on USA-surfer scores at LA28, computed against pooled-event baseline, is **+0.163 points** with a 95% prediction interval of [−0.290, +0.617]. The interval is wide because three available anchors disagree: Lower Trestles WSL data alone returns +0.41 (small sample); USA-CT-pooled returns +0.03 (large sample, no Olympic stakes); Paris 2024 host-country null returns −0.02 (nearby event, low n). The wide PI reflects honest uncertainty about which anchor transfers cleanly to LA28; falsification within the wide PI is uninformative; falsification outside the wide PI substantially constrains transferability.

**Day-of-event amplification.** Predicted slope of mean wave-score on event-day, controlling for surfer skill: **+0.176 points per event-day**, 95% PI [+0.040, +0.312]. Smaller than the WSL CT baseline (+1.17/day) because the Olympic-event format compresses to fewer days and Paris 2024 returned null with n=14.

**Reputation prior.** Predicted heat-FE coefficient on inverted world rank: **β = −0.013** [−0.024, −0.003]. Replicates WSL training-period estimate; Olympic 2024 returns same-direction coefficient at p_bonf = 0.027, n = 108.

**Compatriot panel composition.** Under unreformed ISA panel composition: predicted share of LA28 heats with at least one USA judge on a USA-surfer panel: **~70%**. Under Reform 3 implementation: predicted share **0%** (mechanical elimination).

### 4.3 Per-pairing controversy rankings

The forecast registers 10 most-likely-controversial pairings if they are drawn at LA28. Each pairing combines a high-controversy USA-vs-foreign matchup with a substantial seeding gap that makes a close result statistically unlikely without a bias channel. The full ranking is in the locked prediction file; the top three pairings, all hypothetical until brackets are drawn:

1. Seth Moniz (USA, projected seed 19) vs Italo Ferreira (BRA, projected seed 2) — controversy score 1.85
2. Imaikalani deVault (USA, projected seed 18) vs Italo Ferreira (BRA, projected seed 2) — 1.80
3. Seth Moniz (USA) vs Jack Robinson (AUS, projected seed 4) — 1.75

These are *if-drawn* predictions: the controversy scores apply conditional on those pairings actually occurring. Once the LA28 brackets are drawn, the active subset of predictions resolves; the rest archive without resolution.

### 4.4 Per-surfer forecast (sealed appendix)

Per-surfer robbery and unfair-gift risk rankings are held privately pending an OSF embargo deposit; the SHA-256 of the sealed prediction file is published in the replication archive at `outputs/SEALED_PREDICTIONS_SHA256.txt`. The methodology is published in full; the per-surfer rankings are deliberately not included in the body of the public-facing companion piece (Conner et al. 2026 Substack series, Piece 6) because individual athletes will read the predictions before competing and the reputational asymmetry is unfavorable. The per-surfer file unseals when the LA28 surfing final concludes; the SHA-256 commit in the archive proves the predictions were locked before that event.

### 4.5 Falsification design

The forecast is structured to be informative under both reform and non-reform.

**Under Reform 3 (panel rotation) implementation:** Compatriot panel-composition forecast is mechanically falsified to 0%. Per-judge compatriot DiD effects on USA-surfer scores should drop within the cross-sport benchmark of ~50% reduction.

**Under Reform 2 (scoring-scale architecture) implementation:** Round-number share forecast falsified downward — predicted ~25% becomes ~12-15% under integer-scale reform, lower under 0.5-increment reform. The falsification is in the predicted direction and informative about the magnitude of the cognitive-anchoring channel.

**Under Reform 1 (per-judge transparency) implementation:** Reputation prior, day-of-event amplification, and host-country uplift forecasts should all reduce by 30–50% per cross-sport benchmark.

**Under no reform:** All forecasts resolve against the unreformed baseline. The cross-sport hypothesis (subjective-sport governance requires a scandal to reform) is supported. The empirical-evidence-alone hypothesis is rejected.

Either resolution is informative. The forecast is registered to be falsifiable in either direction.

---

## 5. Implementation Timeline and Counterfactual Scenarios

### 5.1 Recommended ISA implementation timeline

If ISA wishes to implement Reforms 1–3 before LA28 with sufficient lead time for cross-sport-benchmark bias-reduction effects to compound and for measurement to be feasible:

**Q4 2026.** ISA committee adopts the panel-rotation rule (Reform 3) for the 2027 World Surfing Games. The rule requires no methodological controversy and no infrastructure investment.

**Q1 2027.** Software update for integer-scale or 0.5-increment scoring (Reform 2). Pilot at WSG 2027. Cross-sport precedent (figure skating IJS pilot 2003, gymnastics 2006 Code pilot) suggests one event-day of test deployment is sufficient.

**Q2 2027.** Public per-judge data release pilot (Reform 1). One event, full-CSV release with judge-name attribution, 30-day lag.

**Q3 2027.** Publish initial results from the Q1+Q2 pilots. Refine based on operational lessons. Update judge handbook and athlete-facing communications.

**Q4 2027.** Full implementation across all ISA-sanctioned events. Reform 4 (Brier-scored prospective predictions) operationalised independent of the other reforms — Chorus prediction stack registers all 2028 ISA-event predictions ahead of resolution.

**Summer 2028.** LA28 surfing event judged under the four-reform regime. The pre-registered LA28 forecast becomes a reform test rather than a baseline.

The timeline is feasible. Each step's operational cost is modest. The cross-sport reform precedent suggests 18-month lead times are sufficient for full cultural adoption. The window is open.

### 5.2 Counterfactual: what happens under reform implementation

If Reforms 1–3 are implemented before LA28 according to the timeline above, the cross-sport benchmark predicts:

- LA28 round-number share drops from a predicted 25.55% to approximately 12–15% (cognitive-anchoring channel substantially reduced by the scale architecture)
- LA28 host-country compatriot panel composition drops to 0% (mechanical elimination)
- LA28 host-country wave-score uplift drops by approximately half from the unreformed baseline; the reformed point estimate would be ~+0.08 with prediction interval likely overlapping zero
- Day-of-event amplification reduces by approximately 40% (estimate ~+0.10 pts/day)
- Reputation prior reduces marginally (transparency disciplines individual behavior but not the pooled coefficient much)

The pre-registered LA28 forecast resolves systematically against the unreformed predictions — the predictions are falsified downward in the direction the reforms predict. The cross-sport hypothesis (reform reduces but does not eliminate bias) is supported. Surfing becomes the first subjective sport to demonstrate evidence-driven reform without a public scandal.

### 5.3 Counterfactual: what happens under non-implementation

If reforms are not implemented, the LA28 surfing event proceeds under the unreformed regime. The pre-registered forecast resolves against the unreformed baseline:

- Round-number share is observed at approximately 25% on .0/.25/.5/.75 (within the predicted interval)
- USA host-country wave-score uplift is observed somewhere in the predicted [−0.29, +0.62] range; the venue and seeding effects we identified at Bells Beach (2025 Bonsoy +0.612) plausibly transfer to Lower Trestles
- Disputed pairings produce broadcast controversy of the kind that has historically forced reform in other subjective sports
- The cross-sport hypothesis (subjective-sport governance requires a scandal to reform) is supported; the empirical-evidence-alone hypothesis is rejected
- The cross-sport literature receives a prospectively-scored data point on the cost of inaction

The non-implementation counterfactual is, scientifically, a falsification of the more optimistic of the two competing reform-hypotheses. It is also, plausibly, the trigger for the LA28-itself-as-scandal scenario in which the IOC takes the boxing-style nuclear option for the next Olympic cycle.

### 5.4 Counterfactual: partial implementation

The most likely scenario, given cross-sport precedent, is partial implementation. ISA implements Reform 3 (panel rotation) following the WSL precedent — operational, low controversy, modest cost. ISA does not implement Reforms 1 or 2 in time for LA28 due to either institutional inertia or regulatory cycle. Reform 4 operates independent of ISA via the Chorus prediction stack.

Under partial implementation, the LA28 forecast resolves mixed: the compatriot panel-composition forecast is falsified downward; the round-number share resolves close to the unreformed baseline; the host-country uplift resolves within the predicted interval but at the upper end. The cross-sport hypothesis is partially supported.

---

## 6. Discussion

### 6.1 The wider hypothesis being tested

Beyond LA28 surfing, the project tests a hypothesis the cross-sport literature has been unable to evaluate cleanly: **whether subjective-sport governance can reform from cumulative empirical evidence alone**. Every modern reform episode in the cross-sport record has been scandal-driven. The cumulative academic evidence on bias has, in every case, accumulated to a magnitude that should have been sufficient to motivate reform — and in every case, the governing bodies waited for a scandal before acting.

If the LA28 case is consistent with the historical record, the implication is that subjective-sport governance is structurally incapable of evidence-driven reform. The IOC's nuclear option (boxing 2024) becomes the operational mechanism by which sports unable to self-reform are forced to reform. The cumulative academic literature has documentary value but no corrective value.

If the LA28 case breaks the pattern — if ISA implements one or more of the proposed reforms in response to cumulative evidence rather than in response to a scandal — the implication is more optimistic. Evidence-driven reform is feasible. The cross-sport literature has been undervaluing its own corrective potential. Other sports with documented bias residuals (dressage, DanceSport, ski jumping) gain a precedent for evidence-as-trigger.

The prospective forecast we register is the falsifier for both hypotheses simultaneously. We have committed to publishing the resolution. The science of subjective-sport governance reform is, with this paper, an empirical rather than a historical question.

### 6.2 What could go wrong with the forecast

We discuss four threats to the validity of the prospective forecast.

**Threat 1: ISA-WSL judge pool divergence.** Our training corpus is WSL Championship Tour data. The Olympic surfing event uses an ISA-administered panel. The two pools have meaningful overlap but are not identical. If ISA's panel is structurally different — e.g., heavier on non-WSL international judges, different age distribution, different training pipeline — the bias-mechanism transfer assumptions of the forecast may fail. We document this as an assumption rather than a claim. The forecast's prediction intervals incorporate Paris 2024 data (which was ISA-paneled) at the 60% mixture weight to partially address this.

**Threat 2: Venue idiosyncrasy.** Lower Trestles is a high-performance venue with characteristics different from any single WSL Championship Tour stop. Wave-quality conditions, swell direction, and tide phase produce performance distributions that differ from training-corpus venues. The forecast relies on transfer of bias-mechanism architecture, not on transfer of absolute scoring distributions. Even so, venue-specific deviations from the predicted intervals could reflect venue effects rather than mechanism failure.

**Threat 3: Olympic-stakes amplification.** Olympic competition produces stakes-pressure dynamics that exceed Championship Tour competition by an order of magnitude. The day-of-event amplification mechanism may scale differently. The compatriot-bias mechanism (where present) may amplify in close finals. Our forecast extrapolates from CT-stakes data to Olympic-stakes; this extrapolation is uncertain.

**Threat 4: Unanticipated reforms.** ISA could implement reforms we have not anticipated, in directions we have not anticipated. The forecast is structured to falsify under the four reforms we do propose; under reforms outside that set, resolution interpretation requires post-event judgment.

We address these threats by publishing the forecast with transparent assumption-documentation, by registering the prediction intervals broadly enough to absorb expected venue and stakes variance, and by committing to publish the resolution analysis with full uncertainty disclosure post-LA28.

### 6.3 What this paper does not claim about ISA

We do not claim ISA is unwilling to reform. We do not claim ISA is corrupt. We do not claim individual ISA judges are biased. We document a cross-sport historical pattern, propose reforms grounded in that pattern, and register a forecast that resolves either way. The paper is an offer of evidence-based reform proposals, not an indictment.

We also do not claim the Chorus prediction stack is the only or best mechanism for prospective Brier scoring. Other independent groups should register their own predictions. The infrastructure should be plural; the registration discipline is what matters, not which specific platform implements it.

### 6.4 Conclusion

Subjective-sport judging reform has, in the modern era, required a scandal to occur. Surfing is the first sport where the empirical evidence is now sufficient to motivate reform on its own merits, and where the Olympic timeline (LA28 in approximately 24 months) creates a natural reform-implementation window. We propose four reforms — three with cross-sport empirical track records, one operationally novel. We register a SHA-locked prospective forecast for LA28 that resolves either as a reform test or as an unreformed-baseline forecast, depending on what ISA does between now and summer 2028. The hypothesis under test is whether cumulative academic evidence can substitute for a public scandal as a reform trigger. The hypothesis has never been cleanly tested in the cross-sport record. The surfing case is the first opportunity. We commit to publishing the resolution.

---

---

## Data Availability Statement

All data and code supporting the findings in this manuscript are publicly available at the project replication archive: **https://github.com/addie-conner/wsl-judging-bias-2026**.

The archive contains: the aggregate dataset (`data/heats.parquet`, 24,901 panel-trim-mean wave-rows, 2022–2025) and the full panel corpus (60,834 panel-trim-mean wave-rows, 2009–2026); the per-judge corpus (`data/judges.parquet`) containing 301,478 individual judge-scoring decisions, with judge nationality on 86.3% of judge-score values; the sealed 2025 women's CT hold-out manifest (`data/HOLDOUT_MANIFEST.json`, n = 1,815 wave-rows; sha256 `0c1616d755c3199430a094201209f282759da1fc3826cece0dfdce8f627c371a`; locked 2026-05-03 UTC); the pre-registered hypotheses and specifications (`outputs/preregistration_2026-05-03.md`, sealed at git SHA `7d0e2c8` on 2026-05-03 UTC); 49 SHA-locked prospective predictions (`outputs/olympic_2028_la_predictions.md`, registered at git SHA `1ee95a5e4ccb`); analysis scripts (Tier 1–5 + comprehensive battery + per-judge counterfactual + sponsor-alignment) under `scripts/`; and SHA-traceable analysis result files for each test in the 18-gate validation harness under `outputs/*.json`.

Per-judge scoring data was assembled from publicly accessible sources: a public, unauthenticated score-detail endpoint on worldsurfleague.com, the pre-2022 WSL events directory pattern recovered from Common Crawl WARC archives, and Wayback Machine snapshots of WSL competition pages. No proprietary or authenticated WSL data was used.

The repository is committed at the SHA referenced in the pre-registration. Subsequent commits add analyses but do not modify the pre-registered specifications or the hold-out manifest.

## References

(Full reference list shared with Conner et al. 2026 Papers 1 and 2. Additions specific to Paper 3 include:)

International Olympic Committee. (2023). _Decision regarding boxing at Paris 2024 Olympic Games._ IOC Executive Board, Lausanne.

International Surfing Association. (2024). _ISA Olympic surfing competition manual: Paris 2024._ ISA, San Diego.

McLaren, R. H. (2022). _Independent investigation: AIBA scoring and refereeing in Olympic boxing._ McLaren Global Sport Solutions.

Mellers, B., Stone, E., Murray, T., et al. (2015). Identifying and cultivating superforecasters as a method of improving probabilistic predictions. _Perspectives on Psychological Science_, 10(3), 267–281.

Tetlock, P. E., & Gardner, D. (2015). _Superforecasting: The art and science of prediction._ Crown Publishers.

(Plus full reference list from Papers 1 and 2.)
