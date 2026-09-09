# Research Report: FlyRank Content-Refresh Prioritization — Task Framing & Baseline Rule

**Prepared for:** keremozcan1603@gmail.com
**Source notebook:** `work/notebooks/w02_ml_task_framing.ipynb`
**Report date:** 2026-09-08
**Status:** Task framing and descriptive baseline only — no model training performed

---

## 1. Executive Summary

This report summarizes the first analytical pass at the FlyRank content-refresh prioritization problem: given limited editorial review capacity, which pages should be flagged for refresh first? The current notebook does **not** train a predictive model. It defines the problem, constructs an eligibility filter, builds a proxy label for "declining" pages, and tests one fixed heuristic rule against a uniform-random baseline.

**Key finding:** the fixed rule (recency-then-traffic sort) achieves **Precision@50 = 44%**, which is **worse** than the expected precision of uniform random selection from the same eligible pool (**≈60.4%**), because 60.4% of eligible pages are already proxy-positive. This result does not yet justify further modeling investment on its own — it primarily indicates that the current heuristic is not competitive with chance, and that the labeling/eligibility setup needs scrutiny (see Section 5) before any model is trained on it.

---

## 2. Background and Motivation

FlyRank content teams operate with fixed review capacity (assumed at **50 pages per cycle**) and need a way to prioritize which pages are most likely to be declining in organic performance and therefore worth refreshing. This notebook frames that as a ranking/prioritization task and establishes a first, non-learned reference point — a fixed business rule — before any model-based approach is considered. The purpose of this report is to give a reviewer enough evidence to decide whether the problem framing and data are sound enough to proceed to actual model development.

---

## 3. Data and Methodology

### 3.1 Dataset
- 30,000 anonymized pages across 32 clients, one row per page.

### 3.2 Eligibility Filter
Pages were required to have:
- `impressions_90d >= 100`
- `impressions_prev_30d > 0`

This filter reduced the working set from 30,000 to **21,758 eligible pages**.

### 3.3 Proxy Label
`is_declining_proxy` is defined as `trend_direction == "down"`, where "down" indicates a **greater-than-20% drop in impressions** between two consecutive 30-day windows. Within the eligible set, **13,152 pages (≈60.4%)** are proxy-positive.

### 3.4 Fixed-Rule Baseline
Given the assumed capacity of 50 pages per review cycle, a simple, non-learned rule was applied to the eligible pool:
1. Prioritize pages last updated ≥90 days ago.
2. Within that, sort by `impressions_90d` descending.

The top 50 pages from this ordering were evaluated against the proxy label.

### 3.5 Comparator
Expected precision of uniform random selection of 50 pages from the same 21,758-page eligible pool, given the base rate of positives (13,152 / 21,758).

### 3.6 Data Quality Checks
- Missing-value checks were run on the working fields.
- Page-ID uniqueness was verified.
- All outputs were executed and saved in the notebook.

---

## 4. Results

| Method | Precision@50 | Basis |
|---|---|---|
| Fixed rule (recency → impressions desc.) | **44%** (22/50) | Observed, executed in notebook |
| Uniform random selection | **≈60.4%** | Expected value, 13,152/21,758 |

**The fixed rule underperforms random selection by roughly 16 percentage points.** No learned model, held-out evaluation, observed refresh-benefit outcome, or causal experiment exists in this notebook — all comparisons are descriptive, on the same in-sample eligible pool.

---

## 5. Analysis and Discussion

### 5.1 The heuristic is worse than chance
Because 60.4% of the eligible pool is already proxy-positive, any list of 50 pages is likely to contain many positives by chance alone. A useful rule should exceed this base rate; the fixed rule instead falls below it. This suggests that "last updated ≥90 days ago, then impressions descending" is either uncorrelated with, or mildly anti-correlated with, the specific 20%-drop definition of decline used here. Before concluding the rule is genuinely bad, note the following caveats.

### 5.2 Label overlap / potential leakage risk
The retained 90-day metrics (e.g., `impressions_90d`, used both in the eligibility filter and in the fixed rule's sort key) **overlap the same window used to construct the decline label**. Direct label fields were excluded from the working signals, but this overlap means the eligible pool and the ranking rule are already entangled with the outcome window. This is a caution flag for any future model: features drawn from the same 90-day window as the label risk leakage and inflated (or, as seen here, misleadingly deflated) apparent performance. This needs to be resolved by using earlier feature windows before modeling.

### 5.3 No outcome or causal evidence
This exercise measures whether a page *currently looks declining by proxy*, not whether refreshing it would help. There is no observed refresh outcome and no causal design in this notebook. Precision@50 here answers "did we pick pages that are already down 20%+," not "did picking them lead to recovery." These are different questions, and only the former is addressed.

### 5.4 High base rate limits headroom
With 60.4% of eligible pages already proxy-positive, precision-based ranking has limited ceiling for improvement in absolute terms — most reasonable methods will score in a similar band unless a genuinely predictive signal is found. This raises the question of whether precision alone is the right metric, versus something like early detection (catching declines before the proxy threshold is crossed) or ranking quality (AUC/lift) on a less contaminated feature set.

---

## 6. Limitations

- **No model was trained**; this is task framing plus a single fixed rule.
- **No held-out data**; all evaluation is in-sample on the same eligible pool used to build the rule and label.
- **Proxy label only**; "declining" is operationalized purely as a >20% impression drop between two 30-day windows, not validated against any independent ground truth of true content decline.
- **Feature/label window overlap**; 90-day metrics used for ranking overlap the window that defines the label, risking leakage in any future model.
- **No causal or outcome data**; refresh benefit is not measured or estimated anywhere in this notebook.
- **Capacity assumption**; the 50-pages-per-cycle figure is stated as an assumption, not derived from operational data.

---

## 7. Future Work (as identified in the notebook)

- Use **earlier feature windows** (features computed strictly before the label window) to remove overlap/leakage risk.
- Evaluate against **later outcome windows** to test whether flagged pages' performance actually changes after refresh.
- Validate on **held-out clients** rather than in-sample evaluation on the same 32-client, 30,000-page pool.

---

## 8. Recommendation for the Reviewer

The current evidence does **not** yet justify moving to model training as-is. Before further modeling investment:
1. Resolve the feature/label window overlap (Section 5.2) — this is a prerequisite, not optional polish.
2. Re-run the fixed-rule vs. random comparison on leakage-free features to get a trustworthy baseline.
3. Decide whether precision@k is the right target metric given the high (60%) positive base rate, or whether an early-warning / lift-based framing would better reflect the business need.

Only after these steps produce a baseline that reliably beats random selection on clean, non-overlapping features would there be a solid rationale for training a learned model.
