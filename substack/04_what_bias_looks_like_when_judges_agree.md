> **SUBSTACK PASTE GUIDE** (delete this entire block when you're done)
>
> 1. Substack > New Post
> 2. **Title field:** What Bias Looks Like When Judges Agree
> 3. **Subtitle field:** Why the most-cited defense of WSL judging — that judges agree with each other 97 percent of the time — is only half the fairness question
> 4. **Body field:** paste everything below the horizontal rule
> 5. Once pasted, delete the H1 (`# Title`) and H2 (`## Subtitle`) at the top of the body — Substack will use the Title/Subtitle fields you set above
> 6. Section breaks (`---`) and headings (`##`, `###`) render natively. Bold (`**`) and italic (`*`) render natively.

---

# What Bias Looks Like When Judges Agree

## Why the most-cited defense of WSL judging — that judges agree with each other 97 percent of the time — is only half the fairness question

A peer-reviewed paper landed in 2025 with a specific claim about the World Surf League. The authors had pulled 4,095 hand-scraped waves from the 2021 men's CT and computed how much the five judges on each panel agreed with each other. The standard statistical measure for this — called intraclass correlation, or ICC — runs from 0 (judges are basically picking random numbers) to 1 (judges always agree exactly). The Santos paper got a number between 0.97 and 1.00. Typical disagreement between two judges scoring the same wave: about 0.15 points on the 0-to-10 scale. The smallest difference between two waves you could reliably detect through the panel noise: 0.25 points.

The paper's framing was that this was good news. Judges agreeing this strongly, this precisely, sounded like fairness. The surf community took it that way. *Beach Grit* covered it, *Stab* nodded approvingly, and in WSL communications the inter-judge correlation became a quietly load-bearing piece of evidence that the judging system was working.

There is a problem with this framing. It has been documented in the academic literature on subjective sports for almost two decades, and it has been ignored almost everywhere outside that literature. The problem is this:

**Reliability and unbiasedness are not the same property.**

If five people share the same prejudice, they will agree with each other. They will agree at near-ceiling. Their inter-rater correlation will look beautiful. And every score they produce will be wrong in the same direction.

This is not a hypothesis. This is a thing that happened in figure skating in the 1990s, in gymnastics through the 1980s, and — for entirely structural reasons unrelated to bad-faith judging — happens in subjective sports any time judges share a common training pipeline, watch the same broadcasts, attend the same coaching clinics, and develop a shared sense of what a "good" performance looks like. They develop a shared prior. They agree. Their scoring is reliable. Their scoring is also biased.

Heiniger and Mercier laid this out cleanly in their 2021 paper on Olympic gymnastics judging, building on a Findlay and Ste-Marie paper from 2004 in figure skating. The cross-sport literature on subjective scoring has been pointing at this distinction for almost two decades. It has not penetrated surfing.

---

I pulled the WSL data myself and replicated the Santos result on a substantially larger sample. For context: Santos worked with 4,095 hand-scraped waves from the 2021 men's tour. The other peer-reviewed paper on WSL judging — published in the *International Journal of Sport Finance* in 2025 — used 21,013 men's waves from 2017 to 2022. The dataset I'm working with goes from 2009 to 2026, men's and women's tour combined, and contains **60,834 panel-trim-mean wave scores along with 301,478 individual judge-scoring decisions**, with judge nationality known on about 86 percent of them. Roughly 15× the size of Santos and 3× the size of IJSF at the panel level. The per-judge layer — what each individual judge gave each wave, with their nationality attached — is, as best I can tell, the largest publicly-available WSL per-judge dataset that exists outside the WSL itself.

The reliability finding replicates cleanly. The inter-judge agreement in this dataset is, in psychometric terms, "near ceiling." The comparison to figure-skating and gymnastics reliability benchmarks is approximate — different sports use differently-constructed scales — but in absolute terms, surf judging exhibits one of the tightest inter-judge agreements in any subjective-sport corpus that has been examined.

By every reliability test, the WSL judging panel is one of the most-agreeing judging panels in subjective sports.

Then we ran the bias tests.

The tests were pre-registered. We sealed our hypotheses, our specifications, and our predicted effect sizes in a public document with a SHA-256 hash on May 3, 2026, before doing any of the analyses we are about to describe.

The reputation prior — judges scoring better-ranked surfers higher even controlling for the wave they actually surfed — replicated cleanly: β = −0.013 per rank position, p = 1.8 × 10⁻⁴. It survives multiple-comparisons correction. The Findlay–Ste-Marie effect from figure skating, in surfing, twenty-two years later, on a much larger dataset.

Round-number anchoring: 59.9 percent of individual judge-scores end in .0/.25/.5/.75 against a uniform null of 20 percent. That's a 3.0× clustering ratio across 301,478 individual judging decisions. Bulletproof.

A descriptive home-event effect: AUS surfers at AUS events score +0.616 points higher than the rest of the field. PRT surfers at PRT events: +0.43. ZAF: +0.43. All highly significant by conventional tests.

A daily amplification effect: scores rise by +1.17 points per event-day, controlling for surfer skill, controlling for venue. Day 1 of a contest, the same surfer rides what is probably an objectively similar wave to Day 5; the Day-5 score is higher by more than a full point on average. *p* = 9.9 × 10⁻¹².

A panel-composition effect: in 2018, the average Brazilian Championship Tour competitor faced a panel containing 1.72 Brazilian judges. By 2026, that number had fallen to 0.84 — a slope a thousand random shuffles of the year labels never reproduce.

These effects are in the data. They are individually small in magnitude — most of them under one point on a 0-to-10 scale, many of them well under half a point — and individually they would barely be visible to a fan. But they exist. Each is significant under conventional inference. Many survive Bonferroni. The strongest ones survive every robustness check we threw at them.

The judges, recall, agree with each other 97 to 100 percent of the time.

---

The way to read this is that the WSL judging panel is exactly what the cross-sport literature says it should be: high-reliability, with a shared subjective prior that produces systematic patterns on identity-correlated covariates. Reliability and unbiasedness are not, mechanically, the same thing. The panel's reliability — the inter-judge correlation Santos measured — tells us almost nothing about whether the panel is biased. It tells us only whether the judges agree with each other. They do. We replicated it. Then we tested for systematic scoring patterns on identity covariates the rubric does not name. We found them. Both can be true.

This is the methodological lesson of the entire cross-sport judging literature for the past twenty years. I did not invent it. I just verified that it applies to surfing, on the larger corpus described above.

---

What is to be done with this?

The most honest answer is that the *first* problem in pro-surf-judging accountability is that the most-cited defense of the system — high inter-judge correlation — is half of the necessary evidence and not the whole of it. You need both. You need to measure reliability *and* you need to measure bias on identity-correlated covariates, and you need to publish them together.

The second problem is that bias on identity-correlated covariates is hard to measure publicly without per-judge data. The WSL has been releasing only panel-trim-mean scores. The trim-mean operation hides the per-judge anchoring, the per-judge calibration drift, the per-judge compatriot patterns. We were able to recover per-judge data on 86 percent of the corpus by scraping Common Crawl WARC archives and the Wayback Machine. That's the only reason the analyses in this series are possible. The WSL itself does not publish them.

The third problem — and this is the one that matters most for the future of the sport — is that the cross-sport literature has documented exactly *one* effective intervention against shared-prior bias in subjective sports. It is not better training. It is not better judges. It is **public per-judge data**. Eric Zitzewitz showed in his 2014 paper on figure skating that the act of publishing each judge's individual scores, with the judge's name attached, with a lag, *substantially reduced* the magnitude of identifiable biases in the seasons after publication began. The exact effect sizes vary by category — some forms of bias dropped sharply, others moved less — but the direction was consistent and the order of magnitude was meaningful. There is a name for this effect, in economic terms: it is reputation-cost discipline. When a judge's individual scores are public, repeated identifiable bias becomes costly to that judge personally — career visibility, future-assignment likelihood, potential public ridicule. The mechanism is not coercive. It is informational.

The WSL could implement this tomorrow. They have the per-judge data. They have always had it. They simply do not publish it. Other subjective sports — gymnastics, figure skating, diving — have all moved to per-judge transparency in the past two decades, in every case as a *response* to a documented bias scandal, in every case improving outcomes.

Surfing has not had its scandal. It is not going to have a scandal in the conventional sense — there's no Salt Lake City moment lurking. What surfing has, instead, is a pile of academic literature now pointing out that the inter-judge correlation everybody keeps quoting is a necessary but not sufficient condition for fair judging. The conversation has shifted. The ICC defense is no longer enough.

The data is there. The methods are there. The only remaining question is whether the WSL — which already, as our first piece in this series documented, appears to have quietly run one of the most aggressive subjective-sport reforms in recorded history — will follow through and publish the per-judge data the sport needs.

---

For most of the twentieth century, judging panels were trusted because they were the only thing available. The fans had no other option. Then the data got bigger, the methods got better, the literature accumulated. By the 2010s, every subjective sport had researchers running these tests. By the 2020s, the tests were granular enough to track individual judges and individual events.

The thing they keep finding is the same thing: judging panels in every measured sport agree with each other beautifully and produce systematically biased outputs at the same time. The two coexist. They've always coexisted. They will keep coexisting until somebody publishes per-judge data and lets the reputational consequences do the work.

Santos is right that WSL judges agree with each other. I replicated that. The figure-skating and gymnastics literatures of the last twenty years are also right that high inter-judge agreement can coexist with substantial measurable bias on identity covariates. I replicated that too. Both things are true at once. They have always been true at once.

The next move — for surfing, for the WSL, for anyone who cares about the sport's competitive integrity — is to stop pretending one of them is enough.

---

*This is the fourth piece in a six-part series re-analyzing the World Surf League's judging on the largest dataset assembled to date. The next piece looks at how every other subjective sport — figure skating, gymnastics, Olympic boxing — got its judging reform, and what surfing's situation tells us about whether evidence alone is sufficient to drive reform when there has been no scandal. The full academic version is forthcoming on SportRxiv.*
