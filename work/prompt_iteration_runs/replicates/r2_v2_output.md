# FlyRank Content-Refresh: Task Framing & Baseline Report

**Source notebook:** `work/notebooks/w02_ml_task_framing.ipynb`
**Author:** keremozcan1603@gmail.com
**Date:** 2026-09-08
**Stage:** Task framing + descriptive fixed-rule baseline (no model training)

---

## 1. Purpose

This report summarizes the results of an executed notebook that frames a content-refresh prioritization task for FlyRank and evaluates a simple fixed-rule heuristic against a random-selection baseline. The goal is to give a reviewer enough evidence to judge whether these results justify moving forward with actual model development.

---

## 2. Data & Eligibility

| Item | Value |
|---|---|
| Raw pages (anonymized) | 30,000 |
| Clients | 32 |
| Granularity | One row per page |
| Eligibility filter | `impressions_90d >= 100` AND `impressions_prev_30d > 0` |
| Eligible pages | 21,758 |

**Target definition (proxy label):** `is_declining_proxy = (trend_direction == "down")`, where "down" is defined as a greater-than-20% drop in impressions between two consecutive 30-day windows.

- Proxy-positive eligible pages: **13,152 / 21,758 (≈60.4%)**

Data hygiene checks (missing values, page-ID uniqueness) were performed, and executed outputs were saved.

---

## 3. Task Framing

The operational task is framed as: **given a review capacity of 50 pages per cycle, select the 50 pages most likely to be declining.**

This notebook does not train a model. It establishes:
- The eligible population and proxy label described above.
- A **fixed-rule baseline** (not learned) as a reference point.
- A **random-selection baseline** as a lower-bound sanity check.

Direct label-derived fields are excluded from candidate working signals, but it's noted that retained 90-day impression metrics overlap the same window used to construct the decline label — a caution for future feature design.

---

## 4. Fixed-Rule Baseline

**Rule:** Sort pages by "last updated ≥ 90 days ago" first, then by `impressions_90d` descending. Take the top 50.

| Metric | Value |
|---|---|
| Positives found in top 50 | 22 |
| **Precision@50 (fixed rule)** | **44%** |
| Expected Precision@50 (uniform random) | 13,152 / 21,758 ≈ **60.4%** |

---

## 5. Key Finding

**The fixed rule underperforms random selection by roughly 16 percentage points (44% vs. ~60.4%).**

This is the central, and somewhat counter-intuitive, result of the notebook. Because proxy-positive pages are the majority class (60.4% of eligible pages), any selection method needs to actively identify decline signal to beat a random draw — and this heuristic does not. Prioritizing by staleness (≥90 days since update) and then by traffic volume appears to systematically favor pages that are *not* declining, likely because high-traffic, long-untouched pages may be stable "evergreen" performers rather than pages in active decline.

**Implication:** simple recency + traffic heuristics are not a credible substitute for a learned or better-engineered signal in this setting, since they perform worse than doing nothing informative at all.

---

## 6. What This Notebook Does *Not* Show

To keep scope honest for the reviewer:

- **No learned model** has been trained or evaluated.
- **No held-out evaluation** (train/test split, cross-validation) exists.
- **No observed refresh-benefit outcome** — there is no data on what happens to a page's performance after it is actually refreshed.
- **No causal experiment** — the proxy label is a definitional trend classification, not evidence that refreshing changes outcomes.
- The proxy label window overlaps with retained 90-day features, which risks leakage if those features are used directly in future modeling.

---

## 7. Recommendation for Reviewer

**Does this justify further modeling?** Directionally, yes — but with a caveat on what "further modeling" should target first.

- The fixed-rule baseline's underperformance relative to random selection demonstrates that naive heuristics do not capture decline signal and creates a clear, low bar for a learned model to beat.
- However, before training a predictive model, the overlap between the label window and retained 90-day features should be resolved (e.g., via earlier feature windows) to avoid leakage.
- No outcome or causal evidence yet exists to support that identifying "declining" pages and refreshing them actually improves performance — this remains an open question outside this notebook's scope.

---

## 8. Suggested Future Work (as noted in source)

1. Construct features from **earlier time windows**, decoupled from the label window, to reduce leakage risk.
2. Evaluate against **later outcome windows** to test whether the proxy label is predictive of forward decline.
3. Validate on **held-out clients** (not just held-out pages) to test cross-client generalization, given the 32-client structure of the data.
4. If feasible, design a way to observe actual **refresh outcomes** to move from a proxy/descriptive framing toward a causal or outcome-validated one.

---

*All figures in this report are taken directly from executed notebook outputs. No results beyond what is stated in the notebook are inferred or extrapolated.*
