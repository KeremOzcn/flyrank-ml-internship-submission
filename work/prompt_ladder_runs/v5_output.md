## The problem

During my FlyRank internship, I framed content-refresh prioritization as a ranking problem: choose 50 pages per review cycle from 30,000 anonymized pages across 32 clients. The eligible slice contained 21,758 pages with `impressions_90d >= 100` and `impressions_prev_30d > 0`. Because no observed refresh-benefit outcomes were available, I used a binary proxy: `is_declining_proxy = (trend_direction == "down")`, where “down” means impressions fell by more than 20% between consecutive 30-day windows.

## What I did and decided

With AI assistance, I built an executed task-framing notebook that checks missing values and page-ID uniqueness, defines the eligible population and proxy label, and evaluates a fixed prioritization rule. The rule ranks pages last updated at least 90 days ago first, then sorts by `impressions_90d` descending. Direct label fields were excluded from working signals, while documenting that retained 90-day metrics overlap the decline window. No model was trained.

## What came of it

The rule returned 22 proxy-positive pages in its top 50, giving Precision@50 of 44%. Uniform random selection from the same eligible slice has expected Precision@50 of 60.4%. These are full-slice descriptive results, not held-out model evaluation, and they neither measure refresh benefit nor demonstrate business impact. The result establishes a transparent baseline and exposes the need for better study design: earlier feature windows, later outcomes, and held-out clients—without treating temporal or client-held-out evaluation alone as causal evidence that refreshing improves performance.

Artifact: `work/notebooks/w02_ml_task_framing.ipynb`