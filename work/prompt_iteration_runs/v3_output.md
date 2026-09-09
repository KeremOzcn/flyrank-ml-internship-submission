# Research Report: FlyRank Content-Refresh Task Framing (FL-01, Target Task 3)

**Author:** keremozcan1603@gmail.com
**Date:** 2026-09-08
**Source notebook:** `work/notebooks/w02_ml_task_framing.ipynb`
**Scope:** Task framing and a descriptive fixed-rule baseline. No model was trained or evaluated in this work.

---

## 1. Summary

This notebook frames a content-refresh prioritization problem and evaluates a single fixed heuristic rule against a random-selection baseline, on one snapshot of data. Under a fixed review budget of 50 pages, the rule identified 22 proxy-positive pages (Precision@50 = 44%), which is **below** the ~60.4% expected from uniform random selection over the same eligible pool. No learned model, held-out evaluation, causal experiment, or observed refresh outcome is present. These results describe the behavior of one heuristic on one snapshot; they do not establish that ML is necessary, that the rule is broken, or that refreshing flagged pages improves outcomes.

## 2. Data and Eligibility

- Dataset: 30,000 anonymized pages across 32 clients, one row per page.
- Eligibility filter: `impressions_90d >= 100` and `impressions_prev_30d > 0`.
- Eligible pages: 21,758 (of 30,000).
- Missing values and page-ID uniqueness were checked prior to analysis; executed outputs were saved. Whether missingness affects downstream conclusions was not independently tested.

## 3. Proxy Label

- `is_declining_proxy = (trend_direction == "down")`, where "down" is defined as a greater-than-20% impression drop between two consecutive 30-day windows.
- Proxy-positive eligible pages: 13,152 of 21,758 (≈60.4% prevalence).
- Direct label fields were excluded from the working signal set used by the rule. However, the retained 90-day impression metrics overlap the same window used to construct the decline proxy, so the rule's exposure to information related to the label cannot be ruled out from this notebook alone.

## 4. Baseline Method

Given an assumed capacity of 50 pages per review cycle, a fixed rule was applied to the eligible pool:

1. Prioritize pages last updated ≥ 90 days ago.
2. Within that group, sort by `impressions_90d` descending.

This is a deterministic, non-learned rule; no parameters were fit to data.

## 5. Results

| Selection method | Positives in top 50 | Precision@50 |
|---|---|---|
| Fixed rule (recency + impressions) | 22 | 44.0% |
| Uniform random (expected) | — | ≈60.4% |

The rule's Precision@50 is roughly 16 percentage points below the random-selection expectation for the same eligible pool. Given eligible-pool prevalence of ~60.4%, a rule scoring below chance suggests its ranking criteria (staleness, then raw impression volume) may be anti-correlated with the decline proxy in this snapshot — for example, because high-impression pages may be less likely to show a >20% drop, or because "long-since-updated" pages skew toward already-stable traffic. This notebook does not test *why* the rule underperforms, nor whether a different fixed rule or a learned model would do better.

## 6. Limitations

- **No learned model was built or evaluated.** All comparisons are between a fixed heuristic and a random-selection expectation.
- **No held-out evaluation.** Results reflect a single snapshot; there is no train/test or held-out-client split.
- **No causal or intervention evidence.** Nothing here indicates whether refreshing the selected pages would change impressions, rankings, or any downstream business metric.
- **Possible feature/label overlap.** Retained 90-day impression metrics used by the rule overlap the same 30-day windows used to define the decline proxy, which complicates interpreting Precision@50 as a clean measure of predictive value.
- **Single time snapshot.** No temporal separation exists between the features used for ranking and the window used to compute the proxy label.

These gaps mean the comparison above should be read narrowly: it describes how one fixed rule ranks pages in one eligible pool relative to chance, nothing more.

## 7. Future Work

The notebook identifies three concrete next steps:
- Use earlier feature windows, separated in time from the outcome window.
- Evaluate against later, independently observed outcomes rather than a same-window proxy.
- Validate on held-out clients not seen during rule/feature development.

## 8. Conclusion

The completed work establishes a reproducible eligibility filter, a proxy decline label, and a fixed baseline rule, with basic data-quality checks performed and outputs saved. The rule's Precision@50 (44%) underperforms the random-selection expectation (~60.4%) on this snapshot. This finding motivates further investigation — including feature/label timing fixes and out-of-sample validation — but on its own does not demonstrate that the rule is flawed in general, that a learned model would perform better, or that any refresh intervention has value. Those questions remain open and are appropriately deferred to future modeling work.
