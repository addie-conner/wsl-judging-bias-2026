> **SUBSTACK PASTE GUIDE** (delete this entire block when you're done)
>
> 1. Substack > New Post
> 2. **Title field:** The Australian Advantage That Was Mostly Bells
> 3. **Subtitle field:** How the most-cited statistic in WSL judging analysis collapses by an order of magnitude when you ask the right question — and what Jack Robinson at Margaret River has to do with anything
> 4. **Body field:** paste everything below the horizontal rule
> 5. Once pasted, delete the H1 (`# Title`) and H2 (`## Subtitle`) at the top of the body — Substack will use the Title/Subtitle fields you set above
> 6. Section breaks (`---`) and headings (`##`, `###`) render natively. Bold (`**`) and italic (`*`) render natively.

---

# The Australian Advantage That Was Mostly Bells

## How the most-cited statistic in WSL judging analysis collapses by an order of magnitude when you ask the right question — and what Jack Robinson at Margaret River has to do with anything

If you watch a lot of CT heats with someone who is paying half-attention, the loudest argument you'll have is about the Australian leg. Bells, Margaret River, occasionally Snapper. The visiting surfers always seem to come out a little flat. The Aussies always seem to come out a little hot. After enough years of this you start wondering whether what you're seeing is the surfing or the geography.

Here is the statistic.

Australian surfers, competing at Australian-hosted Championship Tour events, score on average 0.616 points higher than the rest of the field at those same events. The standard error is about 0.07. The p-value is around 2 × 10⁻⁹.

That's the kind of number that ends arguments. It clears Bonferroni. It clears false-discovery-rate correction. Run any textbook regression on the WSL data and the AUS home-bloc effect prints out real, large, statistically bulletproof.

And yet.

When you test it six different ways, each one slightly more careful than the last, the answer changes. The same data. Different identification strategies, different answers. By the last test the headline number is gone.

This is what it looks like when the most-quoted statistic in a dataset turns out to be, mostly, an artifact of the question being asked.

---

The naive +0.616 estimate compares the wave-scores of Australian surfers at Australian events to everybody else's. It is the kind of comparison that controls for nothing. The first thing you do, when you don't trust a comparison that controls for nothing, is add controls.

We added them. World rank, year, gender, surfer country, event country. The kitchen-sink regression. The Australian-bloc coefficient came down to about +0.58. Slightly smaller. Still very significant. Still publishable.

This is where the second-pass methodologist asks: but the surfers at Australian events are not random. The waves at Australian events are not random. Bells Beach has waves that are *physically different* from waves at El Salvador. Maybe the +0.6 reflects the fact that good waves attract good surfers and good surfers score high, and Australia happens to host events at venues where Australian surfers — who grew up on those waves — are advantaged. Maybe.

So we ran a within-heat fixed-effect specification. Demean every score within its heat. The within-heat estimate of the Australian-bloc effect dropped to **+0.024**. Almost zero. Not significant.

You see the trick. By holding the wave constant, we're asking: at this specific heat, with these specific waves, do Australian surfers score higher than non-Australians? The answer: barely.

Hold on, says the third-pass methodologist. Within-heat fixed effects discard a lot of data. They might also be controlling away the very effect you're trying to measure, if Australian judges hand out higher scores to *all* surfers at Australian events. There are better tools.

There are. We ran them, each more careful than the last. They all asked the same question — *do Australian surfers actually score higher at Australian events?* — but each one made a different effort to rule out a different alternative explanation.

**Test 1: just compare the averages.** No controls, no adjustments. Australian surfers at AUS events vs everybody else at AUS events. Result: **+0.616 points**.

**Test 2: add the obvious controls.** World rank, year, gender, surfer's home country, event country. Now we're comparing surfers of similar caliber, in similar years. Result: **+0.58 points**. Barely changes.

**Test 3: hold the wave constant.** Compare scores only within the same heat — same wave conditions, same swell, same break, same panel. (The technical name for this is a within-heat fixed-effects regression; what it does is ask, for any given heat, whether Australian surfers score higher than non-Australians in *that specific heat*.) Result: **+0.024 points**. Effectively zero.

**Test 4: let a machine pick the right model.** Run every reasonable specification, weight them by how well each one fits the data, average across all of them. Result: **+0.024 points** — the data prefers the heat-by-heat comparison at almost 100% weight.

**Test 5: use causal-inference machine learning.** This is the standard set of tools economists use when they want to estimate a causal effect from observational data — the methods reduce to "do a flexible model of the outcome, do a flexible model of the treatment, then combine them in a way that's robust to both being slightly wrong." Result: **+0.005 points**, with a confidence interval that comfortably crosses zero. A causal forest run on the same data returns **−0.024 points**, also crossing zero.

**Test 6: shuffle the labels.** Take the data, randomly reassign which surfers count as "Australian" within each event, ten thousand times, and see how often you get a difference as big as +0.616. Result: **about 13% of the time, by chance.** The observed +0.616 is not even statistically rare under random shuffling.

The point estimate moves around. The confidence interval crosses zero. The shuffle test fails to reject random chance. **The "Australian advantage" that prints in the headline as +0.62 collapses to somewhere between essentially zero and +0.10 the moment you ask the question carefully.**

This is what a confounded effect looks like.

---

There's a final test. The cleanest one.

If the Australian-bloc effect were real — if Australian judges were padding the scores of Australian surfers — then on individual events, on individual surfers, we should be able to see it. Take a specific Australian surfer at a specific Australian event. Look at the scores Australian judges gave him. Look at the scores non-Australian judges on the same panel gave him. The difference is the compatriot premium for that surfer at that event.

Take Jack Robinson. Take Margaret River, the Australian-leg event he is most associated with.

Across the Margaret River Pros from 2018 through 2026, we have **995 individual judge-scores given to Jack Robinson** — 354 from Australian judges and 641 from non-Australian judges.

Australian judges scored Jack Robinson, on average: **4.206**.

Non-Australian judges scored Jack Robinson, on average: **4.225**.

The difference is **0.019 points**, with the visiting judges a hair *higher*. The p-value is 0.92. By any sensible test, Australian and non-Australian judges scored Jack Robinson identically at Margaret River. Whatever Robinson earned there, visiting judges saw it the same way his countrymen did.

We ran the same test for Ethan Ewing — an Australian whose Margaret River record makes him exactly the profile a compatriot thumb on the scale would produce, if there were one. Across 579 judge-scores, Australian judges scored Ewing 5.180 and non-Australian judges scored him 5.125. This time the Australians came out higher, by 0.055 points, at a p-value of 0.79. Run the comparison on two different surfers and the sign flips. That is what noise looks like. There is no compatriot premium hiding in either test.

Whatever produced the +0.62 OLS estimate, it was not Australian judges putting their thumb on the scale for Australian surfers.

The cleanest version of this test is a wavepool contest — Surf Ranch, Surf Abu Dhabi — where every ride is mechanically identical and local knowledge is worth nothing. If Australians still scored higher there, the explanation couldn't be the wave. The modern wavepool events with per-judge data total only a few hundred waves, enough to run directionally but not to settle anything, so that test stays on the list.

---

While we're on the subject of effects that look like one thing and turn out to be another, I ran the same kind of test on a completely different question. Sponsorship.

Top professional surfers have sponsor deals with the same brands that put their names on Championship Tour events — Billabong, Hurley, Rip Curl, Quiksilver, Volcom. Jordan asked the obvious follow-up question when I described the Australian-bloc finding: do brand-sponsored surfers score higher at events sponsored by their brand? Does Billabong's stable do better at Billabong Pipeline?

The within-heat test says yes. Brand-sponsored surfers score about a quarter-point higher than their non-brand-sponsored opponents riding the same waves at the same events. Statistically significant. Confidence interval doesn't cross zero.

The within-surfer test — same surfer scoring at brand-sponsored events vs events sponsored by other brands — comes back null. The same John John Florence at Billabong Pipeline scores no higher than the same Florence at events Billabong didn't sponsor. Across thirty surfers with both kinds of events, the within-surfer paired difference is +0.10 points and not statistically significant.

Same shape as the Australian advantage. The headline correlation is real. The cleaner identification cleans it out. The most plausible explanation is that the top brand-sponsored surfers — Florence, Italo Ferreira, Filipe Toledo, Gabriel Medina, Jack Robinson — are also, simply, the top surfers. They win their heats whether or not their brand is on the banner. The descriptive lift you'd see if you ran the naive comparison is mostly a story about which surfers signed which deals, not about whether the deals shift the scoring.

Two caveats travel with that: event-sponsor wildcards tend to go to brand-affiliated athletes, and the sponsor lists are Wikipedia snapshots rather than year-by-year ledgers. The direction is unlikely to flip; the magnitude could move.

Two completely separate questions about WSL judging. Same answer twice.

---

So what was it?

The within-heat fixed-effect specification is the technical answer. When you demean every score within its heat, what's left is the comparison of Australian surfer performance to non-Australian surfer performance *holding the heat constant*. Whatever drives the +0.62 pooled estimate disappears at the within-heat level — which means it lives in *between-heat* variation. Australian surfers and non-Australian surfers, in our data, are not in the same heats in the same proportions. Some heats are stacked with Australian surfers; those heats happen to have higher scores. Others are mixed; their average scores look different. The pooled OLS estimate is reading those compositional differences and reporting them as a national-bloc effect.

Then where does the between-heat variation come from, if not from compatriot judging? Two candidates. First, scheduling: at Australian events, the Australian-leg seedings produce heat compositions that aren't randomized — the Australian surfers tend to cluster in particular brackets. Second, venue: the heats with the most Australian surfers tend to be at specific venues with specific wave conditions, and the venues with the heaviest local-knowledge advantage produce the biggest pooled effects.

We disaggregated the +0.62 by venue. Margaret River, four years of it: AUS-vs-visitor wave-score differences of −0.01, −0.18, +0.32, and −0.10. The sign flips year to year around zero. Snapper Rocks, the 2025 Bonsoy Gold Coast Pro: AUS-vs-visitor difference of *minus 0.30*. Australian surfers underperformed visitors at the most-Australian event of 2025 by a meaningful margin.

Then we got to Bells Beach.

The 2024 Bells contest: **AUS-vs-visitor difference of +0.13**. Modest positive.

The 2025 Bells contest: **AUS-vs-visitor difference of +0.45** — the largest Australian-versus-visitor differential of any event in the four Australian seasons, packed into a single weeklong contest.

A leave-one-event-out check flags 2025 Bells as the single largest contributor to the pooled estimate; the negative Gold Coast event, meanwhile, was pulling the pooled number *down*. The +0.62 isn't an Australian effect spread across the whole tour. It's mostly a Bells effect.

There is a perfectly reasonable, performance-genuine story for why Bells specifically. Bells Beach is the heaviest local-knowledge wave on the calendar. It's a point break with a very specific section that breaks differently depending on swell direction and tide phase. The Bells line-up is a community where Australian surfers grow up surfing. Visiting surfers arrive a week before competition. Bells is also the only contest where you can win a literal 8-foot wood-and-bronze bell on a chain — meaningful ceremony attaches to it; surfers prepare differently. Some fraction of the Bells-specific differential is Australian surfers being better at riding their own home wave.

The +0.62 statistic, the most-cited number in this dataset, is mostly the 2025 Bells Beach Pro.

---

The lesson here is one I keep running into: **statistics tell you what happened. They don't tell you why.**

The naive +0.62 is real, in the arithmetic sense. The numbers add up. But when you interrogate it carefully, the +0.62 turns out to be mostly a Bells effect, and the Bells effect is partly Australian surfers being good at riding a wave they grew up on. The cross-sport literature on compatriot bonuses, going back fifteen years, says when judging-bias effects exist in subjective sports they tend to run between four-hundredths and a third of a point. Our cleanest test on the WSL data lands at about a tenth of a point — small enough that we can't tell with confidence whether it's a real effect or noise.

That's a long way from +0.62.

The fans yelling about Australian judging in the comments section have been sort of right. There's a real, descriptive, replicable home-event effect on the WSL Championship Tour. The cross-sport literature is also right. The magnitude is small and the causal mechanism is mostly venue-and-conditions, not judge-nationality. The fans yelling about Jack Robinson at Margaret River are wrong. Australian and non-Australian judges scored him to within two hundredths of a point of each other. There is no nuance to that finding.

The fans yelling about Billabong's surfers winning at Billabong's events are also sort of right and sort of wrong, in the same shape. The descriptive lift is real. The causal mechanism is mostly that Billabong sponsors the best surfers. Two surveys on the same data, same answer.

Read only the headline number — the +0.62 — and you would walk away believing something the data does not support.

That's not a flaw in the data. It's a recurring shape in how data gets cited. Especially in subjective sports. Especially when the headline number is the one that prints.

---

*This piece draws on the same re-analysis of WSL judging as the last one — 60,834 wave-rows and 301,478 individual judge-scores, 2009 through 2026. Data, code, and the full analysis archive are available on request.*
