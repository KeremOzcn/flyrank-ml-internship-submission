# FlyRank Content-Refresh: Task Framing and Baseline Rule Report

## Abstract
This report summarizes a completed task-framing notebook, produced with AI assistance, that establishes a descriptive proxy for declining pages and evaluates a fixed heuristic rule against uniform random selection. No model was trained, no held-out evaluation was performed, and no causal or intervention outcome was observed. The comparison below is descriptive only and does not establish that machine learning is necessary or that refreshing flagged pages improves outcomes.

## Methodology
The dataset contains 30,000 anonymized pages across 32 clients, one row per page. Eligibility requires impressions_90d ≥ 100 and impressions_prev_30d > 0, yielding 21,758 eligible pages. A proxy label, is_declining_proxy, is set when trend_direction == "down," defined as a greater-than-20% impression fall between consecutive 30-day windows; 13,152 eligible pages are proxy-positive. Assumed review capacity is 50 pages per cycle. The fixed rule orders pages by "last updated ≥90 days ago" first, then by impressions_90d descending, and selects the top 50. Direct label fields were excluded from working signals, though retained 90-day metrics overlap the decline window. Missing values and page-ID uniqueness were checked; outputs were executed and saved.

## Results

| Method | Positives (or expected) at 50 | Precision@50 |
|---|---|---|
| Fixed rule (recency + impressions) | 22 | 44.0% |
| Uniform random (expected) | ~30.2 | ~60.4% |

The rule's Precision@50 (44.0%) is below the random-selection expectation for the same eligible pool (~60.4%), a gap of roughly 16.4 percentage points.

## Discussion
This gap is descriptive: it does not identify why the rule underperforms random selection, does not prove a learned model would do better, and does not establish that selecting proxy-positive pages produces any observed refresh benefit—no such outcome was measured. The proxy label itself overlaps the 90-day metrics used for ranking, so agreement or disagreement between rule and proxy may partly reflect this overlap rather than an independent effect. No causal experiment exists in this notebook.

## Next steps
Planned future work includes constructing earlier feature windows, evaluating later outcome periods, and testing generalization to held-out clients not seen during task framing.

Source: work/notebooks/w02_ml_task_framing.ipynb
