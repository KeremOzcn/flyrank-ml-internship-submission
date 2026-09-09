# FlyRank Content-Refresh: Task Framing & Baseline Report

## Abstract

This report summarizes a completed task-framing notebook for FlyRank's content-refresh prioritization problem, produced with AI assistance. The work defines an eligibility filter, a proxy label for declining pages, and a fixed-rule baseline for selecting pages under a 50-page review capacity. No model was trained, and no held-out evaluation or causal outcome was measured.

## Methodology

From 30,000 anonymized pages across 32 clients (one row per page), eligibility required impressions_90d ≥ 100 and impressions_prev_30d > 0, yielding 21,758 pages. A proxy label, is_declining_proxy, was defined as trend_direction == "down," where "down" indicates a greater-than-20% impression drop between consecutive 30-day windows; 13,152 eligible pages are proxy-positive. The fixed rule ranks pages last updated ≥90 days ago first, then sorts by impressions_90d descending, selecting the top 50. Direct label fields were excluded from working signals, though retained 90-day metrics overlap the decline window. Missing values and page-ID uniqueness were checked; outputs were executed and saved.

## Results

| Method | Positives (or expected) at 50 | Precision@50 |
|---|---|---|
| Fixed rule (staleness → impressions) | 22 | 44.0% |
| Uniform random (same eligible slice) | ~30.2 (13,152/21,758 × 50) | ~60.4% |

The fixed rule's Precision@50 (44%) falls below the random-selection expectation (~60.4%) for the same eligible pool.

## Discussion

This gap does not establish that the rule is harmful, that a learned model would outperform it, or that any refresh intervention produces measurable benefit. The proxy label uses retained 90-day metrics that overlap the decline-detection window, which may bias comparisons; this was not adjusted for. No held-out clients, earlier feature windows, or causal outcomes were evaluated. As in prior work, a rule underperforming a random baseline on a labeled proxy does not by itself justify further modeling or an intervention.

## Next steps

Future work includes constructing features from earlier windows, evaluating against later outcome windows, holding out clients for generalization checks, and designing an outcome-linked or causal evaluation of refresh benefit.

**Source:** work/notebooks/w02_ml_task_framing.ipynb
