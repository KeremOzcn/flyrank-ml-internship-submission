## Content-refresh prioritization at FlyRank

During my FlyRank internship, I developed this task-framing notebook with AI assistance to examine how pages might be prioritized for editorial review.

### Problem

The starter dataset contains 30,000 anonymized content pages from 32 clients, with one row per page. The operational framing assumes a review capacity of 50 pages per cycle.

Because the dataset contains no observed outcomes showing whether refreshing a page improved its performance, the notebook does not train or evaluate a refresh-benefit model. Instead, it defines a descriptive ranking task using a decline proxy.

The eligible population consists of 21,758 pages satisfying:

- `impressions_90d >= 100`
- `impressions_prev_30d > 0`

Binary relevance is defined as:

```text
is_declining_proxy = (trend_direction == "down")
```

Here, `down` indicates a greater-than-20% fall in impressions between consecutive 30-day windows.

### Approach

I evaluated a fixed prioritization rule that:

1. Places pages last updated at least 90 days ago first.
2. Sorts pages within that ordering by `impressions_90d` descending.

The evaluation metric is Precision@50, matching the assumed editorial capacity. I also calculated the expected Precision@50 of uniform random selection from the same eligible slice to provide a prevalence-based reference point.

The notebook checks missing values and page-ID uniqueness and saves its executed outputs. Direct label fields are excluded from the working signals. However, the retained 90-day metrics overlap the time window used to define the decline proxy, so the setup should not be interpreted as temporally clean prediction.

### Result

The fixed rule identifies 22 proxy-positive pages among its first 50 recommendations:

```text
Precision@50 = 22 / 50 = 44.0%
```

Uniform random selection from the same eligible population has an expected Precision@50 of 60.4%.

These figures are full-slice descriptive results—not held-out model performance. No model was trained, no refresh outcomes were available, and the notebook does not demonstrate business impact or the causal effect of refreshing selected pages.

### What this established

The notebook turns an underspecified content-refresh request into an explicit ranking problem with a defined eligible population, review budget, proxy label, baseline rule, metric, and key validity limitations. It also shows that the proposed fixed rule does not improve on the random-selection expectation under this proxy-based framing.

A stronger follow-up study would construct features from earlier windows, measure outcomes in later periods, and evaluate generalization on held-out clients. Even with temporal and client-held-out evaluation, a separate causal design would still be required to establish whether refreshing a selected page causes an improvement.

Artifact: `work/notebooks/w02_ml_task_framing.ipynb`