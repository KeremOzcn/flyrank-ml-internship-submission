# FlyRank Content-Refresh Prioritization: Task Framing & Baseline Report

**Author:** keremozcan1603@gmail.com
**Source notebook:** `work/notebooks/w02_ml_task_framing.ipynb`
**Report date:** 2026-09-08
**Status:** Task framing + fixed-rule baseline (no model training)

---

## 1. Purpose

This report summarizes the executed results of a task-framing exercise for prioritizing which pages to refresh in a content-decline detection workflow ("FlyRank"). The notebook does **not** train or evaluate a learned model. It defines the prediction target, establishes an eligibility filter, and tests a simple fixed-rule heuristic against a fixed review capacity, benchmarked against uniform random selection. The goal of this report is to help a reviewer judge whether these results justify investing in further modeling.

---

## 2. Data

| Item | Value |
|---|---|
| Total pages | 30,000 (anonymized), one row per page |
| Clients | 32 |
| Eligibility filter | `impressions_90d >= 100` AND `impressions_prev_30d > 0` |
| Eligible pages | 21,758 |
| Data quality checks | Missing values and page-ID uniqueness verified |

## 3. Target Definition

- **Proxy label:** `is_declining_proxy = (trend_direction == "down")`
- **"Down"** is defined as a greater-than-20% drop in impressions between two consecutive 30-day windows.
- This is a **proxy** label derived from observed traffic trend, not a validated or causal indicator of content decay requiring refresh.
- **Proxy-positive eligible pages:** 13,152 of 21,758 (≈ 60.4% base rate within the eligible set).

## 4. Task Setup

- **Assumed review capacity:** 50 pages per cycle.
- **Fixed rule (heuristic, not learned):**
  1. Prioritize pages last updated ≥ 90 days ago.
  2. Within that, sort by `impressions_90d` descending.
- **Comparator:** uniform random selection of 50 pages from the same eligible slice.

## 5. Results

| Method | Positives in Top 50 | Precision@50 |
|---|---|---|
| Fixed rule (staleness → impressions) | 22 / 50 | **44.0%** |
| Uniform random (expected) | 13,152/21,758 rate | **≈ 60.4%** |

**Key finding:** The fixed rule's Precision@50 (44%) is **lower** than the expected precision of random selection from the same eligible pool (≈60.4%). In other words, on this evidence, the staleness-then-impressions heuristic performs worse than chance at surfacing proxy-declining pages within the review-capacity budget.

## 6. Discussion & Caveats

- **No model was trained or evaluated.** These results describe a fixed, non-learned prioritization rule and a random baseline for comparison — nothing here reflects predictive modeling performance.
- **No held-out evaluation exists.** Precision@50 was computed once on the full eligible set that also defines the base rate; there is no train/test split or held-out client group.
- **No observed refresh-benefit outcome or causal experiment.** The label (`is_declining_proxy`) measures a traffic-trend pattern, not whether refreshing a page actually improved its performance. Nothing in this notebook establishes that acting on this label produces benefit.
- **Potential label overlap / leakage risk:** while fields directly encoding the label were excluded from candidate working signals, the retained 90-day impression metrics used for ranking overlap the same window used to compute the decline trend. This means the heuristic's inputs are not cleanly separated from the outcome window, and any future modeling work should treat this as a leakage risk to resolve, not as evidence in the rule's favor.
- **Base-rate sensitivity:** because the proxy-positive rate in the eligible pool is high (~60%), even random selection performs well by Precision@50; this makes precision alone a weak signal of ranking quality here. A rule needs to clear a ~60% bar, not a low one, to be considered informative.
- **Scope of the fixed rule:** the rule was evaluated on one static snapshot with one capacity setting (50). No sensitivity analysis across capacities, clients, or repeated random draws is available in this notebook.

## 7. Conclusion

On the evidence produced in this notebook, the fixed staleness-then-impressions heuristic **does not outperform random selection** at the assumed review capacity of 50 pages, and in fact underperforms it by roughly 16 percentage points of Precision@50. This is a negative/inconclusive result for the heuristic as framed, not a demonstration of readiness for further modeling. Before investing in a learned model, the immediate priority should be resolving the feature/label window overlap and establishing a proper held-out evaluation — a positive result for a fixed rule under a leaky evaluation would not be reliable evidence to build on, and this run does not even produce a positive result.

## 8. Recommended Future Work (per notebook)

- Construct features from **earlier windows** than the label window to remove overlap with the decline period.
- Evaluate against **later, out-of-window outcomes** rather than the same trend period used to define the label.
- Use **held-out clients** (not just held-out pages) to test generalization across the 32-client population.
- Only after these fixes: consider a learned ranking/classification model, and re-benchmark against both the random baseline and this fixed rule.

---
*All figures above are taken directly from the executed outputs of `work/notebooks/w02_ml_task_framing.ipynb`. No results beyond what is reported in that notebook are inferred or estimated.*
