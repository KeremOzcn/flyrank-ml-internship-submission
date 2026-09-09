## Abstract

This AI-assisted work frames content-refresh prioritization and evaluates a descriptive fixed-rule baseline on 30,000 anonymized pages from 32 clients. It does not train or validate an ML model. The rule achieved 44.0% Precision@50, below the eligible-pool prevalence of 60.4%, so these results do not justify further modeling without a stronger evaluation design and an observed refresh-benefit outcome.

## Methodology

The dataset contains one row per page. Eligibility required `impressions_90d >= 100` and `impressions_prev_30d > 0`, leaving 21,758 pages. The proxy label was `trend_direction == "down"`, where “down” represents a greater-than-20% impressions fall between consecutive 30-day windows.

Assuming capacity to review 50 pages per cycle, the fixed rule ranked pages last updated at least 90 days ago first, then by `impressions_90d` descending. Direct label fields were excluded from working signals, although retained 90-day metrics overlap the decline window. Missing values and page-ID uniqueness were checked, with executed outputs saved.

## Results

Among eligible pages, 13,152 were proxy-positive.

| Method | Positives or expected positives at 50 | Precision@50 |
|---|---:|---:|
| Fixed rule | 22 | 44.0% |
| Uniform random selection | 30.2 expected | 60.4% expected |

The rule’s Precision@50 was 16.4 percentage points below the random-selection expectation for the same eligible pool.

## Discussion

The fixed rule underperformed the pool-level random expectation at the stated review capacity. This comparison does not explain the underperformance or establish that ML is necessary. Because the notebook has no learned model, held-out evaluation, observed refresh-benefit outcome, or causal experiment, it provides no evidence of generalization or intervention benefit. Window overlap also limits interpretation of the proxy-based evaluation.

## Next steps

Define earlier feature windows and later outcomes, measure actual post-refresh benefit, and evaluate on held-out clients. Only then should learned approaches be compared with transparent rules and random selection under the same review capacity.

Source: `work/notebooks/w02_ml_task_framing.ipynb`