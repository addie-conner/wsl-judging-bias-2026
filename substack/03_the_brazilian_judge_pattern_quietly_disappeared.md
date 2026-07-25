> **SUBSTACK PASTE GUIDE** (delete this entire block when you're done)
>
> 1. Substack > New Post
> 2. **Title field:** The Brazilian-Judge Pattern Quietly Disappeared
> 3. **Subtitle field:** How a head-judge transition reshaped the most-complained-about pattern in pro surfing — and what the data does and doesn't say about why
> 4. **Body field:** paste everything below the horizontal rule
> 5. Once pasted, delete the H1 (`# Title`) and H2 (`## Subtitle`) at the top of the body — Substack will use the Title/Subtitle fields you set above
> 6. Section breaks (`---`) and headings (`##`, `###`) render natively. Bold (`**`) and italic (`*`) render natively.

---

# The Brazilian-Judge Pattern Quietly Disappeared

## How a head-judge transition reshaped the most-complained-about pattern in pro surfing — and what the data does and doesn't say about why

If you watch the WSL with anyone, you have already had this argument. It is the loudest argument in professional surfing, and it has been for most of the last decade. The argument is about a number.

Two.

Every time a Brazilian surfer paddled out for a Championship Tour heat, you could count on roughly two Brazilian judges in the tower scoring them. Five judges per panel. Two of his or her countrymen, on average. The stat moved through comments sections and Slack threads as half-vibe, half-evidence. Brazilian surfer, two Brazilian judges, round it off.

On October 11, 2023, the WSL announced that Pritamo Ahrendt was stepping down after fifteen years as head judge, succeeded by Luiz "Luli" Pereira. Most fans filed it under personnel news.

What happened over the next three years is the most striking shift in modern professional surf judging data. I pulled the panel numbers myself, and the fans hadn't been wrong about the baseline.

*(Correction, July 2026: an earlier version of this piece misnamed the incoming head judge, and attributed the panel shift below to a deliberate assignment policy. The updated analysis is more careful: the data cannot separate an assignment policy from a change in the judge roster itself, so this piece now presents the shift as a documented pattern with an open cause.)*

In 2018, the average Brazilian surfer competing on the Championship Tour faced a panel that contained, on average, **1.72 Brazilian judges**. Five judges per panel. Nearly two of them, on average, would be his or her countrymen. That is — and there's no nice way to say this — a structurally noisy situation. It might or might not produce bias. But it was definitely not what the WSL would have wanted on a slide deck about objective judging.

Then 2024 happened.

The 2024 average dropped to **0.999**. About one Brazilian judge per Brazilian surfer's panel.

In 2025: **0.898**.

In 2026, current data through April: **0.841**.

The mean Brazilian-judge count on Brazilian-surfer panels has fallen by half in three years.

---

When you spot a trend like this, the next question is whether you're looking at something real or just at noise. So ask the data directly: in a world where nothing had changed, how often would a slope this steep show up by accident?

So we shuffled. We took the same dataset, randomly reassigned which year each panel-composition number belonged to, and recomputed the trend. Then we did it again. A thousand times. If the real slope was somewhere inside the cloud of shuffled slopes, the trend was probably random year-to-year drift. If it was outside the cloud, something had actually moved the panels.

The real slope was outside the cloud. The decline is not year-to-year noise; something in the composition of panels genuinely changed around 2024.

Then we widened the lens, and the story got more complicated: the count of Brazilian judges fell on *all* panels — not just the panels scoring Brazilian surfers — and the two series fell in lockstep. That means the data cannot distinguish between two very different stories: a deliberate assignment change that rotates Brazilian judges away from Brazilian surfers, or simply fewer Brazilian judges on the working roster — retirements, churn, hiring. Separating those would take judge-identity records the public data doesn't carry. The pattern is real and sharp. Its cause is an open question.

---

Here's where the story takes a turn.

The natural follow-up question is whether the Brazilian judges who *remain* on panels favor Brazilian surfers when they score them — whether, on the wave-by-wave level, the bias everyone assumes is actually present in the per-judge data.

This is a different test from the panel-composition trend. The panel-composition trend asks how many Brazilian judges are in the room when a Brazilian surfer surfs. The behavioral test asks whether, given that a Brazilian judge is in the room, that judge gives the Brazilian surfer a higher score than a non-Brazilian judge sitting next to them gives the same Brazilian surfer.

We have the data to run it. At Brazilian Championship Tour events — Saquarema, Praia da Macumba, the Oi Rio Pros — our seventeen-year per-judge dataset contains about eleven thousand individual scoring decisions where we know both the surfer's nationality and the judge's nationality. We can split by period, run the test in each, and see what shows up.

The clean version of the test goes like this. Take Brazilian judges scoring Brazilian surfers. Subtract Brazilian judges scoring non-Brazilian surfers. That's the Brazilian-judge "lift" for compatriots. If the lift is positive, Brazilian judges are favoring their own. Then, as a sanity check, do the same comparison for non-Brazilian judges. The difference between the two lifts is the cleanest available measure of the compatriot effect.

Pre-reform period (2009 through 2022): the compatriot lift is **negative 0.10 points**. Mildly negative. Brazilian judges weren't padding Brazilian surfers' scores; they were giving them slightly *less* of a bump than the rest of the panel.

Post-reform period (2024 through 2026): same test, same direction. The lift is **negative 0.13 points**. Still mildly negative, slightly more so.

Across the entire seventeen-year stretch, the per-judge lift averages out to a slight negative. In no period does the test show the positive compatriot bonus that the fan complaints describe.

The compatriot bonus that everyone yells about shows up in panel-level ordinary least squares regressions. It is the kind of estimate that pools across heats, controls for surfer skill and event, and asks whether the presence of any compatriot judge on the panel is associated with a higher trim-mean score. That estimate is positive in our data. It is positive in the published cross-sport literature. It is the source of the IJSF (2025) WSL compatriot estimate of plus-0.04 to plus-0.32 points.

It is also, when you run the more careful identification — the difference-in-differences at individual judge × individual surfer cells, which controls by construction for the venue, the wave conditions, the surfer selection, the panel composition, and the calibration drift that the OLS estimate is mixing together — the estimate that reverses to mildly negative.

Panel composition changed. That part is real and replicable, whatever caused it. The number of times two Brazilian judges sit in the same room watching a Brazilian surfer surf has fallen by half — which, on its own, dissolves the thing fans complain about and removes a class of correlation the panel-level literature has been treating as evidence of bias.

What the shift did not need to change — because there is no clean evidence it was ever there — is the per-judge behavioral compatriot bonus. That estimate has been mildly negative in every sub-period of our 17-year corpus. The data is consistent with two stories at once. Story one: Brazilian judges have always been slightly stricter on Brazilian surfers, perhaps to overcompensate for the suspicion of compatriot bias. Story two: the panel-level OLS estimate the cross-sport literature reports has been measuring something other than per-judge compatriot bias all along — venue effects, selection patterns, calibration drift. Both stories are consistent with the same data.

---

The clean way to read this is that the loudest complaint in professional surfing — Brazilian judges stacked on Brazilian-surfer panels — described a real pattern, and that pattern has now largely dissolved in the data, whether by policy or by roster change. The fan-side narrative receded because the panel composition that produced the *appearance* of the bias became less common.

What the per-judge data adds is the more surprising half: there is no clean evidence the behavioral bias was ever there. Brazilian judges have scored Brazilian surfers slightly *below* what their non-Brazilian colleagues gave the same surfers, in every period we can measure. The composition shift resolved an optics problem. The scoring decisions underneath look clean in both eras.

The one structural gap worth naming is transparency: because the WSL publishes only panel averages, questions like this one can only be answered by outside reconstruction of per-judge data. Publishing per-judge scores — the reform every other subjective sport eventually adopted — would let the league answer its loudest critics with its own records.

---

Surfing is a strange sport to study. It pretends to be a competition decided by waves and athletic execution. It is in fact a competition decided by five people sitting in a tower with tablets, deciding what they just saw. The five-person panel is the entire mechanism. Move the panel and you move the sport.

The WSL appears to have understood this and acted on it. They did not announce that they were acting on it. The data shows them acting on it.

That is — somehow, against the grain of how subjective sports usually behave — accountability.

You just have to read the data to see it.

---

*This is the third piece in a six-part series re-analyzing WSL judging. The next piece takes on the methodological keystone of the series: how high inter-judge agreement and unbiased judging are different properties of judging panels, and why the most-cited statistic in defense of WSL judging — that judges agree 97 percent of the time — answers only half the fairness question.*
