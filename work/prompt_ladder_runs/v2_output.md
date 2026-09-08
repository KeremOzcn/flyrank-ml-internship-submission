## Content-refresh prioritization at FlyRank

During my FlyRank internship, I framed a ranking problem around a practical editorial constraint: if a team can review only 50 pages per cycle, which pages should receive attention first?

The starter dataset contained 30,000 anonymized content pages across 32 clients, with one row per page. After requiring at least 100 impressions over 90 days and nonzero impressions in the previous 30-day window, 21,758 pages remained eligible.

Because the dataset contained no observed outcomes showing whether refreshing a page improved its performance, I used a proxy rather than claiming true refresh benefit. A page was marked proxy-positive when its trend direction was “down,” representing an impression decline greater than 20% between consecutive 30-day windows.

I evaluated a simple fixed prioritization rule:

1. Rank pages last updated at least 90 days ago ahead of newer pages.
2. Within that ordering, sort by 90-day impressions in descending order.
3. Select the first 50 pages for editorial review.

The rule identified 22 declining pages in its top 50, giving a descriptive Precision@50 of 44%. However, the eligible population’s proxy-positive rate was 60.4%, so uniformly selecting 50 pages from the same slice would be expected to achieve 60.4% Precision@50. The heuristic therefore underperformed the random baseline on the chosen proxy.

This is a useful negative result. It shows that combining content age with traffic volume does not necessarily prioritize pages currently exhibiting the defined decline signal. It also demonstrates why even intuitive editorial rules need explicit baselines before being treated as effective.

These figures are full-slice descriptive results, not held-out model performance. No machine-learning model was trained in the notebook. Direct label fields were excluded from the working signals, but the retained 90-day metrics still overlap the period used to define decline, so the setup is not suitable for causal or deployment claims.

The notebook also validates missing values and page-ID uniqueness and preserves executed outputs for reproducibility. The next step would be to construct features from earlier time windows, measure later refresh outcomes, and evaluate ranking performance on held-out clients.

Artifact: `work/notebooks/w02_ml_task_framing.ipynb`