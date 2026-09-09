# FlyRank Content-Refresh: Research Report

**Source:** `work/notebooks/w02_ml_task_framing.ipynb`
**Prepared for:** Reviewer assessment of readiness for further modeling
**Author:** keremozcan1603@gmail.com
**Date:** 2026-09-08

## 1. Scope

This notebook performs task framing and evaluates a fixed-rule baseline for prioritizing pages for content refresh. It does **not** train or evaluate a machine learning model, and it does not measure any refresh-intervention outcome. All findings below describe a descriptive baseline only.

## 2. Data and Eligibility

- **Raw dataset:** 30,000 anonymized pages across 32 clients, one row per page.
- **Eligibility filter:** `impressions_90d >= 100` and `impressions_prev_30d > 0`.
- **Eligible pages:** 21,758 (of 30,000).
- Missing values and page-ID uniqueness were checked, and executed outputs were saved. No further detail on missingness handling (e.g., imputation) is available from this notebook.

## 3. Proxy Label

`is_declining_proxy` is defined as `trend_direction == "down"`, where "down" indicates a greater-than-20% drop in impressions between two consecutive 30-day windows.

- **Proxy-positive eligible pages:** 13,152 of 21,758 (≈60.4% prevalence).

This is a **proxy** for decline, not a validated ground-truth label, and no independent outcome (e.g., observed traffic recovery after refresh) exists to confirm it reflects a real business need for refresh.

## 4. Fixed-Rule Baseline

**Rule:** Rank eligible pages by (1) last-updated ≥90 days ago, then (2) `impressions_90d` descending. Take the top 50, matching an assumed review capacity of 50 pages/cycle.

**Result:** 22 of the top 50 selected pages are proxy-positive.

- **Precision@50 = 22/50 = 44%**

## 5. Comparison to Random Selection

Uniform random selection of 50 pages from the same eligible pool has an expected precision equal to the pool's prevalence:

- **Expected random Precision@50 = 13,152/21,758 ≈ 60.4%**

The fixed rule (44%) performs **below** the random-selection expectation (60.4%) on this proxy label. This comparison does not explain why the rule underperforms, does not demonstrate that a learned model would do better, and does not establish that acting on this proxy produces any downstream benefit.

## 6. Data-Leakage Caveat

Direct label fields were excluded from the rule's inputs, but the retained 90-day impression metrics (used both to rank pages and to compute the decline proxy) overlap the same time window used to construct `is_declining_proxy`. This overlap means the observed precision figures should not be read as evidence of predictive generalization to a future, unseen window.

## 7. What This Notebook Does Not Show

- No trained or learned model was built or evaluated.
- No held-out or out-of-time/out-of-client evaluation exists.
- No observed refresh outcome (e.g., traffic recovery, ranking change) is available.
- No causal or experimental evidence that refreshing flagged pages helps.
- The precision comparison does not establish that the proxy label is a valid measure of true decline, or that ML is necessary or sufficient to improve on this baseline.

## 8. Future Work (as noted in the source notebook)

- Construct features from earlier windows to reduce overlap with the outcome window.
- Evaluate against later, independent outcome periods.
- Test generalization on held-out clients.

## 9. Summary

At assumed capacity of 50 pages/cycle, the fixed-rule baseline achieves Precision@50 = 44% against a 60.4%-prevalence proxy-positive pool — underperforming random selection on the same slice. This single, non-held-out comparison, built on a proxy label with window overlap, is insufficient to justify further modeling on its own; it establishes only that the current rule does not outperform chance on this proxy under these conditions. Whether a learned model would do better, and whether either approach yields a real refresh benefit, remains unknown and is unaddressed by this notebook.
