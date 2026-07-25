# High Agreement, Small Biases: A Per-Judge Analysis of World Surf League Judging

## Authors and contact

Addie Conner (independent; Chorus Research). Corresponding author: addieconner@gmail.com. ORCID: https://orcid.org/0009-0007-7853-4140.

_Replication archive:_ https://github.com/addie-conner/wsl-judging-bias-2026

---

## Abstract

We assemble a per-judge scoring corpus for the World Surf League (WSL) Championship Tour and use it to test the biases most often alleged against surf judging. The corpus is 301,478 individual judge-score decisions drawn from 60,834 scored waves, together with a 24,901-row panel-level analysis set covering the 2022–2025 seasons. The result is largely exculpatory. A per-judge difference-in-differences design, which compares how compatriot and non-compatriot judges on the *same* panel score the *same* wave, finds no compatriot premium: at Brazilian events Brazilian judges score Brazilian surfers 0.024 points *lower* than their non-Brazilian panel-mates do (10,995 decisions), and at Australian events the Australian-judge premium is +0.108 with a bootstrap confidence interval that crosses zero (19,688 decisions). The most-cited home-advantage statistic in surf commentary — a +0.616-point Australian home-event coefficient in naive ordinary least squares — collapses to essentially zero under within-heat comparison, targeted maximum likelihood estimation (+0.005, CI crossing zero), and a causal forest (−0.024), and a within-event permutation test does not reject the null (p = 0.126); the raw effect is localized to a single venue. Inter-judge agreement is near ceiling, consistent with prior WSL reliability work. The one bias that survives every check is round-number anchoring: on the true 0.1-precision scale, 59.9% of judge scores end in .0 or .5 against a 20% null, a 3.0× excess, replicated across gender, year, judge nationality, and event. We also report a descriptive decline in Brazilian-judge representation on Championship Tour panels between 2018 and 2026; because Brazilian judges thinned on *all* panels in lockstep, not only on Brazilian-surfer panels, we cannot separate a change in roster supply from a change in assignment policy, and we advance no causal claim. Every number in the paper is reproduced by a committed script against the public data.

---

## 1. Introduction

When a sporting contest is decided by a panel of human judges scoring on an interpretive rubric — figure skating, gymnastics, diving, dressage, ski-jumping style, professional surfing — two empirical patterns recur. Judges agree with each other to a striking degree, with intraclass correlations often above 0.90 in codified-rubric sports (Heiniger and Mercier 2021; Santos et al. 2025). At the same time, panels exhibit measurable patterns on identity-correlated covariates the rubric does not name. Compatriot bonuses have been estimated at roughly +0.45 within-performance standard deviations in figure skating (Zitzewitz 2006; 2014), at about +0.09 style points in ski jumping (Krumer, Otto, and Pawlowski 2022), and across multiple identity predictors in dressage (Wolframm 2023). Reputation effects at the evaluation stage appear in figure skating (Findlay and Ste-Marie 2004) and Olympic gymnastics (Heiniger and Mercier 2021). The methodological lesson repeated across two decades is that high inter-judge reliability and unbiased judging are independent panel properties: a panel can agree with itself precisely while agreeing on a biased number.

Professional surfing has been under-studied relative to this literature. Two peer-reviewed quantitative studies of WSL judging exist as of this writing. Santos et al. (2025), working with 4,095 manually scraped waves from the 2021 men's Championship Tour, reported an inter-judge intraclass correlation of 0.97–1.00 and framed the result as evidence of judging reliability. Naumann and Rösch (2026) report a panel-level home-advantage analysis on the men's Championship Tour; the sample window and coefficients from that paper should be read from the published version rather than reproduced here. Neither study analyzed the women's tour, neither extended into the post-2022 window, and neither ran the doubly-robust identification battery now standard in the labor-economics and political-economy literatures on discrimination.

This paper makes three contributions, and the headline is that careful identification mostly *exonerates* WSL judging rather than indicting it.

First, we assemble a per-judge WSL corpus at scale — 301,478 individual judge-score decisions across 60,834 scored waves — and use it to run the cleanest available test of the compatriot mechanism: a within-panel, within-wave comparison of how compatriot and non-compatriot judges score the same ride. At that resolution the compatriot premium is zero or slightly negative on both the Brazilian and the Australian event corpora. The named-individual version of the test — Jack Robinson and Ethan Ewing at Margaret River, the two most-discussed Australian-surfer/Australian-venue pairings — is likewise null.

Second, we show that the single most-cited home-advantage number in surf commentary, a +0.616-point Australian home-event coefficient, is an artifact of aggregation and venue mix. Within-heat comparison, targeted maximum likelihood estimation, a causal forest, and a within-event permutation test all return a null, and a leave-one-event-out diagnostic traces the raw effect to a single venue with a plausible performance-genuine local-knowledge component. We report reliability near ceiling, consistent with Santos.

Third, we isolate the one bias that survives every check — round-number anchoring — and restate it correctly for the scale WSL actually uses. On the 0.1-precision score scale, 59.9% of individual judge scores end in .0 or .5 against a 20% null, a 3.0× excess that replicates on every disaggregation and on a temporally held-out sample.

We also document, descriptively, a decline in Brazilian-judge representation on Championship Tour panels between 2018 and 2026. We treat this as description, not identification: because Brazilian judges thinned on all panels in lockstep, a change in judge supply (roster churn) cannot be separated from a change in assignment policy without judge-identity data we do not have.

The paper is organized as follows. Section 2 describes the corpus and its coverage limits. Section 3 reports the per-judge compatriot counterfactual, including the named-individual checks. Section 4 reports the collapse of the Australian home-event effect under doubly-robust identification. Section 5 reports round-number anchoring on the corrected scale. Section 6 is the descriptive panel-composition section. Section 7 reports replication on a held-out 2025 women's-tour sample. Section 8 discusses implications, and Section 9 states the limitations.

## 2. Data

The per-judge corpus contains 301,478 individual judge-score decisions, recovered from 60,834 scored waves on the WSL Championship Tour spanning the men's and women's tours (`data/judges.parquet`). Each wave row carries up to five judge scores with the scoring judge's nationality; melting those columns yields the decision-level corpus. A separate panel-level analysis set, `data/heats.parquet` (24,901 rows, 2022–2025), carries surfer nationality, world rank, venue, and break direction, and is the basis for the doubly-robust analyses in Section 4 and the held-out replication in Section 7.

Two coverage facts govern what the corpus can and cannot support, and we state them plainly because prior drafts of this work overstated coverage. Judge nationality is present only from 2018 onward: it is absent for every 2009–2017 row. Surfer nationality, in the per-judge file, is present only *before* 2018; for 2018-and-later rows it must be imputed from a surfer-name-to-country map built from the panel-level set. That map covers 110 distinct surfers and fills surfer nationality on 68.5% of 2018-plus per-judge rows. The two fields the panel-composition question requires — judge nationality and surfer nationality — therefore co-occur only from 2018 onward, and only on the imputed subset. Any analysis that needs both, including Section 6, is a 2018–2026 analysis on imputed-nationality rows; the pre-2018 layer, however large, contributes nothing to it. We do not claim continuous 2009–2026 nationality coverage.

The data were assembled from publicly accessible sources only. The 2022–2026 per-judge scores come from a public, unauthenticated score-detail endpoint on worldsurfleague.com that returns per-judge scores for a given wave. Pre-2018 event pages, which exposed per-judge scores in public HTML before the site consolidated to a server-side API, were recovered from Common Crawl WARC archives; gaps in the 2018–2021 window were filled from Wayback Machine snapshots. No proprietary or authenticated WSL data was used.

The 2025 women's Championship Tour (1,815 panel rows) was held out as a temporal split for the replication in Section 7 and was not opened during the discovery analyses.

Analyses were run in Python 3.11 with pandas, statsmodels 0.14, and econml 0.16 (targeted maximum likelihood and causal forest). Each reported number is produced by a committed script in `scripts/`, writing a committed result file in `outputs/`; the relevant script and output are named at each result below.

## 3. The compatriot counterfactual

The cleanest test of a compatriot bonus does not regress scores on a compatriot indicator across panels — such a coefficient mixes venue, surfer selection, and calibration drift with any behavioral effect. It compares, within the same wave and the same panel, the score a compatriot judge gives to the score a non-compatriot judge on that same panel gives the same ride, and differences that against the analogous comparison for non-compatriot surfers. That two-by-two difference-in-differences nets out both any wave-level quality signal and any fixed calibration offset a judge population carries.

We run this design at Brazilian events and at Australian events (`outputs/per_judge_counterfactual_2026-05-04.json`). At Brazilian events (10,995 decisions), the cell means are: Brazilian surfer × Brazilian judge 3.017; Brazilian surfer × non-Brazilian judge 3.099; non-Brazilian surfer × Brazilian judge 2.956; non-Brazilian surfer × non-Brazilian judge 3.013. The implied difference-in-differences is −0.024 — Brazilian judges score Brazilian surfers slightly *lower* than their non-Brazilian panel-mates do, once the Brazilian-judge calibration offset estimated on non-Brazilian surfers is removed. The sign is opposite to the compatriot-favoritism prediction and the magnitude is negligible.

At Australian events (19,688 decisions) the difference-in-differences is +0.108, with a 95% bootstrap confidence interval of [−0.062, +0.266] that crosses zero. The point estimate is in the compatriot-favoritism direction but is not distinguishable from no effect.

**Named-individual check.** We re-ran the comparison for the two Australian surfers most often named in home-cooking complaints, at the venue where those complaints concentrate — Margaret River (`scripts/named_individual_counterfactual.py`, `outputs/named_individual_counterfactual_2026-07-25.json`). Because judge nationality exists only from 2018, only 2018-and-later Margaret River appearances contribute judge-decision rows. For Jack Robinson, Australian judges scored him 4.206 on average across 354 decisions and non-Australian judges scored him 4.225 across 641 decisions — a difference of −0.019 (Welch t = −0.10, p = 0.92). For Ethan Ewing, Australian judges scored him 5.180 (234 decisions) and non-Australian judges 5.125 (345 decisions), a difference of +0.055 (t = 0.26, p = 0.79). In both cases the compatriot-versus-non-compatriot gap is statistically indistinguishable from zero, and neither direction supports systematic home-judge padding of these surfers' scores.

(An earlier draft of this work reported these named-individual comparisons with different numbers — Robinson near-identical at 4.277 vs 4.276 across "630" decisions, Ewing 5.371 vs 5.410 — sourced from a computation whose committed output was empty. The values above are the recomputation from the committed data and supersede those figures.)

The counterfactual rules out the simplest compatriot mechanism: judges padding same-nationality surfers' scores above what their panel-mates give on the same waves. It does not rule out subtler between-panel selection — for instance, compatriot judges being assigned systematically to easier-to-score conditions — and the data cannot test that mechanism directly.

## 4. The Australian home-event effect does not survive identification

The most-quoted statistic in WSL bias commentary is a home-advantage coefficient for Australian surfers at Australian events. In our corpus a naive ordinary-least-squares regression of wave score on an Australian-surfer-at-Australian-event indicator returns +0.616 (95% CI [+0.499, +0.741], 1,340 matched waves, p = 2.0 × 10⁻⁹; `outputs/full_paper_grade_results.json`, `outputs/tier2_results.json`). Taken alone, it looks like a large home bias. It does not survive.

A within-heat comparison — Australian versus non-Australian surfers riding the same waves in front of the same panel under the same conditions — reduces the effect to near zero. Doubly-robust identification agrees: cross-fit targeted maximum likelihood estimation returns an average treatment effect of +0.005 with a 95% confidence interval of [−0.153, +0.163] crossing zero, and a causal forest returns −0.024 with interval [−0.565, +0.517] (`outputs/tier2_results.json`, `outputs/tier1_results.json`). A within-event permutation test (10,000 replications, shuffling the Australian-bloc label within events) puts the observed +0.616 only about 1.15 standard deviations above the permutation null: p = 0.126 (`outputs/tier5_results.json`). A wild-cluster bootstrap of the naive coefficient, clustering on event, likewise fails to reject (p = 0.50; `outputs/tier2_results.json`) — the naive standard error was understating clustered uncertainty.

The raw +0.616 is real arithmetic but is venue-localized rather than pan-Australian. A leave-one-event-out diagnostic identifies a single high-local-knowledge venue as the dominant contributor to the pooled estimate; dropping it removes most of the effect. That the residual home signal concentrates at one point-break venue with heavy accumulated local knowledge is at least as consistent with genuine performance advantage as with judging bias. What the identification battery rules out is the compatriot-judging reading of the pooled number: there is no pan-Australian home-judging effect in these data.

Consistent with Santos et al. (2025), inter-judge agreement in the corpus is near ceiling; the biases we can measure operate as small offsets on top of a panel that agrees with itself precisely, exactly the configuration the cross-sport literature warns is compatible with bias in the aggregate number.

## 5. Round-number anchoring

The one bias that survives every check is round-number anchoring, and it must be stated on the scale WSL actually uses. Individual judge scores are recorded to 0.1 precision: across all 301,478 decisions the hundredths digit is always zero, so endings of .25 and .75 never occur (`scripts/round_number_restated.py`, `outputs/round_number_restated_2026-07-25.json`). The correct null for a tenth-precision score is therefore two admissible round endings out of ten tenths — .0 and .5 — that is, 20%. (A prior framing that compared observed .0/.25/.5/.75 shares against a 4-in-20 null was on a 0.01 scale the data never uses; the headline multiple is unchanged, but the arithmetic must be stated correctly.)

On that scale, 27.8% of judge scores end in .0 and 32.1% end in .5, so 59.9% end in .0 or .5 against the 20% null — a 3.0× excess, with an exact binomial p effectively zero. The signature replicates across every disaggregation we tested: it holds for men's and women's tours, across years 2018–2026, and across judge nationality (Brazilian, Australian, American, French, Portuguese, and South African judges each show it). It also replicates on the held-out 2025 women's sample at the panel-trim-mean level (Section 7).

A companion paper (Conner 2026) reports a pre-registered test of whether time-pressure proxies explain the anchoring, on a held-out sample; the pre-registered predictions do not replicate, and the companion's conclusion is that anchoring in this corpus is not primarily a time-pressure phenomenon. The cognitive-science literature on round-number production under cognitive load is broad and among the more replicable findings in judgment and decision making (Tversky and Kahneman 1974; Pope and Simonsohn 2011; Englich, Mussweiler, and Strack 2006). The practical implication is narrow and defensible: an architectural fix — scoring on an integer scale at the input layer and dividing for display — targets the mechanism directly, whereas lengthening the deliberation window, which the companion paper finds unrelated to the anchoring, would not be expected to help.

## 6. Descriptive: Brazilian-judge representation on panels, 2018–2026

We report a descriptive trend and, deliberately, no causal claim. Table 1 gives, per year, the mean number of Brazilian-passport judges seated on panels scoring Brazilian surfers and — the crucial comparison — on all panels (`scripts/panel_composition_descriptive.py`, `outputs/panel_composition_descriptive_2026-07-25.json`). Both series are on the imputed-nationality 2018-plus subset described in Section 2; the "all panels" series covers all waves whose surfer nationality could be imputed.

**Table 1.** Mean Brazilian-judge count on panels, by year (wave-level; each row is one scored wave).

| Year | BRA-surfer panels | n | All panels | n |
|---|---|---|---|---|
| 2018 | 1.711 | 1,788 | 1.601 | 6,375 |
| 2019 | 1.545 | 2,302 | 1.528 | 8,171 |
| 2021 | 1.365 | 230 | 1.146 | 1,041 |
| 2022 | 1.567 | 2,019 | 1.542 | 5,889 |
| 2023 | 1.568 | 1,567 | 1.544 | 4,874 |
| 2024 | 0.999 | 1,121 | 0.992 | 4,445 |
| 2025 | 0.899 | 1,202 | 0.886 | 4,486 |
| 2026 (through April) | 0.841 | 673 | 0.756 | 1,352 |

(2020 has no full Championship Tour season and does not appear.)

The Brazilian-surfer series falls from 1.71 in 2018 to 0.84 in 2026. But the all-panels series falls almost identically, from 1.60 to 0.76. The two decline in lockstep. That is the decisive fact for interpretation: Brazilian judges became less common on Championship Tour panels generally, not specifically on the panels scoring Brazilian surfers. A story about assignment policy — panels being composed to avoid Brazilian judge/Brazilian surfer concentration — and a story about supply — fewer Brazilian judges on the roster through retirement and churn — produce the same pattern in these data. Without judge-identity data (which judges, appearing when) we cannot distinguish them, and we do not try to.

For completeness we report an exploratory event-clustered bootstrap of the year slope on the Brazilian-surfer series: resampling whole events with replacement (90 events, 2,000 replications) gives a slope of −0.095 Brazilian judges per year with a 95% interval of [−0.120, −0.064]. We label this exploratory and descriptive. It confirms only that the downward year trend is not an artifact of a single event's sampling; it is not a policy test, and it inherits the supply-versus-assignment ambiguity above. The one institutional event in the window — Luiz "Luli" Pereira succeeding Pritamo Ahrendt as WSL head judge in October 2023 — is noted here as a coinciding date and nothing more; we make no claim that it caused the trend.

## 7. Hold-out replication on the 2025 women's tour

The 2025 women's Championship Tour (1,815 panel-trim-mean rows) was reserved as a temporal-split hold-out and opened only for the replication reported here (`outputs/tier5_results.json`). We test three findings established on the training data.

The within-heat rank-prior coefficient, estimated on training data at β = −0.013 per rank position, replicates on the hold-out at β = −0.034 (p = 7.6 × 10⁻⁴, n = 1,386): same direction, larger magnitude. The trim-mean round-number rate, 22.7% on training data, replicates at 25.2%. The Australian home-event coefficient replicates at the women-only descriptive level at +0.475 (p = 0.012, 328 matched waves) — the descriptive signal is real and reproduces, even though its causal interpretation collapses under the identification battery in Section 4; both readings hold at once.

One limitation of this design: the hold-out is a temporal split set aside from the training period, but it was not git-sealed at a commit predating the training analyses. The file was not opened during discovery and was not used in any training-period computation, but a pre-sealed design would be a stronger commitment than analytic isolation, and we do not overstate it.

## 8. Discussion

The through-line of this paper is that the biases most often alleged against WSL judging are, under careful identification, either absent or small. The compatriot mechanism — the intuitive charge that judges favor their countrymen — does not operate at detectable amplitude when the test is run at the only resolution that isolates it: within the same panel, on the same wave. Brazilian judges, if anything, score Brazilian surfers a hair lower than their panel-mates; the Australian compatriot premium is a tenth of a point with an interval through zero; and the two named surfers most associated with home-cooking complaints show no compatriot gap at their home venue. The most-cited home-advantage number in the sport, +0.616, is an artifact of pooling and venue mix that disappears the moment one compares surfers within the same heat and does not survive doubly-robust identification. Inter-judge agreement is near ceiling. This is not the profile of a captured judging system.

The one durable bias is mechanical rather than motivational: round numbers. Judges anchor to .0 and .5 at three times chance, everywhere, on every disaggregation and on held-out data. That is a cognitive regularity, not a partiality, and it has a clean architectural fix — score on an integer scale and divide for display. It is the single reform this analysis actually supports.

The descriptive panel-composition trend deserves a word precisely because it is the finding most easily over-read. Brazilian-judge representation on Championship Tour panels roughly halved between 2018 and 2026. It would be tempting to narrate that as a quiet reform. The data do not license the narrative: Brazilian judges thinned on all panels together, so the number cannot tell us whether assignment policy changed or the roster simply turned over. We report the decline and stop there. The right posture toward it — and toward the whole corpus — is that the biases which can be measured are small and the one that is large is fixable, which is a more useful message to a governing body than a bias indictment would be.

The reform most supported by the cross-sport literature is orthogonal to any of our specific findings: publishing per-judge scores with name attribution, on the template Zitzewitz (2014) documents for figure skating. The WSL already collects per-judge data internally; releasing it with a short lag would let exactly the analyses in this paper be run continuously and independently, and would let questions the present data cannot answer — including the supply-versus-assignment question in Section 6 — be settled directly.

## 9. Limitations

The corpus's coverage is windowed and its nationality fields do not overlap cleanly. Judge nationality exists only from 2018; surfer nationality in the per-judge file exists only before 2018 and is imputed for later years from a 110-surfer name map that fills roughly two-thirds of 2018-plus rows. Every analysis requiring both fields is thus a 2018–2026 analysis on an imputed subset, and statements about temporal robustness are bounded accordingly. The pre-2018 per-judge layer, though large, does not contribute to any nationality-dependent result.

The compatriot counterfactual rules out the within-panel padding mechanism but not between-panel assignment mechanisms; the data cannot test whether compatriot judges are systematically placed on easier-to-score conditions. The Australian home-event effect is descriptively real and replicable on women-only data even as its causal interpretation collapses; we retain the descriptive number and decline the causal reading. The panel-composition trend in Section 6 cannot separate judge supply from assignment policy, and its exploratory year-slope bootstrap is descriptive only.

The hold-out in Section 7 is a temporal split that was analytically isolated during discovery but not pre-sealed at an earlier commit. A video-computer-vision objective-features check that an earlier version of this work proposed as an external accuracy benchmark is not part of this submission: a 22-wave pilot returned negative leave-one-out R² with severe overfit and is inconclusive.

Two peer-reviewed WSL studies (Santos et al. 2025; Naumann and Rösch 2026) cover overlapping but smaller corpora. We replicate Santos's near-ceiling reliability finding. We partially confirm Naumann and Rösch's home-advantage direction on a per-judge difference-in-differences specification with a confidence interval that crosses zero; the values read from Naumann and Rösch are those in the published version. Neither prior study analyzed the women's tour or extended into the post-2022 window.

---

## Data and code availability

All data and code are available at https://github.com/addie-conner/wsl-judging-bias-2026. The archive contains the per-judge corpus (`data/judges.parquet`, 301,478 individual judge-score decisions across 60,834 scored waves), the panel-level analysis set (`data/heats.parquet`, 24,901 rows, 2022–2025), the held-out 2025 women's-tour file with a documented manifest (`data/HOLDOUT_MANIFEST.json`), and, for each result reported above, the script in `scripts/` that produces it and the result file in `outputs/`. The three analyses new to this version — the panel-composition description (Section 6), the named-individual counterfactual (Section 3), and the restated round-number signature (Section 5) — are produced by `scripts/panel_composition_descriptive.py`, `scripts/named_individual_counterfactual.py`, and `scripts/round_number_restated.py`, writing dated JSON outputs. Per-judge scoring data was assembled from publicly accessible sources only: a public, unauthenticated score-detail endpoint on worldsurfleague.com, Common Crawl WARC archives, and Wayback Machine snapshots. No proprietary or authenticated WSL data was used.

## References

Boen, F., van Hoye, K., Vanden Auweele, Y., Feys, J., & Smits, T. (2008). Open feedback in gymnastic judging causes conformity bias based on informational influencing. *Journal of Sports Sciences*, *26*(6), 621–628. https://doi.org/10.1080/02640410701670393

Callaway, B., & Sant'Anna, P. H. C. (2021). Difference-in-differences with multiple time periods. *Journal of Econometrics*, *225*(2), 200–230. https://doi.org/10.1016/j.jeconom.2020.12.001

Cameron, A. C., Gelbach, J. B., & Miller, D. L. (2008). Bootstrap-based improvements for inference with clustered errors. *The Review of Economics and Statistics*, *90*(3), 414–427. https://doi.org/10.1162/rest.90.3.414

Conner, A. (2026). *Time Pressure Does Not Explain Round-Number Anchoring in Professional Surf Judging: A Pre-Registered Mechanism Test.* Companion paper, this archive.

Englich, B., Mussweiler, T., & Strack, F. (2006). Playing dice with criminal sentences: The influence of irrelevant anchors on experts' judicial decision making. *Personality and Social Psychology Bulletin*, *32*(2), 188–200. https://doi.org/10.1177/0146167205282152

Findlay, L. C., & Ste-Marie, D. M. (2004). A reputation bias in figure skating judging. *Journal of Sport and Exercise Psychology*, *26*(1), 154–166. https://doi.org/10.1123/jsep.26.1.154

Heiniger, S., & Mercier, H. (2021). Judging the judges: Evaluating the accuracy and national bias of international gymnastics judges. *Journal of Quantitative Analysis in Sports*, *17*(4), 289–305. https://doi.org/10.1515/jqas-2019-0113

Koo, T. K., & Li, M. Y. (2016). A guideline of selecting and reporting intraclass correlation coefficients for reliability research. *Journal of Chiropractic Medicine*, *15*(2), 155–163. https://doi.org/10.1016/j.jcm.2016.02.012

Krumer, A., Otto, F., & Pawlowski, T. (2022). Nationalistic bias among international experts: Evidence from professional ski jumping. *Scandinavian Journal of Economics*, *124*(1), 278–300. https://doi.org/10.1111/sjoe.12451

McLaren, R. H. (2022). *Independent investigation: AIBA scoring and refereeing in Olympic boxing.* McLaren Global Sport Solutions.

Naumann, D. L., & Rösch, J. (2026). Home advantage in professional surfing: Are local surfers better? Are local judges more challenging? *International Journal of Sport Finance*, *21*(1), 21–37. https://doi.org/10.1177/15586235251403230

Pope, D., & Simonsohn, U. (2011). Round numbers as goals: Evidence from baseball, SAT takers, and the lab. *Psychological Science*, *22*(1), 71–79. https://doi.org/10.1177/0956797610391098

Santos, T. M., Rodrigues Santos, L. E., Vinicius, Í., Brietzke, C., Pereira, L. C., Melo, P. H., Moura, T. C. B., De Negri, T., Elsangedy, H. M., & Pires, F. O. (2025). Intrinsic judgment error in men's championship World Surf League: WSL 2021. *Retos*, *64*, 311–321. https://doi.org/10.47197/retos.v64.106821

Tversky, A., & Kahneman, D. (1974). Judgment under uncertainty: Heuristics and biases. *Science*, *185*(4157), 1124–1131. https://doi.org/10.1126/science.185.4157.1124

Wolframm, I. (2023). Let them be the judge of that: Bias cascade in elite dressage judging. *Animals*, *13*(17), 2797. https://doi.org/10.3390/ani13172797

Zitzewitz, E. (2006). Nationalism in winter sports judging and its lessons for organizational decision making. *Journal of Economics & Management Strategy*, *15*(1), 67–99. https://doi.org/10.1111/j.1530-9134.2006.00092.x

Zitzewitz, E. (2014). Does transparency reduce favoritism and corruption? Evidence from the reform of figure skating judging. *Journal of Sports Economics*, *15*(1), 3–30. https://doi.org/10.1177/1527002512441479
