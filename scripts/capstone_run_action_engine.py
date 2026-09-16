#!/usr/bin/env python3
"""Capstone action engine — builds ranked refresh queue with reason codes and actions."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = ROOT / 'data' / 'processed'
OUTPUT_DIR = ROOT / 'outputs'
CHART_DIR = OUTPUT_DIR / 'charts'

df = pd.read_csv(PROCESSED_DIR / 'capstone_feature_vector.csv')
preds = pd.read_csv(PROCESSED_DIR / 'capstone_predictions.csv')
results = json.loads((OUTPUT_DIR / 'capstone_model_results.json').read_text())

print(f'Feature vector: {df.shape}')
print(f'Predictions: {preds.shape}')


def compute_reason_codes(row):
    reasons = []
    prob = row.get('model_probability', row.get('prob', 0))
    if prob >= 0.65:
        reasons.append('model_decline_risk')
    if row['impressions_90d'] >= 500 and prob >= 0.5:
        reasons.append('high_visibility_declining')
    if row['impressions_90d'] >= 100 and row.get('avg_position', 0) > 0 and row['avg_position'] <= 20 and row.get('ctr', 0) < 0.5:
        reasons.append('low_ctr_visible_position')
    if row.get('sessions_90d', 0) >= 30 and row.get('engagement_rate', 0) < 30 and row.get('engagement_rate', 0) > 0:
        reasons.append('low_engagement_with_traffic')
    if row.get('is_very_stale', 0) == 1:
        reasons.append('old_content_losing_position')
    elif row.get('is_stale', 0) == 1:
        reasons.append('stale_content')
    wc = row.get('word_count', 0)
    if wc and wc > 0 and wc < 1000 and row['impressions_90d'] >= 100:
        reasons.append('thin_content_visible')
    if prob < 0.3 and row['impressions_90d'] >= 500:
        reasons.append('growing_page_protect')
    if 0.3 <= prob < 0.5 and row['impressions_90d'] >= 100:
        reasons.append('stable_page_monitor')
    return '|'.join(reasons) if reasons else 'general_review'


def suggest_action(reason_codes_str):
    reasons = set(reason_codes_str.split('|'))
    if 'thin_content_visible' in reasons:
        return 'expand_and_refresh'
    if 'growing_page_protect' in reasons:
        return 'protect'
    if 'stable_page_monitor' in reasons and not reasons.intersection({'model_decline_risk', 'high_visibility_declining'}):
        return 'monitor'
    if 'low_ctr_visible_position' in reasons and 'low_engagement_with_traffic' in reasons:
        return 'refresh_and_review_engagement'
    if 'low_ctr_visible_position' in reasons:
        return 'refresh_and_review_ctr'
    if 'low_engagement_with_traffic' in reasons:
        return 'refresh_and_review_engagement'
    if reasons.intersection({'model_decline_risk', 'high_visibility_declining', 'old_content_losing_position'}):
        return 'refresh'
    if 'stale_content' in reasons:
        return 'refresh'
    return 'monitor'


def compute_priority_score(row):
    score = row.get('model_probability', row.get('prob', 0)) * 50
    imp = row['impressions_90d']
    if imp >= 10000:
        score += 20
    elif imp >= 1000:
        score += 12
    elif imp >= 100:
        score += 6
    if row.get('is_very_stale', 0) == 1:
        score += 12
    elif row.get('is_stale', 0) == 1:
        score += 6
    pos = row.get('avg_position', 0)
    if pos > 0 and pos <= 10:
        score += 8
    elif pos > 0 and pos <= 20:
        score += 4
    if imp >= 100 and row.get('ctr', 0) < 0.5 and pos > 0 and pos <= 20:
        score += 6
    return float(np.clip(score, 0, 100))


def confidence_label(score, prob, impressions):
    if score >= 65 and prob >= 0.5 and impressions >= 500:
        return 'high'
    if score >= 40:
        return 'medium'
    return 'low'


# Build queue
queue = preds.rename(columns={'prob': 'model_probability', 'pred': 'model_pred'})

feature_cols = ['content_id', 'client_id', 'impressions_90d', 'clicks_90d', 'sessions_90d',
                'pageviews_90d', 'ctr', 'avg_position', 'engagement_rate', 'scroll_rate',
                'content_age_days', 'days_since_last_update', 'word_count',
                'content_type', 'is_stale', 'is_very_stale', 'has_position', 'is_top10', 'is_top3']
feature_cols = [c for c in feature_cols if c in df.columns]

queue = queue.merge(df[feature_cols], on='content_id', how='left', suffixes=('', '_feat'))

queue['reason_codes'] = queue.apply(compute_reason_codes, axis=1)
queue['suggested_action'] = queue['reason_codes'].apply(suggest_action)
queue['priority_score'] = queue.apply(compute_priority_score, axis=1)
queue['confidence'] = queue.apply(
    lambda r: confidence_label(r['priority_score'], r['model_probability'], r['impressions_90d']),
    axis=1,
)

queue = queue.sort_values('priority_score', ascending=False).reset_index(drop=True)
queue['rank'] = queue.index + 1

print(f'\nQueue size: {len(queue):,}')
print(f'\nAction distribution:')
print(queue['suggested_action'].value_counts())
print(f'\nConfidence distribution:')
print(queue['confidence'].value_counts())

# Charts
fig, axes = plt.subplots(1, 3, figsize=(20, 6))

action_counts = queue['suggested_action'].value_counts()
action_colors = ['#E74C3C', '#E67E22', '#F39C12', '#27AE60', '#3498DB', '#9B59B6', '#95A5A6', '#1ABC9C']
axes[0].barh(action_counts.index[::-1], action_counts.values[::-1], color=action_colors[:len(action_counts)][::-1])
axes[0].set_title('Suggested Action Distribution')
axes[0].set_xlabel('Count')
for i, v in enumerate(action_counts.values[::-1]):
    axes[0].text(v + 20, i, f'{v:,}', va='center', fontsize=9)

conf_counts = queue['confidence'].value_counts().reindex(['high', 'medium', 'low'], fill_value=0)
axes[1].bar(conf_counts.index, conf_counts.values, color=['#E74C3C', '#F39C12', '#95A5A6'])
axes[1].set_title('Confidence Distribution')
axes[1].set_ylabel('Count')

reason_counts = {}
for rc in queue['reason_codes']:
    for r in str(rc).split('|'):
        reason_counts[r] = reason_counts.get(r, 0) + 1
top_reasons = pd.Series(reason_counts).sort_values(ascending=False).head(12)
axes[2].barh(top_reasons.index[::-1], top_reasons.values[::-1], color='#6F4E7C')
axes[2].set_title('Top Reason Codes')
axes[2].set_xlabel('Count')

plt.tight_layout()
plt.savefig(CHART_DIR / 'action_engine_distribution.png', bbox_inches='tight', dpi=150)
plt.close()

# Export
export_cols = ['rank', 'content_id', 'client_id', 'priority_score', 'model_probability',
               'suggested_action', 'confidence', 'reason_codes',
               'impressions_90d', 'ctr', 'avg_position', 'content_age_days',
               'days_since_last_update', 'content_type', 'is_declining']
export_cols = [c for c in export_cols if c in queue.columns]

full_queue_path = OUTPUT_DIR / 'capstone_refresh_queue.csv'
queue[export_cols].to_csv(full_queue_path, index=False)
print(f'\nFull queue: {full_queue_path} ({len(queue):,} rows)')

top50_path = OUTPUT_DIR / 'capstone_refresh_queue_top50.csv'
queue[export_cols].head(50).to_csv(top50_path, index=False)
print(f'Top 50: {top50_path}')

top100_path = OUTPUT_DIR / 'capstone_refresh_queue_top100.csv'
queue[export_cols].head(100).to_csv(top100_path, index=False)
print(f'Top 100: {top100_path}')

# Save summary
action_summary = {
    'total_pages_scored': int(len(queue)),
    'action_distribution': {k: int(v) for k, v in queue['suggested_action'].value_counts().items()},
    'confidence_distribution': {k: int(v) for k, v in queue['confidence'].value_counts().items()},
    'top_reason_codes': {k: int(v) for k, v in top_reasons.items()},
    'priority_score_stats': {
        'mean': float(queue['priority_score'].mean()),
        'median': float(queue['priority_score'].median()),
        'p80': float(queue['priority_score'].quantile(0.8)),
        'max': float(queue['priority_score'].max()),
    },
    'high_confidence_count': int((queue['confidence'] == 'high').sum()),
    'outputs': {
        'full_queue': str(full_queue_path),
        'top50': str(top50_path),
        'top100': str(top100_path),
    },
}

summary_path = OUTPUT_DIR / 'capstone_action_summary.json'
summary_path.write_text(json.dumps(action_summary, indent=2))
print(f'Saved: {summary_path}')

print(f'\n--- Top 10 Queue ---')
display_cols = ['rank', 'priority_score', 'model_probability', 'suggested_action', 'reason_codes', 'impressions_90d']
display_cols = [c for c in display_cols if c in queue.columns]
print(queue[display_cols].head(10).to_string(index=False))

print('\n✓ Action engine complete')