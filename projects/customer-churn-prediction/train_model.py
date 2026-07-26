import pandas as pd
import numpy as np
import json
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                              roc_auc_score, confusion_matrix, roc_curve)

df = pd.read_csv('churn_features.csv')

NUMERIC = ['frequency', 'monetary', 'avg_order_value', 'recency_days', 'tenure_days',
           'order_span_days', 'cancel_return_rate']
CATEGORICAL = ['segment', 'acquisition_channel']
TARGET = 'churned'

df = df.dropna(subset=NUMERIC + CATEGORICAL + [TARGET])
X = df[NUMERIC + CATEGORICAL]
y = df[TARGET]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

preprocessor = ColumnTransformer([
    ('num', StandardScaler(), NUMERIC),
    ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), CATEGORICAL),
])

results = {}

for name, clf in [
    ('Logistic Regression', LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42)),
    ('Random Forest', RandomForestClassifier(n_estimators=300, max_depth=6, class_weight='balanced', random_state=42)),
]:
    pipe = Pipeline([('prep', preprocessor), ('clf', clf)])
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)
    y_proba = pipe.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_proba)
    cm = confusion_matrix(y_test, y_pred).tolist()
    fpr, tpr, _ = roc_curve(y_test, y_proba)

    results[name] = {
        'accuracy': round(acc, 3), 'precision': round(prec, 3), 'recall': round(rec, 3),
        'f1': round(f1, 3), 'roc_auc': round(auc, 3), 'confusion_matrix': cm,
        'roc_curve': {'fpr': [round(x,4) for x in fpr[::max(1,len(fpr)//30)]],
                      'tpr': [round(x,4) for x in tpr[::max(1,len(tpr)//30)]]},
    }
    print(f"\n{name}")
    print(f"  Accuracy: {acc:.3f}  Precision: {prec:.3f}  Recall: {rec:.3f}  F1: {f1:.3f}  ROC-AUC: {auc:.3f}")
    print(f"  Confusion matrix: {cm}")

    if name == 'Random Forest':
        # Feature importances
        cat_names = pipe.named_steps['prep'].named_transformers_['cat'].get_feature_names_out(CATEGORICAL)
        feature_names = NUMERIC + list(cat_names)
        importances = pipe.named_steps['clf'].feature_importances_
        imp_df = pd.DataFrame({'feature': feature_names, 'importance': importances}).sort_values('importance', ascending=False)
        print(imp_df.head(10))
        results['feature_importance'] = [
            {'feature': r['feature'], 'importance': round(r['importance'], 4)}
            for _, r in imp_df.head(8).iterrows()
        ]

results['class_balance'] = {'churned': int(y.sum()), 'not_churned': int((y==0).sum()), 'total': int(len(y))}
results['baseline_majority_accuracy'] = round(max(y.mean(), 1-y.mean()), 3)

with open('model_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\nBaseline (predict majority class every time):", results['baseline_majority_accuracy'])
print("Class balance:", results['class_balance'])
