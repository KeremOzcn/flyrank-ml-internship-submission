# FlyRank Content-Refresh Notebook: Research Report

**Source:** `work/notebooks/w02_ml_task_framing.ipynb`
**Scope:** Task framing and a descriptive fixed-rule baseline. No model training was performed.

## 1. Task and Data

The notebook frames a content-refresh prioritization task: given a limited review capacity, which pages should be inspected first as candidates for a "declining" refresh?

The dataset covers 30,000 anonymized pages across 32 clients, one row per page. An eligibility filter (`impressions_90d >= 100` and `impressions_prev_30d > 0`) reduces this to 21,758 eligible pages.

The proxy label `is_declining_proxy` is defined as `trend_direction == "down"`, where "down" indicates a greater-than-20% drop in impressions between two consecutive 30-day windows. Among eligible pages, 13,152 are proxy-positive — a prevalence of roughly 60.4%.

## 2. Baseline Rule and Comparison

Under an assumed review capacity of 50 pages per cycle, a fixed rule was applied: sort eligible pages by (a) last-updated at least 90 days ago, then (b) `impressions_90d` descending. This rule surfaces 22 positives in its top 50, giving **Precision@50 = 44%**.

For reference, uniform random selection from the same eligible pool has an expected Precision@50 equal to the base prevalence, **≈60.4%** (13,152/21,758).

The fixed rule therefore performs *below* the random-selection expectation on this metric. This comparison does not explain why the rule underperforms, does not demonstrate that a learned model is necessary, and does not establish any intervention or refresh benefit — no such experiment was run.

## 3. Data Quality Checks

Missing values and page-ID uniqueness were checked, and executed notebook outputs were saved. These checks address data integrity for the framing exercise but do not constitute an evaluation of any predictive method's generalization or reliability.

## 4. Limitations

- **No learned model** exists in this notebook; only a fixed heuristic rule was evaluated.
- **No held-out evaluation** was performed; the precision figures above are computed on the full eligible/training-adjacent population, not a separate test split.
- **No observed refresh-benefit outcome** is available — there is no data on what happens after a page is refreshed.
- **No causal experiment** was conducted; nothing here supports claims about what refreshing pages would cause.
- **Label overlap risk:** direct label fields are excluded from working signals, but the retained 90-day metrics overlap the same window used to define the decline label, which may inflate or otherwise distort apparent relationships between features and the proxy label.
- The `is_declining_proxy` label is itself a proxy (a >20% window-over-window impression drop), not a validated indicator of content quality decline or refresh need.

## 5. Future Work (Planned, Not Yet Executed)

- Constructing features from earlier windows, with outcomes measured in later windows, to reduce label/feature overlap.
- Held-out client evaluation to test generalization across clients not seen during rule/feature development.

## 6. Conclusion

This notebook establishes a task framing, an eligibility-filtered dataset, a proxy label, and a fixed-rule baseline with Precision@50 = 44%, compared against a random-selection expectation of ≈60.4% on the same pool. This single comparison, on non-held-out data with a proxy label that overlaps its own feature window, is insufficient to judge whether a learned model would outperform simpler rules, whether refresh interventions are beneficial, or whether this approach generalizes to unseen clients or time periods. Further modeling work would need to address the held-out evaluation, feature/label window separation, and causal outcome measurement identified above before such judgments can be made.
