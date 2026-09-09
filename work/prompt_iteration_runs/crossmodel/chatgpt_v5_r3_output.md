## Abstract

This report summarizes FL-01 Target Task 3: task framing and a descriptive fixed-rule baseline for prioritizing FlyRank content refreshes. The executed notebook analyzed 30,000 anonymized pages from 32 clients, with one row per page. The work was completed with AI assistance and did not include model training. Results do not justify the current rule over random selection, but they identify requirements for further modeling and evaluation.

## Methodology

Eligibility required `impressions_90d >= 100` and `impressions_prev_30d > 0`, leaving 21,758 pages. The proxy label was `is_declining_proxy = (trend_direction == "down")`; “down” denotes a greater-than-20% impression fall between consecutive 30-day windows.

Assuming capacity to review 50 pages per cycle, the fixed rule prioritized pages last updated at least 90 days ago, then sorted them by descending `impressions_90d`. Direct label fields were excluded from working signals. Missing values and page-ID uniqueness were checked, with executed outputs saved.

## Results

Of the eligible pages, 13,152 were proxy-positive, giving a prevalence—and uniform-random expected Precision@50—of 60.4%. The fixed rule retrieved 22 positives among its first 50.

| Method | Positives or expected positives at 50 | Precision@50 |
|---|---:|---:|
| Fixed prioritization rule | 22.0 | 44.0% |
| Uniform random selection | 30.2 expected | 60.4% expected |

The fixed rule was 16.4 percentage points below the random-selection expectation, corresponding to approximately 8.2 fewer positives per 50 reviewed pages.

## Discussion

The descriptive rule underperformed uniform random selection from the same eligible pool. This comparison does not explain the underperformance, prove that machine learning is necessary, or establish that refreshing selected pages would improve performance.

The evidence is limited by the absence of a learned model, held-out evaluation, an observed refresh-benefit outcome, and a causal experiment. Although direct label fields were excluded, retained 90-day metrics overlap the window used to define decline, so the notebook does not establish a clean prospective prediction design. Results across individual clients and generalization beyond these 32 clients remain unknown.

## Next steps

Further work should use earlier feature windows and later outcomes, define an observed refresh-benefit target, and evaluate on held-out clients. Any proposed intervention should subsequently be tested prospectively against an appropriate baseline, with causal claims reserved for a valid experiment.

Source: `work/notebooks/w02_ml_task_framing.ipynb`