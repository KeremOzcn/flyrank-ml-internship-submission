# FlyRank Content-Refresh: Task Framing and Baseline Report

## Abstract
This report summarizes a completed task-framing and descriptive baseline exercise for a content-refresh prioritization problem, not a trained model. Using a fixed heuristic rule over 21,758 eligible pages (from 30,000 anonymized pages across 32 clients), the notebook evaluates whether staleness-plus-traffic sorting outperforms random selection at a 50-page review capacity. It does not.

## Methodology
Eligibility required impressions_90d ≥ 100 and impressions_prev_30d > 0. The proxy label is_declining_proxy flags pages with trend_direction == "down," defined as a greater-than-20% impression drop between consecutive 30-day windows. The fixed rule ranks pages by last-updated recency (≥90 days first), then by impressions_90d descending, selecting the top 50. Direct label fields were excluded from ranking signals, though retained 90-day metrics overlap the decline-detection window. Missing values and page-ID uniqueness were checked; outputs were executed and saved. No model was trained, no held-out split was used, and no refresh-outcome or causal experiment was observed.

## Results

| Method | Positives (or expected) at 50 | Precision@50 |
|---|---|---|
| Fixed rule (staleness + impressions) | 22 | 44% |
| Uniform random (same slice) | ~30.2 (13,152/21,758 × 50) | ~60.4% |

Proxy-positive prevalence among eligible pages is 13,152/21,758 (60.4%).

## Discussion
The fixed rule's Precision@50 (44%) is below the random-selection expectation (~60.4%) on the same eligible pool. This gap indicates the heuristic does not concentrate proxy-positive pages better than chance in this slice; it does not explain the cause of underperformance, does not demonstrate that a trained model would do better, and does not establish any refresh-benefit or causal effect, since no intervention outcome was observed. The overlap between retained 90-day metrics and the decline-window definition warrants caution before treating these fields as clean predictive signals. Missingness and ID-uniqueness checks were performed but do not by themselves confirm data readiness for modeling.

## Next steps
Planned work includes constructing earlier feature windows, later outcome windows, and held-out client splits to enable a genuine train/evaluate separation. Only after such an evaluation exists can claims about predictive lift or refresh benefit be assessed.

**Source:** work/notebooks/w02_ml_task_framing.ipynb
