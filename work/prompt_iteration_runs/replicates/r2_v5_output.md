# Abstract

This report summarizes a completed AI-assisted task-framing notebook for FlyRank's content-refresh problem (30,000 anonymized pages, 32 clients). No model was trained; the work establishes eligibility rules, a proxy decline label, and a fixed-rule baseline for prioritizing pages under a 50-page review capacity. The baseline underperforms random selection on the available proxy label, indicating the current evidence does not yet justify further modeling investment.

# Methodology

Eligibility required impressions_90d ≥ 100 and impressions_prev_30d > 0, yielding 21,758 pages from 30,000. The proxy label is_declining_proxy = (trend_direction == "down"), defined as a >20% impression drop between consecutive 30-day windows, producing 13,152 proxy-positive eligible pages. The fixed rule ranks pages by "last updated ≥ 90 days ago" first, then by impressions_90d descending, selecting the top 50 under an assumed 50-page review capacity. Direct label fields were excluded from working signals, though retained 90-day metrics overlap the decline window. Missing values and page-ID uniqueness were checked; outputs were executed and saved. No held-out evaluation or causal/intervention experiment was run.

# Results

| Method | Positives (or expected) at 50 | Precision@50 |
|---|---|---|
| Fixed rule (recency + impressions) | 22 | 44.0% |
| Uniform random (expected) | ~30.2 | 60.4% |

The fixed rule's precision is roughly 16.4 percentage points below the random-selection expectation on the same eligible pool.

# Discussion

Given prevalence of 13,152/21,758 (≈60.4%), uniform random selection at n=50 has an expected precision matching that prevalence. The fixed rule achieves only 44%, below this baseline. This comparison does not explain why the rule underperforms, does not establish that a learned model would do better, and does not demonstrate any refresh-benefit outcome, since no held-out evaluation or causal experiment exists in this notebook. The overlap between retained 90-day metrics and the decline-window definition is a labeling caveat, not a validated leakage finding. This work was completed with AI assistance and remains task framing plus a descriptive baseline.

# Next steps

Planned future work includes constructing features from earlier time windows, evaluating against later, independent outcome windows, and testing generalization on held-out clients. No timeline or resourcing decision is implied by this report.

Source: work/notebooks/w02_ml_task_framing.ipynb
