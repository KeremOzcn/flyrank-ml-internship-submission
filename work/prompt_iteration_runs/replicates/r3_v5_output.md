# Abstract
This report summarizes a completed task-framing and descriptive-baseline exercise for the FlyRank content-refresh notebook, developed with AI assistance. No model was trained, no held-out evaluation was performed, and no causal or refresh-benefit outcome was observed. The notebook establishes an eligibility-filtered dataset, a proxy decline label, and a fixed-rule prioritization baseline, then compares it to uniform random selection under an assumed 50-page review capacity.

# Methodology
The source dataset contains 30,000 anonymized pages across 32 clients (one row per page). Eligibility requires impressions_90d ≥ 100 and impressions_prev_30d > 0, yielding 21,758 eligible pages. The proxy label is_declining_proxy = (trend_direction == "down"), where "down" denotes a >20% impression drop between consecutive 30-day windows; 13,152 eligible pages are proxy-positive. The fixed rule sorts pages last updated ≥90 days ago first, then by impressions_90d descending, selecting the top 50 under an assumed 50-page review capacity. Direct label fields were excluded from working signals, though retained 90-day metrics overlap the decline window. Missing values and page-ID uniqueness were checked; executed outputs were saved.

# Results
| Method | Positives at 50 | Precision@50 |
|---|---|---|
| Fixed rule | 22 of 50 | 44.0% |
| Random (expected) | 30.2 of 50 | 60.4% (13,152/21,758) |

The fixed rule identifies 22 proxy-positive pages in its top 50 (44%), roughly 16.4 percentage points below the 60.4% expected under uniform random selection from the same eligible pool.

# Discussion
This gap shows the fixed rule underperforms random selection on the proxy label within this notebook; it does not explain the cause, does not establish that a learned model would perform better, and does not demonstrate any refresh-benefit outcome, since no intervention or causal experiment was run. The overlap between retained 90-day metrics and the decline-window definition is a noted limitation that has not been resolved. No held-out evaluation exists, so generalization to unseen clients or time periods is unknown.

# Next steps
Planned future work includes constructing features from earlier windows, evaluating against later outcome periods, and testing on held-out clients to assess generalization before considering model training.

Source: work/notebooks/w02_ml_task_framing.ipynb
