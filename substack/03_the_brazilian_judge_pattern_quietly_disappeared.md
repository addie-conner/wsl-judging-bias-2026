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

_A note on framing before we start: this piece is about a structural pattern in panel composition, not about individual judges. Subjective-sport judging systems produce measurable, identity-correlated patterns unless transparency and panel design actively counteract them. That is the universal claim of the cross-sport literature. Specific judges are not the subject._

---

If you watch the WSL with anyone, you have already had this argument. It is the loudest argument in professional surfing, and it has been for most of the last decade. The argument is about a number.

Two.

Every time a Brazilian surfer paddled out for a Championship Tour heat, you could count on roughly two Brazilian judges in the tower scoring them. Five judges per panel. Two of his or her countrymen, on average. The stat moved through comments sections and Slack threads as half-vibe, half-evidence. Brazilian surfer, two Brazilian judges, round it off.

Then on October 11, 2023, the WSL announced that Pritamo Ahrendt was stepping down after fifteen years as head judge. His replacement was Luiz "Luli" Pereira. Brazilian. Ex-CT competitor, longtime panelist. The announcement landed in the back half of a press release about the upcoming Pipeline event. Most fans never read it. The few who did filed it under personnel news.

What happened over the next three years is the most consequential reform in modern professional surf judging. The WSL never said a word about it being a reform.

I pulled the panel data myself. The fans hadn't been wrong about the number.

In 2018, the average Brazilian surfer competing on the Championship Tour faced a panel that contained, on average, **1.72 Brazilian judges**. Five judges per panel. Nearly two of them, on average, would be his or her countrymen. That is — and there's no nice way to say this — a structurally noisy situation. It might or might not produce bias. But it was definitely not what the WSL would have wanted on a slide deck about objective judging.

Then 2024 happened.

The 2024 average dropped to **0.999**. About one Brazilian judge per Brazilian surfer's panel.

In 2025: **0.898**.

In 2026, current data through April: **0.841**.

The mean Brazilian-judge count on Brazilian-surfer panels has fallen by half in three years.

---

When you spot a trend like this, the next question is whether you're looking at something real or just at noise. The honest way to answer is to ask the data the question directly: in a world where nothing had changed, how often would a slope this steep show up by accident?

So we shuffled. We took the same dataset, randomly reassigned which year each panel-composition number belonged to, and recomputed the trend. Then we did it again. A thousand times. If the real slope was somewhere inside the cloud of shuffled slopes, the trend was probably random year-to-year drift. If it was outside the cloud, something had actually moved the panels.

The real slope was outside the cloud. Every single time. None of the thousand random shuffles produced a downward trend anywhere near this steep.

The cleanest interpretation is that panel-assignment policy changed. Not random year-to-year drift. Not coincidence. Something operational, something deliberate, that we can't prove from the panel data alone but that the panel data is very hard to reconcile with anything else.

For sanity, we ran one more test. Take the four other countries with substantial Championship Tour presence — Australia, the United States, France, South Africa — and ask: if Brazil's panel composition had drifted the way these comparable countries did, what should the Brazilian count have been in 2024, 2025, 2026? Imagine a fake "Brazil" built out of those four real countries' panel-composition trends, blended together. Where does fake-Brazil land?

Fake-Brazil stays almost flat. Around 1.4 to 1.5 Brazilian judges per panel, year over year — basically the pre-reform baseline.

Real Brazil drops to 0.84. The gap between real Brazil and fake-Brazil widens every year. By 2026, real Brazil has about 0.9 fewer Brazilian judges per panel than the comparable-country trends would have predicted.

This is the kind of effect economists publish papers about when they spot it in government policy data. We caught it inside the WSL's own panel-assignment ledger.

---

Here's where the story takes a turn.

The natural follow-up question is whether the Brazilian judges who *remain* on panels still favor Brazilian surfers when they score them — whether, on the wave-by-wave level, the bias the panel-rotation reform was supposed to address is actually present in the per-judge data.

This is a different test from the panel-composition trend. The panel-composition trend asks how many Brazilian judges are in the room when a Brazilian surfer surfs. The behavioral test asks whether, given that a Brazilian judge is in the room, that judge gives the Brazilian surfer a higher score than a non-Brazilian judge sitting next to them gives the same Brazilian surfer.

We have the data to run it. At Brazilian Championship Tour events — Saquarema, Praia da Macumba, the Oi Rio Pros — our seventeen-year per-judge dataset contains about eleven thousand individual scoring decisions where we know both the surfer's nationality and the judge's nationality. We can split by period, run the test in each, and see what shows up.

The clean version of the test goes like this. Take Brazilian judges scoring Brazilian surfers. Subtract Brazilian judges scoring non-Brazilian surfers. That's the Brazilian-judge "lift" for compatriots. If the lift is positive, Brazilian judges are favoring their own. Then, as a sanity check, do the same comparison for non-Brazilian judges. The difference between the two lifts is the cleanest available measure of the compatriot effect.

Pre-reform period (2009 through 2022): the compatriot lift is **negative 0.10 points**. Mildly negative. Brazilian judges weren't padding Brazilian surfers' scores; they were giving them slightly *less* of a bump than the rest of the panel.

Post-reform period (2024 through 2026): same test, same direction. The lift is **negative 0.13 points**. Still mildly negative, slightly more so.

Across the entire seventeen-year stretch, the per-judge lift averages out to a slight negative. In no period does the test show the positive compatriot bonus that the fan complaints describe.

This is a delicate story to tell, so I am going to tell it carefully.

The compatriot bonus that everyone yells about — the one the WSL appears to have responded to with the panel-rotation reform — shows up in panel-level ordinary least squares regressions. It is the kind of estimate that pools across heats, controls for surfer skill and event, and asks whether the presence of any compatriot judge on the panel is associated with a higher trim-mean score. That estimate is positive in our data. It is positive in the published cross-sport literature. It is the source of the IJSF (2025) WSL compatriot estimate of plus-0.04 to plus-0.32 points.

It is also, when you run the more careful identification — the difference-in-differences at individual judge × individual surfer cells, which controls by construction for the venue, the wave conditions, the surfer selection, the panel composition, and the calibration drift that the OLS estimate is mixing together — the estimate that reverses to mildly negative.

The WSL judging body changed panel composition. That part is real, identified, replicable. They reduced the *optics* of compatriot stacking — the number of times two Brazilian judges sit in the same room watching a Brazilian surfer surf. That, by itself, is meaningful. It addresses a thing fans complain about. It removes a class of correlation between panel composition and venue / outcome that the panel-level OLS literature has been treating as evidence of bias. Those are real wins.

What the reform may not have changed — because there is no clean evidence it was ever there — is the per-judge behavioral compatriot bonus. That estimate has been mildly negative in every sub-period of our 17-year corpus. The data is consistent with two stories at once. Story one: Brazilian judges have always been slightly stricter on Brazilian surfers, perhaps to overcompensate for the suspicion of compatriot bias. Story two: the panel-level OLS estimate the cross-sport literature reports has been measuring something other than per-judge compatriot bias all along — venue effects, selection patterns, calibration drift. Both stories are consistent with the same data.

---

The clean way to read this is that the WSL judging body has, in the past three years, been quietly running one of the most aggressive optics-level subjective-sport reforms anyone has documented. They never announced it. They never branded it. There was no press release. Pereira took over. The panels rotated. The fan-side narrative — that Brazilian judges were favoring Brazilian surfers — receded, because the panel composition that produced the *appearance* of the bias became less common.

To my knowledge, no prior subjective-sport judging study has ever caught a within-governing-body reform mid-data. We've studied figure skating from the Salt Lake City scandal forward, but the IJS reform was announced — Olympic-press-conference-announced. We've studied gymnastics post-Athens, but the Code of Points overhaul was published. The WSL did this without a publication. They just changed the panels.

There are two ways to feel about that. The first is admiring: in an era when subjective sports are mostly defending their judging legitimacy with public-relations talking points, here's a body that quietly fixed the most-complained-about pattern in their data. They didn't argue. They didn't deny. They rotated the panels and moved the trendline.

The second is skeptical: the only reason we know this happened is that we ran the data ourselves. There's no public ledger. There's no per-judge accountability mechanism. The reform that moved the panel-composition number from 1.72 to 0.84 could be quietly reversed in 2027, and the only people who would catch it would be the small number of people running this kind of analysis. And — the more uncomfortable observation — we cannot independently verify, from per-judge behavior, that there was a behavioral compatriot bias for the panel-rotation reform to address. The reform addressed the appearance of a problem. Whether it addressed a problem in the underlying scoring decisions is harder to say.

The reform is real. What it did is real. What it cannot demonstrate, on the data we have, is that it was solving the problem fans were yelling about.

---

Surfing is a strange sport to study. It pretends to be a competition decided by waves and athletic execution. It is in fact a competition decided by five people sitting in a tower with tablets, deciding what they just saw. The five-person panel is the entire mechanism. Move the panel and you move the sport.

The WSL appears to have understood this and acted on it. They did not announce that they were acting on it. The data shows them acting on it.

That is — somehow, against the grain of how subjective sports usually behave — accountability.

You just have to read the data to see it.

---

*This is the third piece in a six-part series re-analyzing WSL judging. The next piece takes on the methodological keystone of the series: how high inter-judge agreement and unbiased judging are different properties of judging panels, and why the most-cited statistic in defense of WSL judging — that judges agree 97 percent of the time — answers only half the fairness question.*
