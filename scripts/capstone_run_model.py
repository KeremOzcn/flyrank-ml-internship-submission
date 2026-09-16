#!/usr/bin/env python3
"""Capstone model pipeline — trains 5 models with GroupKFold CV, evaluates, saves results."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.metrics import (
    roc_auc_score, average_precision_score, f1_score, precision_score,
    recall_score, brier_score_loss, confusion_matrix,
)
from sklearn.calibration import calibration_curve
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import xgboost as xgb
import lightgbm as lgb

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = ROOT / 'data' / 'processed'
OUTPUT_DIR = ROOT / 'outputs'
CHART_DIR = OUTPUT_DIR / 'charts'
CHART_DIR.mkdir(parents=True, exist_ok=True)

# --- Load ---
df = pd.read_csv(PROCESSED_DIR / 'capstone_feature_vector.csv')
config = json.loads((PROCESSED_DIR / 'capstone_feature_config.json').read_text())

NUMERIC_FEATURES = config['NUMERIC_FEATURES']
CATEGORICAL_FEATURES = config['CATEGORICAL_FEATURES']
LABEL = 'is_declining'

print(f'Loaded: {df.shape}, label positive rate: {df[LABEL].mean():.3f}')

# --- Build feature matrix ---
X_num = df[NUMERIC_FEATURES].apply(pd.to_numeric, errors='coerce').replace([np.inf, -np.inf], np.nan).fillna(0)
X_cat = pd.get_dummies(df[CATEGORICAL_FEATURES].fillna('unknown').astype(str), dummy_na=False, dtype=float)
X = pd.concat([X_num, X_cat], axis=1)
# Clean feature names for XGBoost (no [, ], <)
X.columns = [c.replace('[', '_').replace(']', '_').replace('<', '_').replace(' ', '_') for c in X.columns]
y = df[LABEL].values
groups = df['client_id'].values
feature_names = list(X.columns)

print(f'Feature matrix: {X.shape}')

# --- Client-holdout split ---
unique_clients = np.unique(groups)
rng = np.random.default_rng(RANDOM_SEED)
shuffled = rng.permutation(unique_clients)
n_test = max(1, int(round(len(shuffled) * 0.2)))
test_clients = set(shuffled[:n_test])

test_mask = np.array([c in test_clients for c in groups])
train_idx = np.where(~test_mask)[0]
test_idx = np.where(test_mask)[0]

X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
y_train, y_test = y[train_idx], y[test_idx]
groups_train = groups[train_idx]

print(f'Train: {len(train_idx):,} rows ({len(np.unique(groups_train))} clients)')
print(f'Test:  {len(test_idx):,} rows ({len(test_clients)} clients)')

# --- Models ---
models_config = {
    'logistic_regression': Pipeline([
        ('scaler', StandardScaler()),
        ('model', LogisticRegression(class_weight='balanced', max_iter=2000, random_state=RANDOM_SEED)),
    ]),
    'random_forest': RandomForestClassifier(
        n_estimators=300, max_depth=12, min_samples_leaf=20,
        class_weight='balanced_subsample', n_jobs=-1, random_state=RANDOM_SEED,
    ),
    'xgboost': xgb.XGBClassifier(
        n_estimators=300, max_depth=6, learning_rate=0.1,
        subsample=0.8, colsample_bytree=0.8,
        scale_pos_weight=(1 - y_train.mean()) / y_train.mean(),
        eval_metric='aucpr', random_state=RANDOM_SEED, n_jobs=-1,
    ),
    'lightgbm': lgb.LGBMClassifier(
        n_estimators=300, max_depth=8, learning_rate=0.1,
        subsample=0.8, colsample_bytree=0.8,
        class_weight='balanced', random_state=RANDOM_SEED, n_jobs=-1, verbose=-1,
    ),
    'extra_trees': ExtraTreesClassifier(
        n_estimators=300, max_depth=12, min_samples_leaf=20,
        class_weight='balanced', n_jobs=-1, random_state=RANDOM_SEED,
    ),
}


def precision_at_k(y_true, scores, k):
    idx = np.argsort(scores)[::-1][:k]
    return float(y_true[idx].mean()) if len(idx) > 0 else 0.0


def make_model(name):
    """Factory for fresh model instances (for CV)."""
    if name == 'logistic_regression':
        return Pipeline([('scaler', StandardScaler()), ('model', LogisticRegression(class_weight='balanced', max_iter=2000, random_state=RANDOM_SEED))])
    elif name == 'random_forest':
        return RandomForestClassifier(n_estimators=200, max_depth=10, min_samples_leaf=20, class_weight='balanced_subsample', n_jobs=-1, random_state=RANDOM_SEED)
    elif name == 'xgboost':
        return xgb.XGBClassifier(n_estimators=200, max_depth=6, learning_rate=0.1, subsample=0.8, colsample_bytree=0.8, scale_pos_weight=1.0, eval_metric='aucpr', random_state=RANDOM_SEED, n_jobs=-1)
    elif name == 'lightgbm':
        return lgb.LGBMClassifier(n_estimators=200, max_depth=8, learning_rate=0.1, subsample=0.8, colsample_bytree=0.8, class_weight='balanced', random_state=RANDOM_SEED, n_jobs=-1, verbose=-1)
    elif name == 'extra_trees':
        return ExtraTreesClassifier(n_estimators=200, max_depth=10, min_samples_leaf=20, class_weight='balanced', n_jobs=-1, random_state=RANDOM_SEED)
    raise ValueError(name)


# --- Train & evaluate ---
results = {}
predictions = {}

for name, model in models_config.items():
    print(f'\nTraining {name}...')
    model.fit(X_train, y_train)

    if hasattr(model, 'predict_proba'):
        probs = model.predict_proba(X_test)[:, 1]
    else:
        probs = model.decision_function(X_test)

    preds_bin = (probs >= 0.5).astype(int)

    metrics = {
        'roc_auc': float(roc_auc_score(y_test, probs)),
        'average_precision': float(average_precision_score(y_test, probs)),
        'f1': float(f1_score(y_test, preds_bin, zero_division=0)),
        'precision': float(precision_score(y_test, preds_bin, zero_division=0)),
        'recall': float(recall_score(y_test, preds_bin, zero_division=0)),
        'brier_score': float(brier_score_loss(y_test, probs)),
        'precision_at_20': precision_at_k(y_test, probs, 20),
        'precision_at_50': precision_at_k(y_test, probs, 50),
        'precision_at_100': precision_at_k(y_test, probs, 100),
    }

    # GroupKFold CV
    cv_aucs = []
    gkf = GroupKFold(n_splits=5)
    X_train_arr = X_train.values
    for tr, va in gkf.split(X_train_arr, y_train, groups_train):
        model_cv = make_model(name)
        if name == 'xgboost':
            spw = (1 - y_train[tr].mean()) / max(y_train[tr].mean(), 1e-6)
            model_cv = xgb.XGBClassifier(n_estimators=200, max_depth=6, learning_rate=0.1, subsample=0.8, colsample_bytree=0.8, scale_pos_weight=spw, eval_metric='aucpr', random_state=RANDOM_SEED, n_jobs=-1)
        model_cv.fit(X_train_arr[tr], y_train[tr])
        probs_cv = model_cv.predict_proba(X_train_arr[va])[:, 1] if hasattr(model_cv, 'predict_proba') else model_cv.decision_function(X_train_arr[va])
        cv_aucs.append(roc_auc_score(y_train[va], probs_cv))

    metrics['cv_roc_auc_mean'] = float(np.mean(cv_aucs))
    metrics['cv_roc_auc_std'] = float(np.std(cv_aucs))

    results[name] = metrics
    predictions[name] = probs

    print(f'  ROC AUC: {metrics["roc_auc"]:.3f} | AP: {metrics["average_precision"]:.3f} | P@50: {metrics["precision_at_50"]:.3f} | CV AUC: {metrics["cv_roc_auc_mean"]:.3f}±{metrics["cv_roc_auc_std"]:.3f}')

# --- Baselines ---
majority_probs = np.full_like(y_test, y_train.mean(), dtype=float)
rng2 = np.random.default_rng(RANDOM_SEED)
random_probs = rng2.uniform(0, 1, size=len(y_test))
stale_scores = X_test['is_stale'].values + X_test['is_very_stale'].values * 0.5 + X_test['content_age_days'].values / 500
stale_probs = (stale_scores - stale_scores.min()) / (stale_scores.max() - stale_scores.min() + 1e-10)

baselines = {
    'majority_class': {
        'roc_auc': 0.5, 'average_precision': float(y_test.mean()),
        'precision_at_50': float(y_test.mean()), 'precision_at_100': float(y_test.mean()),
        'f1': 0.0, 'recall': 0.0, 'brier_score': float(brier_score_loss(y_test, majority_probs)),
    },
    'random': {
        'roc_auc': float(roc_auc_score(y_test, random_probs)),
        'average_precision': float(average_precision_score(y_test, random_probs)),
        'precision_at_50': precision_at_k(y_test, random_probs, 50),
        'precision_at_100': precision_at_k(y_test, random_probs, 100),
        'f1': float(f1_score(y_test, (random_probs >= 0.5).astype(int), zero_division=0)),
        'recall': float(recall_score(y_test, (random_probs >= 0.5).astype(int), zero_division=0)),
        'brier_score': float(brier_score_loss(y_test, random_probs)),
    },
    'stale_first_rule': {
        'roc_auc': float(roc_auc_score(y_test, stale_probs)),
        'average_precision': float(average_precision_score(y_test, stale_probs)),
        'precision_at_50': precision_at_k(y_test, stale_probs, 50),
        'precision_at_100': precision_at_k(y_test, stale_probs, 100),
        'f1': float(f1_score(y_test, (stale_probs >= 0.5).astype(int), zero_division=0)),
        'recall': float(recall_score(y_test, (stale_probs >= 0.5).astype(int), zero_division=0)),
        'brier_score': float(brier_score_loss(y_test, stale_probs.clip(0, 1))),
    },
}

for bn, bm in baselines.items():
    print(f'{bn:20s} ROC AUC: {bm["roc_auc"]:.3f} | AP: {bm["average_precision"]:.3f} | P@50: {bm["precision_at_50"]:.3f}')

# --- Best model ---
best_name = max(results, key=lambda k: results[k]['average_precision'])
best_model = models_config[best_name]
best_probs = predictions[best_name]
best_preds = (best_probs >= 0.5).astype(int)

print(f'\n✓ Best model: {best_name}')
print(f'  ROC AUC: {results[best_name]["roc_auc"]:.4f}')
print(f'  Avg Precision: {results[best_name]["average_precision"]:.4f}')

# --- Feature importance ---
if hasattr(best_model, 'feature_importances_'):
    importances = best_model.feature_importances_
elif hasattr(best_model, 'named_steps') and hasattr(best_model.named_steps.get('model', None), 'coef_'):
    importances = np.abs(best_model.named_steps['model'].coef_[0])
else:
    importances = np.zeros(len(feature_names))

imp_df = pd.DataFrame({'feature': feature_names, 'importance': importances})
imp_df = imp_df.sort_values('importance', ascending=False).head(20)

# --- Charts ---
colors = ['#2A5D63', '#B4552F', '#6F4E7C', '#3498DB', '#E67E22']

# Model comparison
fig, axes = plt.subplots(1, 4, figsize=(20, 5))
metrics_to_plot = ['roc_auc', 'average_precision', 'precision_at_50', 'f1']
metric_labels = ['ROC AUC', 'Avg Precision', 'Precision@50', 'F1']
model_names = list(results.keys())

for ax, metric, label in zip(axes, metrics_to_plot, metric_labels):
    vals = [results[m][metric] for m in model_names]
    base_vals = [baselines['stale_first_rule'].get(metric, 0)] * len(model_names)
    x = np.arange(len(model_names))
    ax.bar(x - 0.15, vals, 0.3, color='#2A5D63', label='Model')
    ax.bar(x + 0.15, base_vals, 0.3, color='#B4552F', alpha=0.6, label='Stale Rule')
    ax.set_xticks(x)
    ax.set_xticklabels([m.replace('_', '\n') for m in model_names], fontsize=8)
    ax.set_title(label)
    ax.legend(fontsize=8)
    ax.set_ylim(0, max(max(vals), max(base_vals)) * 1.15)

plt.suptitle('Model Comparison vs Stale-First Baseline', fontsize=14, y=1.02)
plt.tight_layout()
plt.savefig(CHART_DIR / 'model_comparison.png', bbox_inches='tight', dpi=150)
plt.close()

# ROC curves
from sklearn.metrics import roc_curve
fig, ax = plt.subplots(figsize=(8, 7))
for (name, probs), color in zip(predictions.items(), colors):
    fpr, tpr, _ = roc_curve(y_test, probs)
    ax.plot(fpr, tpr, color=color, label=f'{name} ({results[name]["roc_auc"]:.3f})')
ax.plot([0, 1], [0, 1], 'k--', alpha=0.3, label='Random (0.500)')
ax.set_xlabel('False Positive Rate')
ax.set_ylabel('True Positive Rate')
ax.set_title('ROC Curves — Client Holdout Test Set')
ax.legend(loc='lower right')
plt.tight_layout()
plt.savefig(CHART_DIR / 'roc_curves.png', bbox_inches='tight', dpi=150)
plt.close()

# Precision@K
fig, ax = plt.subplots(figsize=(10, 6))
k_values = [10, 20, 30, 50, 75, 100, 150, 200, 300, 500]
for (name, probs), color in zip(predictions.items(), colors):
    pk_vals = [precision_at_k(y_test, probs, k) for k in k_values]
    ax.plot(k_values, pk_vals, color=color, marker='o', markersize=4, label=name)
ax.plot(k_values, [float(y_test.mean())] * len(k_values), 'k--', alpha=0.3, label=f'Base rate ({y_test.mean():.3f})')
ax.set_xlabel('K (top-N pages)')
ax.set_ylabel('Precision@K')
ax.set_title('Precision@K — Client Holdout Test Set')
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig(CHART_DIR / 'precision_at_k.png', bbox_inches='tight', dpi=150)
plt.close()

# Confusion matrix + calibration
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
cm = confusion_matrix(y_test, best_preds)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[0],
            xticklabels=['Not Declining', 'Declining'],
            yticklabels=['Not Declining', 'Declining'])
axes[0].set_title(f'Confusion Matrix — {best_name}')
axes[0].set_xlabel('Predicted')
axes[0].set_ylabel('Actual')

frac_pos, mean_pred = calibration_curve(y_test, best_probs, n_bins=10, strategy='quantile')
axes[1].plot([0, 1], [0, 1], 'k--', alpha=0.3, label='Perfect')
axes[1].plot(mean_pred, frac_pos, 's-', color='#2A5D63', label=best_name)
axes[1].set_xlabel('Mean Predicted Probability')
axes[1].set_ylabel('Fraction of Positives')
axes[1].set_title(f'Calibration Curve — {best_name}')
axes[1].legend()
plt.tight_layout()
plt.savefig(CHART_DIR / 'confusion_and_calibration.png', bbox_inches='tight', dpi=150)
plt.close()

# Feature importance
fig, ax = plt.subplots(figsize=(10, 7))
ax.barh(imp_df['feature'][::-1], imp_df['importance'][::-1], color='#2A5D63')
ax.set_title(f'Top 20 Feature Importances — {best_name}')
ax.set_xlabel('Importance')
plt.tight_layout()
plt.savefig(CHART_DIR / 'feature_importance_best.png', bbox_inches='tight', dpi=150)
plt.close()

# Per-client performance
test_df = df.iloc[test_idx].copy()
test_df['prob'] = best_probs
test_df['pred'] = best_preds

client_perf = test_df.groupby('client_id').agg(
    n_pages=('content_id', 'count'),
    actual_rate=('is_declining', 'mean'),
    pred_rate=('pred', 'mean'),
    precision=('is_declining', lambda x: precision_score(x, test_df.loc[x.index, 'pred'], zero_division=0)),
    recall=('is_declining', lambda x: recall_score(x, test_df.loc[x.index, 'pred'], zero_division=0)),
).reset_index()
client_perf = client_perf[client_perf['n_pages'] >= 10].sort_values('n_pages', ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
x = np.arange(len(client_perf))
axes[0].bar(x - 0.15, client_perf['precision'], 0.3, color='#2A5D63', label='Precision')
axes[0].bar(x + 0.15, client_perf['recall'], 0.3, color='#B4552F', label='Recall')
axes[0].set_xticks(x)
axes[0].set_xticklabels([f'c{i}' for i in range(len(client_perf))], fontsize=7, rotation=45)
axes[0].set_title('Per-Client Precision & Recall')
axes[0].legend()
axes[1].bar(x, client_perf['n_pages'], color='#6F4E7C')
axes[1].set_xticks(x)
axes[1].set_xticklabels([f'c{i}' for i in range(len(client_perf))], fontsize=7, rotation=45)
axes[1].set_title('Pages per Client (test set)')
plt.tight_layout()
plt.savefig(CHART_DIR / 'per_client_performance.png', bbox_inches='tight', dpi=150)
plt.close()

# Error analysis
test_df['error_type'] = 'correct'
test_df.loc[(test_df['is_declining'] == 1) & (test_df['pred'] == 0), 'error_type'] = 'false_negative'
test_df.loc[(test_df['is_declining'] == 0) & (test_df['pred'] == 1), 'error_type'] = 'false_positive'

fig, axes = plt.subplots(1, 3, figsize=(18, 5))
for i, col in enumerate(['impressions_90d', 'avg_position', 'content_age_days']):
    data = test_df.copy()
    data[col] = pd.to_numeric(data[col], errors='coerce')
    if col == 'impressions_90d':
        data[col] = np.log1p(data[col].clip(lower=0))
        xlabel = 'log(impressions_90d)'
    else:
        xlabel = col
    for et in ['correct', 'false_positive', 'false_negative']:
        subset = data[data['error_type'] == et][col].dropna()
        axes[i].hist(subset, bins=40, alpha=0.5, label=et)
    axes[i].set_title(f'{xlabel} by Error Type')
    axes[i].legend(fontsize=8)
plt.tight_layout()
plt.savefig(CHART_DIR / 'error_analysis.png', bbox_inches='tight', dpi=150)
plt.close()

print(f'\nError type distribution:')
print(test_df['error_type'].value_counts())

# --- Save results ---
model_results = {
    'best_model': best_name,
    'split': 'client_holdout',
    'n_train': int(len(train_idx)),
    'n_test': int(len(test_idx)),
    'n_test_clients': int(len(test_clients)),
    'models': results,
    'baselines': baselines,
    'feature_importance_top': [
        {'feature': r['feature'], 'importance': float(r['importance'])}
        for _, r in imp_df.head(15).iterrows()
    ],
    'random_seed': RANDOM_SEED,
}

results_path = OUTPUT_DIR / 'capstone_model_results.json'
results_path.write_text(json.dumps(model_results, indent=2))
print(f'\nSaved: {results_path}')

# Save predictions
pred_df = test_df[['content_id', 'client_id', 'is_declining', 'prob', 'pred', 'error_type',
                    'impressions_90d', 'ctr', 'avg_position', 'content_age_days', 'content_type']].copy()
pred_df.to_csv(PROCESSED_DIR / 'capstone_predictions.csv', index=False)
print(f'Saved predictions: {len(pred_df):,} rows')

print(f'\n✓ Pipeline complete')
print(f'  Best model: {best_name}')
print(f'  ROC AUC: {results[best_name]["roc_auc"]:.4f} (baseline stale: {baselines["stale_first_rule"]["roc_auc"]:.4f})')
print(f'  Avg Precision: {results[best_name]["average_precision"]:.4f} (baseline: {baselines["stale_first_rule"]["average_precision"]:.4f})')