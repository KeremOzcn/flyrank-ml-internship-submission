# Abstract

This report summarizes FL-01 Target Task 3: task framing and a descriptive fixed-rule baseline for prioritizing FlyRank content refreshes. The executed notebook, completed with AI assistance, analyzes 30,000 anonymized pages from 32 clients. It does not train or evaluate a machine-learning model. The baseline’s Precision@50 is 44.0%, below the 60.4% proxy-positive prevalence in the eligible pool.

# Methodology

The dataset contains one row per page. Eligibility requires `impressions_90d >= 100` and `impressions_prev_30d > 0`, leaving 21,758 pages. The proxy label is `is_declining_proxy = (trend_direction == "down")`; “down” represents an impression decline greater than 20% between consecutive 30-day windows.

Assuming a review capacity of 50 pages per cycle, the fixed rule prioritizes pages last updated at least 90 days ago, then sorts by `impressions_90d` descending. Uniform random selection from the same eligible slice provides the descriptive comparison. Direct label fields were excluded from working signals, although retained 90-day metrics overlap the decline window.

# Results

There are 13,152 proxy-positive pages among 21,758 eligible pages.

| Method | Positives or expected positives at 50 | Precision@50 |
|---|---:|---:|
| Fixed prioritization rule | 22 | 44.0% |
| Uniform random selection (expected) | 30.2 | 60.4% |

The fixed rule is 16.4 percentage points below the random-selection expectation. Missing values and page-ID uniqueness were checked, and the executed outputs were saved.

# Discussion

The rule does not outperform random selection against this decline proxy. This comparison does not explain the underperformance, show that a learned model would perform better, or establish that refreshing selected pages produces a benefit.

The evidence is descriptive only: there is no learned model, held-out evaluation, observed refresh-benefit outcome, or causal experiment. Because retained metrics overlap the proxy’s decline window, the notebook also does not establish a clean temporal separation between predictors and outcomes. Generalization across unseen clients remains unknown.

# Next steps

Further modeling should use earlier feature windows and later observed outcomes, followed by evaluation on held-out clients. A later intervention or causal design would be required to estimate whether content refreshes improve outcomes. Until then, the current baseline does not justify deployment and provides limited evidence for further modeling beyond identifying the required evaluation design.

Source: `work/notebooks/w02_ml_task_framing.ipynb`