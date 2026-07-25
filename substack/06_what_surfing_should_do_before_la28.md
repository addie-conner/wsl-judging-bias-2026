> **SUBSTACK PASTE GUIDE** (delete this entire block when you're done)
>
> 1. Substack > New Post
> 2. **Title field:** What Surfing Should Do Before LA28
> 3. **Subtitle field:** Three reforms we know work, one reform that has never been tried, and what the data forecasts will happen at the next Olympic surfing event if nothing changes
> 4. **Body field:** paste everything below the horizontal rule
> 5. Once pasted, delete the H1 (`# Title`) and H2 (`## Subtitle`) at the top of the body — Substack will use the Title/Subtitle fields you set above
> 6. Section breaks (`---`) and headings (`##`, `###`) render natively. Bold (`**`) and italic (`*`) render natively.

---

# What Surfing Should Do Before LA28

## Three reforms we know work, one reform that has never been tried, and what the data forecasts will happen at the next Olympic surfing event if nothing changes

_A note on athlete naming before we start: this piece names specific surfers in the context of structural model-risk forecasts derived from public WSL Championship Tour scoring data. The forecasts are not predictions about how individual athletes will perform; they are predictions about how the unreformed judging architecture will treat surfer profiles of various kinds. Per-surfer model-risk rankings are deliberately moved to a sealed appendix at `outputs/olympic_2028_la_predictions_locked.json` for that reason. The body of this piece names individuals only in pairing-level scenarios, which are about heat structure rather than athlete character._

---

Surfing returns to the Olympics in summer 2028 at Lower Trestles in San Clemente, California. Predictable waves. American venue. A host-nation contingent on the start list that is likely to be deep, though final qualification hasn't locked yet. The 2028 event will be the first major-stakes international surf competition since Paris 2024, and the first held on what is unambiguously American home soil.

This is, on every dimension the data tracks, a higher-stakes test than Paris was. Paris was held on French Polynesian water with an ISA panel and minimal home-crowd presence, and even Paris reproduced four out of the five WSL bias mechanisms we measured. Trestles won't have those mitigating factors. The crowd will be partisan. The venue rewards local knowledge that the host-country surfers grew up with and that visitors will see for a week before competition starts.

A note on the judges: the ISA judging pool that operates the Olympic surfing event is, as a matter of public record, distinct from the WSL Championship Tour pool, but the two have meaningful overlap — several individual judges have served on both. The bias mechanisms we have measured on WSL data may transfer in part or in whole to the ISA panel; whether they do is itself an empirical question that LA28 will help answer. The forecasts below assume material transfer; if ISA's pool turns out to be substantively different, the forecasts will be falsified in a different and equally informative way.

The question is what to do about it. The answer, to the surprise of nobody who has read the cross-sport literature, is not complicated. There are three reforms with documented bias-reduction effects in other subjective sports, plus one reform that has never been tried but is approximately free to implement.

ISA could deploy all four before the 2028 surfing event. Whether they will is a different question. We are going to make a forecast about what happens if they don't.

---

## The forecast (SHA-locked, May 2026)

Before the 2028 surfing event happens, we've registered a set of specific, falsifiable predictions about what the LA28 final will look like under unreformed judging. The predictions are time-stamped and locked to a public commit so they can't be retroactively edited. They'll resolve when the Olympic event happens.

Round-number share at LA28: about **26 percent** of trim-mean wave scores will end on .0 or .5 — the same headline metric we measured on the regular tour, where the WSL ran around 23 percent. Round-number anchoring is a property of how humans count under time pressure, so we don't expect the Olympic stage to break the pattern.

USA wave-score uplift at LA28 — the simplest test of "are American surfers being given a boost on home water?" — predicts a small positive number, around a sixth of a point, with a confidence interval that runs from slightly negative to about half a point. The interval is wide because three different ways of computing the prediction disagree with each other. Trestles-only WSL data says the boost should be larger; the broader USA-CT data says it should be roughly zero; the Paris 2024 Olympic comparison says it should be slightly negative. Honest range, not a confident point estimate.

Day-of-event amplification — scores tending to drift higher as the event progresses — predicts about a sixth of a point per day. Smaller than the regular tour, but not zero.

Most-likely-controversial pairings, conditional on draw — these are scenario examples based on currently modeled seed assumptions, not claims about the final LA28 qualification list (top 3 if drawn): Seth Moniz (USA, projected seed 19) vs Italo Ferreira (BRA, projected seed 2); Imaikalani deVault (USA, projected seed 18) vs Italo Ferreira; Seth Moniz vs Jack Robinson (AUS, projected seed 4). Each pairing combines a USA-vs-foreign matchup with a substantial seeding gap that makes a close result statistically unlikely without a bias channel.

Per-surfer model-risk exposure rankings — the surfers most exposed to *adverse* model-risk under the unreformed regime, and the surfers most exposed to *favorable* model-risk — are SHA-locked in the sealed appendix `outputs/olympic_2028_la_predictions_locked.json`. The per-surfer rankings are deliberately not published in the body of this piece. The reasoning is straightforward: individual athletes will read the predictions before competing in their Olympic event, and the reputational asymmetry of pre-publication is unfavorable. The sealed structure preserves the falsification design — the predictions are committed, the resolution is binding — while limiting the pre-event reputational footprint to what the methodology requires.

These are pre-event predictions. They resolve at the 2028 final. If reforms 1–3 (below) are implemented before LA28, the unreformed-baseline predictions become reform tests rather than baseline forecasts; the expected direction is clear (compatriot-panel exposure should fall, round-number clustering should drop, day-of-event amplification should weaken), and the magnitude of expected reduction — based on the figure-skating IJS post-reform window measured by Zitzewitz (2014) and the gymnastics post-Athens window measured by Heiniger and Mercier (2018, 2021) — runs roughly a third to a half on the cleanest categories. If nothing changes, the predictions resolve against the unreformed baseline. The data will tell us which.

---

## Reform 1: Public per-judge data with 30-day lag

This is the reform that has the strongest empirical track record and the cheapest implementation. ISA — like the WSL — already collects per-judge scoring data on a tablet at every wave. They simply do not release it. After each event, they publish only the panel trim-mean.

What the cross-sport literature, specifically Eric Zitzewitz's 2014 paper on figure skating, found is that releasing the per-judge data publicly, with a thirty-day lag, with judge names attached, **reduced figure-skating compatriot bias by approximately 50 percent** in the seasons after publication began. The mechanism is not coercive. It is informational. When a judge's individual scores are public, repeated identifiable bias becomes career-costly to that judge — the visibility creates reputational discipline that did not exist when the bias could only be inferred from aggregate trim-mean.

Gymnastics moved to per-judge transparency after Athens 2004. Diving went transparent in the early 2010s. Boxing has been moving in the same direction since the McLaren report on AIBA in 2022. Every subjective sport that has implemented this reform has measured bias reductions on the order of 30 to 50 percent, sustained across subsequent seasons.

Surfing has not. Pro surfing is now the largest subjective-sport field that maintains panel-only opacity. ISA could change this for the 2027 World Surfing Games as a pilot, with full implementation by LA28. Implementation cost is operational — a CSV release per event. There is no methodological barrier. There is no precedent for negative consequences. There is two decades of cross-sport precedent for positive consequences.

The single highest-leverage reform on the table, by every available empirical benchmark, is per-judge transparency. It is also the reform ISA can do tomorrow.

## Reform 2: Integer-scale scoring (kills round-number anchoring)

The round-number clustering signature in WSL judging — 60 percent of individual judge-scores ending in .0/.25/.5/.75 against a 4-percent random baseline — is the most-replicable, most-bulletproof, most-survives-every-correction finding in our entire 17-year corpus. It is also a property of how humans count under time pressure, not a property of WSL judges specifically. Olympic divers exhibit it. Gymnastics judges exhibit it. Real-estate listings exhibit it. Tip jars exhibit it.

You can fix it without fixing the judges. You change the scale.

The simplest version: judges score from 0 to 100 in unit increments, and the system divides by 10 for display. The judge's internal counting palette no longer has any reason to cluster on .25 or .5 — those values do not exist on the input scale. The displayed score still ranges 0.0 to 10.0 in 0.1 increments, indistinguishable to fans. The bias is removed at the input layer.

Alternative version: rotate the displayed increment by 0.01 each wave. The judge's mental palette has no fixed anchor to cluster on, because what counts as "round" changes wave to wave. Same effect.

A natural alternative reform — and one we want to rule out before recommending the architectural fix — is operational rather than architectural: extend the deliberation window. Give judges ninety seconds instead of thirty to submit a score, rotate panels mid-heat to fight fatigue, slow the wave queue. We tested it. Anchoring is detectably time-pressure-sensitive in the corpus, but the effect is small. Extending the typical wave-to-wave gap from twenty-four seconds to seven minutes — Q1 to Q4 of the wave-density distribution — moves the anchoring rate by about two percentage points on a thirty-one-percent baseline. Judge-fatigue across a long competition day moves it by a similar amount. You cannot run the clock long enough to fix this at the operational layer. The fix has to be at the input layer.

Olympic gymnastics implemented an analogous scale-redesign in the 2008 Code of Points, moving from a 10-point holistic scale to a constructed-from-categories deduction system. Round-number clustering at the final-score level dropped from textbook-significant to negligible within a single Olympic cycle.

Implementation cost for surfing: a software update to the scoring tablet, one event-day of testing, written documentation for the judge handbook. We are talking weeks of operational work, not months.

## Reform 3: Panel-rotation accountability rule

The WSL appears to have implemented this informally between October 2023 and the present. The data shows it: the average count of Brazilian judges on Brazilian-surfer panels fell from 1.72 in 2018 to 0.84 in 2026, with a slope no random shuffle of the year labels reproduces in 1,000 attempts. Whatever Luiz "Luli" Pereira did when he took over as head judge in 2023, it dramatically reduced compatriot panel-stacking.

ISA could codify this directly for LA28. The rule is: no judge scores a heat that contains a compatriot surfer. Gymnastics has had a version of this rule since 2008. Figure skating has a softer version (compatriot judges' scores can be discounted from trim-mean computation). Boxing's post-McLaren reforms moved toward something similar. It is not a controversial reform. It is the most operationally unambiguous of the three.

Predicted bias reduction: the panel-composition compatriot mechanism is mechanically eliminated. The behavioral compatriot mechanism (per-judge difference-in-differences from compatriot judges) plausibly also drops, though that depends on how individual judges respond to the new rule.

Implementation cost: ISA panel-assignment policy update. Operational.

## Reform 4: Pre-registered, Brier-scored, public prospective predictions

This reform has never been tried in any subjective sport. It is the one we are using to write this article.

Here is what it looks like in practice. Before each event, independent research groups register specific, falsifiable, quantitative predictions about what the bias signatures will look like at that event — for example, *the round-number share at LA28 will land between 20% and 31%*. Each prediction is committed to a public, time-stamped ledger so it cannot be retroactively edited. Each prediction has a pre-specified rule for whether it counted as right or wrong. After the event, the predictions are scored on accuracy using a standard forecasting metric called the Brier score (zero for perfect, one for systematically wrong; lower is better, the way golf works).

We have registered 49 such predictions for the 2026 WSL Championship Tour and the 2028 Olympic surfing event. They are public. They will resolve. The Brier scores will tell us, prospectively, how well the analysis in this paper transfers to events that have not happened yet. The pre-registration commit and the locked prediction file are addressable at git SHA `1ee95a5e4ccb` against heats SHA `7f07fb121abe`; the LA28 forecast specifically is in `outputs/olympic_2028_la_predictions.md` and `outputs/olympic_2028_la_predictions_locked.json` in the public replication archive. The infrastructure is platform-agnostic — other independent research groups should register their own predictions on their own infrastructure; the registration discipline is what matters, not which specific platform implements it.

The function of public Brier scoring in a subjective sport is the same as the function of public per-judge data: reputational discipline through information disclosure. The difference is that Brier scoring disciplines the *analysts* rather than the *judges*. It prevents a research community from quietly walking away from predictions that don't pan out, or from selectively emphasizing the predictions that do. It creates a pile of forecasting accuracy data that accumulates across events and that any subsequent reform debate can cite.

Implementation cost is close to zero. The infrastructure is already public. ISA needs only to acknowledge that it exists and invite independent groups to register predictions for ISA-sanctioned events.

---

## What ISA needs to do, and on what timeline

If ISA wants reforms 1–3 in place before LA28, with enough lead time for the bias-reduction effects to compound and for measurement to be possible, the timeline looks like this:

- **Q4 2026 (now):** ISA committee adopts panel-rotation rule (Reform 3) for the 2027 World Surfing Games.
- **Q1 2027:** Software update for integer-scale scoring (Reform 2). Pilot at WSG 2027.
- **Q2 2027:** Public per-judge data release pilot (Reform 1). One event.
- **Q3 2027:** Publish initial results from the pilot. Refine before LA28.
- **Q4 2027:** Full implementation across all ISA-sanctioned events.
- **Summer 2028:** LA28 surfing event judged under the four-reform regime.

If ISA implements all four, the SHA-locked predictions in this article become *test cases for the reforms*. The compatriot mechanism should drop to mechanical zero. The round-number share should drop from a predicted 25.5 percent to somewhere around 12 to 15 percent. Per-judge transparency should reduce day-of-event amplification by half or more. Public Brier scoring should reveal the magnitude of each individual reform.

If ISA does nothing, the SHA-locked predictions resolve against the unreformed baseline, and the cross-sport literature receives a fresh, well-measured data point on the cost of inaction at a subjective-sport governing body.

Either way, we will know.

---

There is a version of this story that ends with reform. Figure skating got reform after Salt Lake City. Gymnastics got reform after Athens. Boxing has been getting reform, slowly, since 2022. In each case, the reform came after a public scandal — a moment when the ordinary everyday biases that subjective sports always have became suddenly visible enough that the governing body could not credibly continue pretending they didn't exist.

Surfing hasn't had its scandal. There's no Salt Lake City moment lurking. What it has instead is a pile of accumulated empirical evidence pointing out that the same biases which triggered reform in other sports are present in surfing too, on the largest dataset ever assembled. The reforms have a track record. The implementation cost is rounding error against the WSL's broadcast revenue. The Olympic event is twenty-four months out.

What ISA does between now and Lower Trestles will tell us whether subjective-sport governing bodies need scandals to reform, or whether they can do it on the data alone.

Either way, we'll know.

---

*This is the sixth and final piece in a series re-analyzing WSL judging on the largest dataset assembled to date. The full academic version is forthcoming on SportRxiv. The data, the analyses, the SHA-locked pre-registration, and the 49 prospective predictions are publicly available — including the LA 2028 forecast registered May 4, 2026, against git SHA `1ee95a5e4ccb`. They will resolve at the Olympic surfing final in summer 2028.*
