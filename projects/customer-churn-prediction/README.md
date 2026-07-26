# Customer Churn Prediction (Classification)

**Focus of this project: predictive modeling.** Where the other e-commerce
project answers "what happened" (SQL/BI), this one answers "what's likely
to happen next" — classifying which customers are at risk of not
returning, using scikit-learn.

## Problem framing

Churn is defined as: **no order in the 90 days following a feature
cutoff date**, for customers who had already signed up and placed at
least one order before that cutoff. Concretely:

- Feature cutoff `T0` = 90 days before the dataset's end date.
- All features (recency, frequency, monetary value, tenure, cancellation
  rate, etc.) are computed using **only** orders on or before `T0`.
- The label — churned or not — is computed from what happens **after**
  `T0`, in the following 90 days.

This split matters: using "days since last order" as of *today* as both
a feature and the basis for the label would leak the answer into the
input. Separating a feature window from an outcome window is what makes
this an honest predictive model rather than a circular one.

## Honest caveats

- **Class imbalance.** 77.3% of eligible customers churned by this
  definition (805 of 1,042) — a majority-class baseline already gets
  77.3% accuracy, so accuracy alone is a weak metric here. ROC-AUC
  (0.954) and precision/recall are reported for that reason.
- **"Churn" here partly reflects one-time buyers, not just disengaged
  repeat customers.** A meaningful share of customers were only ever
  going to place 1-2 orders in total (that's baked into how "New"
  segment customers behave) — for them, "churned" is closer to "never
  going to be a repeat customer" than "used to buy, then stopped." A
  production churn model would ideally separate these cases; this one
  doesn't, and that's a real limitation worth naming rather than
  glossing over.
- **`segment` is a strong predictor partly by construction** — VIP and
  Returning customers are defined by having ordered more often, so their
  correlation with not-churning is somewhat definitional, not purely
  discovered. `recency_days` and `tenure_days` are the more genuinely
  behavioral signals, and they're also the two strongest features.

## Results

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---|---|---|---|---|
| Logistic Regression | 87.0% | 96.2% | 86.6% | 0.911 | 0.946 |
| **Random Forest** | **87.7%** | **97.2%** | **86.6%** | **0.916** | **0.954** |

Baseline (always predict the majority class): 77.3% accuracy — both
models clear that bar, and the ROC-AUC gap (0.95 vs. 0.50 for a random
guess) is where the real signal shows up.

**Top predictive features (Random Forest):** `recency_days` (40%),
`tenure_days` (19%), being a VIP customer (14.5%), `order_span_days`
(5.5%), being a Returning customer (5.5%). Recency alone carries almost
half the model's predictive weight — customers who haven't ordered
recently are, unsurprisingly but now quantifiably, the ones least likely
to order again.

## Dataset & method

Uses the same synthetic e-commerce dataset as the SQL/dashboard
projects (1,200 customers, 3,436 orders). Built with `pandas` for
feature engineering and `scikit-learn` (`LogisticRegression`,
`RandomForestClassifier`, `ColumnTransformer`, `StandardScaler`,
`OneHotEncoder`) for modeling. Evaluated with a stratified 75/25
train/test split and `class_weight='balanced'` to account for the
churn/non-churn imbalance.

## Files

- `build_features.py` — feature engineering with the time-based
  train/outcome window split
- `train_model.py` — trains Logistic Regression and Random Forest,
  outputs metrics and feature importances
- `index.html` — dashboard: KPI cards, confusion matrix, ROC curve,
  feature importance chart
- `churn_features.csv`, `model_results.json` — generated outputs

## Skills demonstrated

Leakage-aware feature engineering (feature window vs. outcome window),
classification modeling with scikit-learn, evaluating with metrics
appropriate to an imbalanced problem rather than defaulting to
accuracy, and being upfront about where a model's strongest predictor
is partly definitional rather than purely discovered.
