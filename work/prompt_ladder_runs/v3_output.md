## Content-refresh prioritization at FlyRank

During my FlyRank internship, I framed content refresh as a ranking problem: given a limited editorial budget of 50 reviews per cycle, which pages should be reviewed first?

The starter dataset contained 30,000 anonymized pages across 32 clients, with one row per content page. I restricted the analysis to 21,758 pages with at least 100 impressions over 90 days and nonzero impressions in the previous 30-day window. This removed pages with insufficient activity for a meaningful trend comparison.

Because the dataset contained no observed outcomes showing whether a refresh improved performance, I could not define a true refresh-benefit target. Instead, I used a diagnostic proxy:

`is_declining_proxy = (trend_direction == "down")`

A page is classified as “down” when impressions fell by more than 20% between consecutive 30-day windows. This proxy identifies declining pages, not pages that would necessarily benefit from editorial intervention.

I evaluated a fixed prioritization rule that:

1. Places pages last updated at least 90 days ago first.
2. Sorts pages within that ordering by 90-day impressions, descending.

Among its top 50 pages, 22 were proxy-positive, giving a descriptive Precision@50 of 44%.

For context, 60.4% of the eligible slice was proxy-positive, so uniform random selection from the same population would have an expected Precision@50 of 60.4%. The rule therefore underperformed random selection against the chosen proxy. This is still a useful result: recency and traffic alone did not concentrate declining pages and may instead favor high-traffic pages whose performance is comparatively stable.

These numbers are full-slice diagnostics, not held-out model results. No model was trained in the notebook, and the exercise should not be interpreted as evidence of production ranking performance. Direct label fields were excluded from the working signals, but retained 90-day metrics overlap the period used to construct the decline proxy, so the setup is not yet suitable for leakage-safe predictive evaluation.

The next step would be to convert the framing into a temporal learning problem: construct features from earlier windows, observe later outcomes such as recovery or incremental value after refresh, and evaluate on held-out clients. That would test both generalization and the decision that actually matters—whether prioritizing a page leads to measurable editorial impact.

The executed analysis, including missing-value checks, page-ID uniqueness validation, and saved outputs, is documented in `work/notebooks/w02_ml_task_framing.ipynb`.