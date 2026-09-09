## Abstract

This report summarizes FL-01 Target Task 3: task framing and a descriptive fixed-rule baseline for prioritizing FlyRank content refreshes. The executed notebook analyzed 30,000 anonymized pages from 32 clients, with one row per page. The work was completed with AI assistance and did not involve model training. The baseline underperformed uniform random selection, so the available results do not justify claiming predictive value or refresh benefit.

## Methodology

Eligibility required `impressions_90d >= 100` and `impressions_prev_30d > 0`, leaving 21,758 pages. The proxy label `is_declining_proxy` equals `trend_direction == "down"`; “down” denotes a greater-than-20% impression fall between consecutive 30-day windows. Among eligible pages, 13,152 were proxy-positive.

Assuming capacity to review 50 pages per cycle, the fixed rule ranked pages last updated at least 90 days ago first, then by descending `impressions_90d`. Direct label fields were excluded from working signals.

## Results

| Method | Positives or expected positives at 50 | Precision@50 |
|---|---:|---:|
| Fixed prioritization rule | 22 | 44.0% |
| Uniform random selection from eligible pages | 30.2 expected | 60.4% expected |

The fixed rule’s Precision@50 was 22/50 = 44.0%. Eligible prevalence was 13,152/21,758 ≈ 60.4%, corresponding to 30.2 expected positives in 50 random selections. The rule was therefore approximately 16.4 percentage points below the random-selection expectation.

## Discussion

The fixed rule did not improve proxy-positive concentration relative to random selection from the same eligible pool. This comparison does not explain the underperformance, prove that machine learning is necessary, or establish that refreshing selected pages would improve performance.

There was no learned model, held-out evaluation, observed refresh-benefit outcome, or causal experiment. Moreover, retained 90-day metrics overlap the window defining decline, limiting temporal separation between signals and the proxy. Missing values and page-ID uniqueness were checked, and executed outputs were saved; these checks do not establish generalization or causal validity.

## Next steps

Further modeling should use earlier feature windows and later observed outcomes, followed by evaluation on held-out clients. An intervention or causal design would be required to estimate whether refreshing prioritized pages produces benefit. Unknown information remains unknown.

Source: `work/notebooks/w02_ml_task_framing.ipynb`