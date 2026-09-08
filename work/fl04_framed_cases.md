# Voice card

**Direct, curious, practical, specific, no buzzwords.**

Standing instruction for my Claude Project:

> Use this voice card for my portfolio: direct, curious, practical, specific, no buzzwords. Write short sentences. Use concrete decisions and results from my work. Keep uncertainty visible. Never invent personal motivations, interview answers, or achievements. Avoid “passionate,” “results-driven,” and “cutting-edge.” If a claim has no evidence, remove it or describe it as a next step.

# Frame It as Cases — Kerem Özcan

**Audience:** An Applied ML Manager at a search or content technology company.  
**One action:** Inspect the FlyRank notebook on GitHub.  
**Scope:** The sitemap calls for one flagship FlyRank project across Home, Work, About, and Contact. The copy below covers all four pages; it does not turn them into four invented projects.

## Home / Hero

### Which pages should an editor review first?

I’m working on that question in the FlyRank ML internship. My current notebook checks 30,000 anonymized pages, defines a review-priority proxy, and measures a simple rule before making any claim about ML.

The first finding is a useful limit: the stale-first rule found declining pages in 22 of its first 50 recommendations. That was below the 60.4% expected from random selection in the same eligible slice.

**[Inspect the FlyRank notebook](https://github.com/KeremOzcn/flyrank-ml-internship-submission/blob/main/work/notebooks/w02_ml_task_framing.ipynb)**

## Work / Case Study

### FlyRank: checking a content refresh rule before building a model

**Status:** Task framing and descriptive baseline complete. Learned ranking and held-out validation remain future work for this case.

### The problem

A content team has more pages than it can review at once. Page age alone is an easy way to build a queue, but being old does not necessarily mean a page needs attention. The decision I framed was: which pages should an editor inspect first for a possible refresh?

I used FlyRank’s starter dataset: 30,000 anonymized content pages across 32 clients. It contains search activity and freshness signals, but no record showing that a refresh helped. That limits what I can call a result.

### What I did and decided

I continued with the content refresh lane and framed it as ranking. The output should order a review queue. I assumed 50 review slots per cycle so the evaluation would match a concrete editorial capacity; this is an exercise assumption, not a measured team workload.

With AI assistance, I completed and executed a pandas notebook that checks the columns, missing values, and page identifiers. I kept pages with at least 100 impressions over 90 days and a nonzero previous 30-day impression count. That left 21,758 pages with enough visibility for this provisional screen and a defined trend comparison.

I used observed impression decline as a proxy for review relevance. The proxy is positive when the dataset labels a page “down,” meaning impressions fell by more than 20% between the two 30-day windows. It is not proof that the page needs rewriting.

The comparison rule puts pages last updated at least 90 days ago first, then orders them by impressions. I chose Precision@50 to count how many of the first 50 review slots reach proxy-positive pages. I also kept missing word counts as missing and treated position zero as unavailable, following the data dictionary.

I separated the label from the working signals. I also documented that the remaining 90-day metrics overlap the decline window: removing the trend columns alone would not make a future-prediction experiment valid.

### What came of it

The notebook runs top to bottom and saves the data checks, sample rows, and baseline results. The working dataframe contains 21,758 pages and 17 columns.

The stale-first rule reached **22 declining pages out of 50: Precision@50 = 44%**. Uniform random selection from this slice has an expected Precision@50 of **60.4%**. This suggests that the particular rule is a weak way to find observed declines in this slice. It does not establish that ML performs better, or that refreshing any of those pages would recover traffic.

The deliverable is a reproducible framing notebook and a baseline to challenge. An editor would still inspect each page before choosing whether to update facts, expand coverage, revise metadata, or leave it alone.

**Next time:** I would define the feature cutoff and a later outcome window before training, then compare the model and rule on held-out clients. I would also seek editor-reviewed priority labels rather than treating decline as refresh need.

**[Inspect the FlyRank notebook](https://github.com/KeremOzcn/flyrank-ml-internship-submission/blob/main/work/notebooks/w02_ml_task_framing.ipynb)**

## About / Methodology

I’m Kerem Özcan, an ML intern working on search performance and content review prioritization. In my FlyRank work, I use Python and pandas to make the decision, data assumptions, and baseline visible before moving to a model.

I use AI to help write and check the work, and make that assistance explicit. The notebook shows what was measured and what still needs validation. I want a reviewer to be able to follow the evidence without taking a headline on trust.

## Contact / Verification

If you’re evaluating how I approach an applied ML problem, start with the notebook. It shows the task choice, the dataframe, the rule comparison, and the limits of the result.

**[Inspect the FlyRank notebook](https://github.com/KeremOzcn/flyrank-ml-internship-submission/blob/main/work/notebooks/w02_ml_task_framing.ipynb)**

## Before / After

**Generic AI line:** “I leverage cutting-edge machine learning to deliver transformative SEO results.”

**Edited version:** “I checked a stale-first content rule on FlyRank’s starter data. It found declining pages in 22 of its first 50 picks—below the random-selection expectation for that slice.”

The edited line names the actual work and a result the notebook supports. It drops the unmeasured claim that the work transformed SEO performance.

## Evidence and final review

- Scope comes from [the portfolio sitemap](fl02_portfolio_sitemap.md); the audience is narrowed to one of the roles already named there.
- Decisions and numbers come from [Week 1 framing](notebooks/w01_research_question.ipynb) and [the executed Week 2 notebook](notebooks/w02_ml_task_framing.ipynb).
- The sitemap’s earlier “3× improvement” headline is not used here. This case does not establish that model result, and its stale-first baseline differs from the starter pipeline’s baseline.
- The paper URL file is still a placeholder, so the CTA points to the notebook instead of promising a deployed paper.
- This draft was assembled by AI from repository evidence at my request. No personal interview was conducted; no interview answers or personal motivations have been invented.

Remaining personal steps:

- [ ] Paste the voice card and standing instruction into the Claude Project. This file does not change Claude’s settings.
- [ ] Read the copy aloud and replace any wording I would not use or cannot stand behind.
- [ ] Commit and push this document, then submit its public GitHub URL.
