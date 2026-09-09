# Capstone Report — Content Refresh Priority Ranking

- **Author:** Kerem Özcan
- **Lane:** Content Refresh Priority Ranking (ranking lane)
- **Repo:** [KeremOzcn/flyrank-ml-internship-submission](https://github.com/KeremOzcn/flyrank-ml-internship-submission)
- **Date:** September 9, 2026

> Built on the [FlyRank ML Internship](https://flyrank.ai) dataset. All data is anonymized — no client names, URLs, titles, or keywords appear in this report or in any committed file.

---

## 0. Abstract

Which pages should an editor review first for a possible content refresh? I framed this as a ranking problem on 30,000 anonymized content pages from 32 pseudonymized clients, using observed impression decline as a proxy for review relevance. A transparent stale-first baseline reached Precision@50 = 24.0% on the starter pipeline's client-holdout split — below the 54.2% positive-class base rate, meaning the rule is worse than random at finding declining pages. A random forest trained on 52 leak-free features reached Precision@50 = 74.0% on the same split, a 3.1× lift over the baseline and 19.8 percentage points above base rate. The output is a ranked review queue with reason codes, not a publishing decision — an editor still inspects each page before acting. The pipeline is reproducible from a fresh clone with `python scripts/run_all.py`.

---

## 1. Problem framing

**Decision:** Which pages should an editor inspect first for a possible content refresh, given limited review capacity?

**Unit of analysis:** One content page (one row per page in the dataset).

**Output:** A ranked review queue. Each page gets a priority score (0–100), a model probability, an action label (`refresh`, `refresh_and_review_ctr`, `refresh_and_review_engagement`, `expand_and_refresh`, `monitor`), and human-readable reason codes.

**Action a human takes:** An editor works down the ranked queue, inspecting each page's content, checking whether facts are current, coverage is adequate, and metadata is accurate, then deciding whether to update, expand, or leave the page alone.

**Cost of a wrong call:**
- *False positive (page flagged but not declining):* editor wastes review time on a page that didn't need attention.
- *False negative (page declining but not flagged):* a declining page goes unreviewed, potentially losing search traffic.

**Why data/ML helps:** 30,000 pages is too many for a human to review manually. A ranking model that prioritizes pages with observed decline signals — while respecting a strict data contract — lets the editor spend their 50 review slots on the pages most likely to need attention.

---

## 2. Data safety

**Data used:** `data/raw/content_refresh_anonymized.csv` — 30,000 rows × 44 columns, 32 pseudonymized clients. Bundled with the starter repo.

**Columns deliberately excluded as features:**

| Column(s) | Reason for exclusion |
|---|---|
| `trend_direction`, `trend_pct` | **Label-derived.** The target `is_declining_label` is defined as `trend_direction == "down"`. Including these would be direct label leakage. |
| `content_id`, `client_id` | **Pseudonymous IDs.** Used for grouping (client-holdout split) and joins only — never as features. Encoding them would let the model memorize client-specific outcomes. |
| `provider_used`, `model_used` | LLM provider/model that generated the article. Not a content quality signal; including it could introduce provider bias unrelated to refresh need. |
| `impressions_90d`, `clicks_90d`, `pageviews_90d`, `sessions_90d`, `users_90d`, `engaged_sessions_90d` | **Raw totals** replaced by log-transformed versions (`log_impressions_90d`, etc.) to compress scale and reduce outlier dominance. Not leakage, but redundant with their log forms. |

**Leakage risks considered:**
- **Label-derived fields:** `trend_direction` and `trend_pct` define the label. Verified they are not in the feature list (`scripts/01_prepare_features.py` excludes them explicitly).
- **Trend window overlap:** The 90-day activity metrics overlap with the trend comparison window. Removing `trend_pct` alone does not make this a clean future-prediction experiment — the activity columns carry information from the same window used to define decline. This is documented as a limitation (§6).
- **Client grouping:** Train/test split is grouped by client (`client_holdout`), so no client appears in both train and test. This prevents the model from learning client-specific patterns and testing on the same clients.

**Nothing client-identifying appears in `work/`:** No client names, URLs, domains, titles, or keywords. The dataset is anonymized at source. Confirmed by inspecting every committed file in `work/`.

---

## 3. Baseline

**Rule:** Stale-first — sort by `days_since_last_update` descending, then by `impressions_90d` descending. The oldest, most-visible pages come first.

**Why it's a fair comparison:** It's the rule a content team would naturally build without ML: "review the oldest popular pages first." It uses two signals available before any model, and it produces a total ordering that can be evaluated at Precision@K.

**Numbers (same split, same metric as the model):**

| Metric | Baseline | Random selection expectation |
|---|---|---|
| Precision@50 | 0.240 | 0.542 (positive-class rate) |
| Precision@100 | 0.360 | 0.542 |
| Precision@20 | 0.150 | 0.542 |
| ROC AUC | 0.627 | 0.500 |

The baseline is below the base rate at every K. Sorting by staleness + visibility is worse than random at finding declining pages in this dataset.

**My own notebook's measurement (on the 21,758-page eligible slice with ≥100 impressions):**

| Metric | Stale-first rule | Random expectation |
|---|---|---|
| Precision@50 | 44.0% (22/50) | 60.4% (13,152/21,758) |

The stale-first rule lost to chance by 16.4 percentage points on my filtered slice. This is a different slice than the full 30,000-row pipeline (which includes all pages), but the direction is the same: staleness alone is a weak signal for decline.

---

## 4. Model / analysis

**Method:** Random forest classifier, selected by Precision@50 on the client-holdout split.

**Why it fits the lane:** The content refresh problem is tabular data with mixed numeric and categorical features, non-linear interactions, and no need for sequence modeling or deep representations. Random forests handle mixed types, capture interactions without explicit feature engineering, and produce feature importances that support interpretation. A logistic regression was also trained as a linear baseline; the forest outperformed it.

**Feature list (52 features):**

*Numeric (18):* `search_volume`, `competition`, `cpc`, `word_count`, `char_count`, `log_impressions_90d`, `log_clicks_90d`, `log_sessions_90d`, `log_ai_sessions_90d`, `days_with_impressions`, `days_with_sessions`, `content_age_days`, `days_since_last_update`, `ctr`, `avg_position`, `engagement_rate`, `scroll_rate`, `ai_traffic_pct`

*Categorical (8, one-hot encoded):* `competition_level`, `content_type`, `main_intent`, `age_tier`, `freshness_tier`, `word_count_tier`, `impression_tier`, `position_tier`

**Left out on purpose:** `trend_direction`, `trend_pct` (label-derived), `content_id`, `client_id` (IDs), raw totals (replaced by log versions), `provider_used`, `model_used` (not quality signals).

**Target / proxy definition:** `is_declining_label = (trend_direction == "down")`. A page is "declining" if its impressions fell by more than 20% between two 30-day windows. This is a proxy for review relevance — it is not proof that the page needs a refresh, only that its search visibility dropped.

**Other models trained:**

| Model | Precision@50 | ROC AUC |
|---|---|---|
| Logistic regression | 0.400 | 0.700 |
| Decision tree | 0.540 | 0.742 |
| Random forest (selected) | 0.740 | 0.750 |

---

## 5. Evaluation

**Split:** Client-holdout. 80% of clients (≈27,675 rows) for training, 20% (≈2,325 rows) for testing. No client appears in both sets. This simulates deploying the model on a new client's pages — the honest generalization test.

**Why not a random split:** A random split would leak client-specific patterns. The model could memorize that "client_abc123 tends to decline" and exploit that at test time. Client-holdout prevents this.

**Why not a time-based split:** The dataset is a single snapshot (90-day trailing window). There is no temporal dimension to split on.

**Metrics (model vs baseline, same split):**

| Metric | Baseline (stale-first) | Logistic Reg | Decision Tree | Random Forest |
|---|---|---|---|---|
| Precision@50 | 0.240 | 0.400 | 0.540 | **0.740** |
| Precision@100 | 0.360 | 0.440 | 0.530 | **0.720** |
| Precision@20 | 0.150 | 0.350 | 0.500 | **0.650** |
| ROC AUC | 0.627 | 0.700 | 0.742 | **0.750** |
| Average precision | 0.468 | 0.522 | 0.575 | **0.618** |
| F1 | — | 0.566 | 0.634 | **0.640** |
| Recall | — | 0.567 | 0.716 | **0.744** |

**Base rate:** 54.2% of pages are labeled declining. A model that predicted "declining" for every page would get 54.2% precision. The random forest's 74.0% Precision@50 is 19.8 percentage points above base rate — the honest discrimination number.

**Error analysis:** The model's main failure mode is over-flagging high-impression pages with low CTR as "needs refresh" when the low CTR may be structural (e.g., branded queries with high volume but low click intent). The reason codes `low_ctr_visible_page` and `low_engagement_visible_page` appear frequently in the top-ranked items, which is expected — the model correctly identifies these as review candidates, but not every low-CTR page needs a content refresh; some need metadata or intent alignment instead.

---

## 6. Interpretation

**What the model found (top feature importances):**

1. **`days_with_impressions` (0.158)** — Pages with more days of impression activity are more likely to be flagged. This makes sense: pages with sustained visibility have more to lose from decline.
2. **`log_impressions_90d` (0.128)** — Higher-impression pages dominate the ranking. The model prioritizes pages where a refresh could recover meaningful traffic.
3. **`avg_position` (0.109)** — Pages deeper in search results are more likely to be flagged. Position is a strong decline signal — pages losing rank positions are losing visibility.
4. **`content_age_days` (0.095)** — Older content is more likely to need review, but this is not the dominant signal (it was 4th, not 1st). The stale-first baseline's failure confirms: age alone is insufficient.
5. **`char_count` / `word_count` (0.043 / 0.040)** — Content length has a small but non-zero contribution. Shorter pages may have less coverage to refresh.

**Surprises and negative results:**
- The stale-first baseline losing to chance was the most important finding. It overturned the assumption that "old = needs refresh" and justified the ML approach.
- `ai_traffic_pct` was a low-importance feature (not in top 10). AI-assisted traffic does not appear to be a strong signal for decline in this dataset.
- The logistic regression's Precision@50 (0.400) was below base rate (0.542), meaning a linear model barely improves on random selection. The non-linear interactions captured by the forest matter.

**Limitations:**
- The trend window overlaps with the 90-day activity metrics. This is not a clean future-prediction experiment — the model uses current-window signals to predict a current-window label. A true prospective evaluation would require a later outcome window not available in this dataset.
- The proxy (`trend_direction == "down"`) measures observed decline, not refresh need. A page may be declining for reasons a refresh cannot fix (algorithm change, seasonality, competitive shift).
- No held-out evaluation on a separately collected dataset has been performed. The client-holdout split is the strongest available generalization test, but it is not a prospective trial.

---

## 7. Recommendation

**Ranked actions the output supports:**

1. **Review high-confidence `refresh_and_review_ctr` items first.** These are pages the model flags as declining with demand, low CTR, and visible positions. They have the clearest opportunity: traffic exists but clicks are underperforming. Start with the top 50.
2. **Review `refresh` items next.** Declining pages without a specific CTR or engagement flag — the model believes they're declining but doesn't point to a specific cause. Manual inspection needed.
3. **Review `refresh_and_review_engagement` items for content quality.** These pages have traffic but low engagement (scroll rate, session duration). The content may be thin or mismatched to visitor intent.
4. **Monitor `monitor` items.** The model scored these low — no action needed now, but worth tracking in the next cycle.

**How a FlyRank editor would use this tomorrow:**
- Open `outputs/refresh_queue.csv`, sorted by score descending.
- Take the top 50 rows (one review cycle's capacity).
- For each row, inspect the page, check the reason codes, and decide: update facts, expand coverage, revise metadata, or leave alone.
- Track which recommended actions improved traffic over the next 30 days — this builds the editor-reviewed label set that a future model iteration should train on.

**Confidence:** Moderate. The model clearly outperforms the baseline and base rate on the client-holdout split, but the trend-window overlap means this is decision-support, not prospective prediction. The recommendations are directional, not prescriptive.

**Limits:** Do not use this model to claim "this page will recover traffic if refreshed." The model ranks review priority — it does not measure refresh outcomes. No causal experiment was conducted.

---

## 8. Reproducibility

**Fresh clone to results:**

```bash
git clone https://github.com/KeremOzcn/flyrank-ml-internship-submission.git
cd flyrank-ml-internship-submission
pip install -r requirements.txt
python scripts/run_all.py
```

This runs the full pipeline: `01_prepare_features.py` → `02_baseline_score.py` → `03_train_model.py` → `04_evaluate_and_export.py` → `05_build_pdf_report.py`.

**Outputs produced:**
- `outputs/model_results.json` — all metrics, feature importances, model comparison
- `outputs/refresh_queue.csv` — ranked review queue with scores, actions, reason codes
- `outputs/model_report.md` — Markdown summary
- `outputs/charts/*.svg` — 5 charts (feature importance, action mix, confidence mix, reason codes, trend distribution)
- `outputs/flyrank_refresh_model_results.pdf` — PDF report

**Environment:**
- Python 3.11+
- Key dependencies: `pandas`, `scikit-learn`, `matplotlib`, `numpy` (see `requirements.txt`)
- No GPU required

**Random seeds:** Set in `scripts/03_train_model.py` (`random_state=42` for all models). Re-runs produce identical results.

**Split verification:** The client-holdout split is built in `scripts/01_prepare_features.py`. The training and test client sets are logged in `outputs/model_results.json` under `split_strategy: "client_holdout"`. Train rows: 27,675. Test rows: 2,325.

**Claims traceability:** Every number in this report comes from `outputs/model_results.json` or `outputs/summary.json`, both committed to the repo. To verify any metric, run `python scripts/run_all.py` and diff the output.

---

## 9. Acknowledgments & data credit

Built on the [FlyRank ML Internship](https://flyrank.ai) dataset — 30,000 anonymized content pages across 32 pseudonymized clients. The dataset, pipeline skeleton, and evaluation framework were provided by the FlyRank internship program. All analysis, framing decisions, and conclusions in this report are my own.

Data source: [FlyRank](https://flyrank.ai) · Dataset: `content_refresh_anonymized.csv` (bundled, MIT-licensed code) · Data use governed by [DATA_USE.md](../DATA_USE.md).

---

## Claims checklist

- [x] All claims are **observed / measured / directional / decision-support** — no causal claims
- [x] No "predicted Google's algorithm" — the model ranks review priority, not search rankings
- [x] Base rate (54.2%) reported alongside all Precision@K numbers
- [x] Lift over baseline (3.1× at Precision@50) and lift over base rate (+19.8pp) both reported
- [x] No client-identifying details in any committed file
- [x] Numbers match `outputs/model_results.json` — verifiable by re-running `scripts/run_all.py`
- [x] Limitations stated explicitly (trend-window overlap, proxy not outcome, no prospective trial)
- [x] Acknowledgments section links to FlyRank