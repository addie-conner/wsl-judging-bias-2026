> **SUBSTACK PASTE GUIDE** (delete this entire block when you're done)
>
> 1. Substack > New Post
> 2. **Title field:** Judges Have a Thing for Round Numbers
> 3. **Subtitle field:** What 301,478 individual scoring decisions tell us about how the human brain refuses to count past the nearest fraction it likes
> 4. **Body field:** paste everything below the horizontal rule
> 5. Once pasted, delete the H1 (`# Title`) and H2 (`## Subtitle`) at the top of the body — Substack will use the Title/Subtitle fields you set above
> 6. Section breaks (`---`) and headings (`##`, `###`) render natively. Bold (`**`) and italic (`*`) render natively.

---

# Judges Have a Thing for Round Numbers

## What 301,478 individual scoring decisions tell us about how the human brain refuses to count past the nearest fraction it likes

I love surfing. It's the most beautiful thing in the world.

But as a data person, I can't get past the scoring.

I ran this analysis last night. The Gold Coast Pro was on. Jordan was watching. I was at my laptop, because at some point along the way the data had gotten more interesting to me than the heats. I needed to know whether what I'd been picking up over years of watching was actually a pattern, or whether I was just remembering the events where I happened to be right.

So I pulled the data. About sixty thousand panel-trim-mean wave scores, plus three hundred thousand individual judge-scoring decisions, across seventeen years of Championship Tour competition. Roughly fifteen times the size of the largest published academic study of WSL judging, and as best I can tell the largest publicly-available WSL judging dataset outside the league itself.

This is the first of six pieces.

This piece is the first of six things I found. It's the most universal — it has nothing to do with surfing, really. It has to do with how human brains count.

---

Picture the tower. Five judges, five tablets, a wave breaking outside. About thirty seconds to decide.

The scale is 0.00 to 10.00 in 0.01 increments. A thousand and one possible scores. You can give a 6.43, a 7.18, a 4.91. The math doesn't care. The leaderboard doesn't care. Nobody around you cares. The surfer is paddling back out, the broadcaster is cutting away, the tablet just wants a number.

What I noticed when I started looking at score distributions, across seventeen years of WSL Championship Tour data, is how few of those thousand-and-one numbers ever actually get used.

About **60 percent of all professional surf judging scores end in .0, .25, .5, or .75**.

Statisticians will argue about what number you should compare 60% against. Skip the argument. The strictest version of "what chance would produce" is four percent. The most generous is twenty percent. Either way, 60% is well off the chart. The judges are clustering on round numbers somewhere between three and fifteen times more than they would by accident.

Somewhere between the wave breaking and the score appearing on the screen, something is happening to professional judges that has very little to do with surfing.

---

This pattern has a name. Cognitive scientists call it round-number anchoring or, slightly more dryly, ordinal-scale clustering.

It shows up everywhere. Real-estate listings: $499,000 happens far more than $498,750 even though the difference is meaningless. Restaurant menus: $14.95 and $15.00 are common; $14.83 doesn't appear. Self-reported personal data: in a survey of roughly any kind, more people will tell you they are 40 than 39 or 41, more people say they weigh 180 than 178 or 181. Auction bids cluster on round numbers. Tip amounts cluster on round numbers. Court verdicts cluster on round numbers — there's a published paper showing that personal-injury settlements pile up at $50,000 and $100,000 and $250,000 and almost nowhere else nearby.

The brain has a strong preference for round numbers. The cleanest research suggests this is because round numbers are easier to retrieve from working memory and require fewer cognitive steps to generate. When you are forced to produce a number under time pressure — *quickly, what was that wave worth?* — your brain doesn't actually search the full space of possible answers. It narrows to a small mental palette of "score-shaped" numbers, and a 6.5 lives in that palette while a 6.43 doesn't.

This is not a flaw in surf judging. It's a cognitive feature of how humans count under time pressure. Surf judges aren't doing anything wrong. They are doing something *human*.

But the consequences for surfing are real, and worth thinking through.

---

The first thing to understand is that surf scoring is a trim-mean operation. Five judges score each wave. The high and low scores get dropped. The middle three get averaged. That number — to two decimal places — is the wave's official score.

If three judges all anchor on .5 endings, the trim-mean is going to land on a .5 ending too, or close to it. If a judge says 7.5 because their brain prefers 7.5 to 7.4 or 7.6, and another judge says 7.5 for the same reason, and a third judge says 7.0 because *their* brain prefers 7.0, the trim-mean is going to pop out at something like 7.33. The wave probably "deserved" something between 7 and 7.5, and the wave got scored somewhere between 7 and 7.5, and from a fan's standpoint everything looks fine.

The problem is that the round-number anchor doesn't just hit the middle of the distribution. It hits the *boundaries* — the close calls.

A wave is being scored. One judge thinks the right number is somewhere between a 7 and a 7.5. They have to pick one. They pick 7.5, because their brain prefers half-points. Now imagine a different wave, half a step worse. The same judge reaches for the same mental palette. They pick 7.5 again. The two waves get the same score, even though one was modestly better than the other.

Across 60,000 waves a season, this kind of compression happens thousands of times. Most of the time it doesn't matter. Sometimes it matters. Once or twice a season, in a heat that decides a final, the difference between an 8.5 and a 7.5 — both of which a judge might have been willing to give, for waves that actually merited an 8.0 and a 7.7 — is the difference between who advances and who goes home.

---

You can see the effect at every level of granularity. Across all 60,834 trim-mean wave-scores in the corpus, **22.7 percent end in .0 or .5**. The mechanical baseline — the rate you'd get if judges weren't anchoring at all and the trim-mean were computed honestly across uniform inputs — is around 6.7 percent. So the trim-mean rate is **3.4 times the mechanical baseline**.

At the per-judge level, where the anchoring happens before the trim-mean has a chance to dilute it, the rate is even higher: **59.9 percent of individual scores end in .0, .25, .5, or .75**. The uniform-random null is 20 percent. The observed-to-null ratio is 3.0.

The pattern holds across genders. Across years. Across all top judging-pool nationalities. We checked Brazilian, Australian, American, French, Portuguese, and South African judges separately. They all anchor on round numbers. The rate varies a little — Brazilian judges anchor slightly more, French judges slightly less — but every nationality is well above the null.

This is not a fixable bias by retraining individual judges. It is a property of how humans count.

---

There is a fix, though, and it's not complicated.

Olympic gymnastics ran into this problem decades ago and partially solved it by moving to a 0.0–10.0 scale with mandated 0.1 increments and explicit deduction tables. The deductions force judges to *compute* a score from a sum of categories rather than *generate* a score holistically. You add 0.1 for a step out, 0.3 for a fall, 0.5 for a major form break, and so on. The scoring is constructed, not retrieved. Round-number anchoring still happens at the deduction-category level, but it can't anchor the final score because the final score is a sum.

Olympic diving uses a different fix. Judges score on a 0.0–10.0 scale in 0.5 increments — scores literally cannot end in anything other than .0 or .5. Round-number anchoring is forced to be visible because the underlying scale is round. Bias is then easier to detect at the inter-judge level (when a judge keeps giving 6.5s for a dive that the rest of the panel calls a 7.0).

Surfing could do either. The simplest version: **let judges score on a 0–100 integer scale, then display it as 0.0–10.0 in 0.1 increments**. The judge's input palette no longer contains .25 or .5 to anchor on; the displayed score reads exactly the way fans are used to. The trade-off is that you lose one decimal of input precision; in exchange you reduce the strongest single anchoring channel in the data.

A randomized-anchor variant is also possible: the visible increment moves by 0.01 each wave, so the judge cannot anchor on a fixed mental palette across wave-to-wave decisions.

Neither reform fully removes round-number anchoring — humans can still cluster on whole numbers, decade markers, and other cognitive shortcuts even when half-points and quarter-points are absent — but both reforms reduce the dominant channel observable in the current data. Across a season the reduction would probably move outcomes by a heat or two. Possibly by a title.

---

The thing I keep coming back to, when I look at this data, is that the round-number bias is the cleanest, most-replicable, most-bulletproof finding in the entire 17-year corpus. It survives every multiple-comparisons correction we throw at it. It survives at every venue, every surfer, every year. It is independent of every other bias mechanism we tested.

It also survives the discipline test that matters most — pre-registration with held-out validation. Before running any of the analyses you are reading about, I sealed the 2025 women's Championship Tour data (n = 1,815 panel-trim-mean wave-rows) at a public commit hash and committed not to look at it during the discovery phase. After all the analyses on the training data were locked, I opened the held-out file. The trim-mean round-rate on the held-out 2025 women's CT was 25.2 percent on .0/.5 endings, against 22.7 percent in the training-period data. Effectively identical.

A note on what this validates: the held-out test is at the panel-trim-mean level, which is the secondary version of the round-number metric. The headline 60-percent per-judge clustering rate isn't independently held-out, because the corpus split was at the wave-row level rather than the per-judge-score level. Both metrics replicate cleanly within their respective scopes; the held-out evidence is strongest for the trim-mean clustering rate specifically.

That is not a methodology that can be retroactively gamed. It is also not a methodology subjective-sport governance has historically demanded of itself. The fact that the trim-mean clustering rate shows up identically in the sealed and the open data is the strongest version of *that* claim available, and the per-judge clustering rate replicates within the training period across every disaggregation we tested.

It is the most-true thing we know about WSL judging, and it has nothing to do with surfing. It is what happens when you put humans in a tower and ask them to grade waves on a continuous scale, under time pressure, for a national broadcast audience.

The bias that gets the most attention in pro surfing is compatriot bias. It's small, probably venue-confounded, and what fans yell about. The bias that the rigorous identification keeps flagging as real is round-number anchoring. Most fans don't know about it. The WSL has never publicly addressed it.

The most important bias in subjective sports is often the one nobody's yelling about. It just sits there, in the data, repeating itself across every event for seventeen years. You only see it if you go looking.

---

*This is the first piece in a six-part series re-analyzing the World Surf League's judging on the largest dataset assembled to date — 60,834 wave-rows and 301,478 individual judge-scores spanning 2009 through 2026. The next piece looks at the most-quoted statistic in WSL judging analysis — that Australian surfers get a +0.62 point boost in Australian events — and what happens to that statistic when you ask the right question.*
