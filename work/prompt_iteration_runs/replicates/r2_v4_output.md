# FlyRank Content-Refresh Notebook: Research Report

## Abstract

This report summarizes a task-framing and baseline-analysis notebook (not model training) evaluating a fixed-rule prioritization heuristic for identifying declining pages among 30,000 anonymized pages across 32 clients. The rule underperforms uniform random selection on the same eligible pool, indicating no evidence yet supports the value of a learned model or intervention.

## Methodology

The dataset contains one row per page (30,000 total). Eligibility filters (impressions_90d >= 100 and impressions_prev_30d > 0) reduced the pool to 21,758 pages. A proxy label, is_declining_proxy, marks pages where trend_direction == "down" (a >20% impression drop between consecutive 30-day windows); 13,152 eligible pages are proxy-positive. Assuming a review capacity of 50 pages per cycle, a fixed rule was constructed: sort pages last updated ≥90 days ago first, then by impressions_90d descending. Precision@50 was compared against the expected precision of uniform random selection from the same eligible slice. Direct label fields were excluded from working signals, though retained 90-day metrics overlap the decline window. Missing values and page-ID uniqueness were checked; executed outputs were saved.

## Results

| Method | Positives (or expected) at 50 | Precision@50 |
|---|---|---|
| Fixed rule (staleness + impressions) | 22 | 44% |
| Uniform random (expected) | ~30.2 | ~60.4% |

The fixed rule identifies fewer positives in its top 50 than random selection would be expected to yield from the same 21,758-page pool with 13,152 proxy-positives.

## Discussion

The fixed rule's Precision@50 (44%) falls below the random-selection baseline (~60.4%) on this proxy label. This gap does not explain the underperformance's cause, does not demonstrate that a learned model would do better, and does not establish any causal or observed refresh benefit—no such experiment was run. The proxy label itself is heuristic (a >20% consecutive-window drop) and retained 90-day metrics overlap the decline-detection window, which may introduce leakage-like artifacts not yet assessed. No held-out evaluation exists. These results describe one framing and one baseline on one dataset snapshot; they do not generalize beyond it.

## Next steps

Future work includes earlier feature windows, later outcome measurement, held-out client evaluation, and formal assessment of label-window overlap before any modeling claims are made.

**Source:** work/notebooks/w02_ml_task_framing.ipynb
