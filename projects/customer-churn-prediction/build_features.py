"""
Customer churn classification.

Design choice to avoid leakage: rather than using "no order in the last
90 days as of today" as both the label AND a feature (recency), we split
time into a feature window and an outcome window:

  - Feature cutoff T0 = 2026-04-01 (90 days before the dataset's end date)
  - Features (recency, frequency, monetary, tenure, etc.) are computed
    using ONLY orders that happened on or before T0.
  - Label: churned = 1 if the customer has NO order in the outcome
    window (T0, 2026-06-30]; 0 if they do.
  - Only customers who (a) signed up on or before T0 and (b) placed at
    least one order on or before T0 are included -- this is a repeat-
    purchase churn model, not a first-purchase conversion model, and
    excluding very new signups avoids penalizing customers who simply
    haven't had time to order again yet.
"""
import pandas as pd
import numpy as np
from datetime import date
import json

customers = pd.read_csv('data/customers.csv', parse_dates=['signup_date'])
orders = pd.read_csv('data/orders.csv', parse_dates=['order_date'])

END_DATE = pd.Timestamp('2026-06-30')
T0 = pd.Timestamp('2026-04-01')  # feature cutoff, 90 days before end

# Eligible customers: signed up on/before T0
eligible = customers[customers['signup_date'] <= T0].copy()

feat_orders = orders[orders['order_date'] <= T0]
outcome_orders = orders[(orders['order_date'] > T0) & (orders['order_date'] <= END_DATE)]

# Customers with at least 1 order before T0
customers_with_history = feat_orders['customer_id'].unique()
eligible = eligible[eligible['customer_id'].isin(customers_with_history)].copy()

print(f"Eligible customers (signed up <= T0, has order history): {len(eligible)}")

# ---- Feature engineering (all from feat_orders only) ----
g = feat_orders.groupby('customer_id')
feats = g.agg(
    frequency=('order_id', 'count'),
    monetary=('order_total', 'sum'),
    avg_order_value=('order_total', 'mean'),
    last_order_date=('order_date', 'max'),
    first_order_date=('order_date', 'min'),
).reset_index()

feats['recency_days'] = (T0 - feats['last_order_date']).dt.days
feats['tenure_days'] = (T0 - feats['first_order_date']).dt.days
feats['order_span_days'] = (feats['last_order_date'] - feats['first_order_date']).dt.days

# Cancellation / return behavior (risk signal)
status_counts = feat_orders.groupby(['customer_id', 'status']).size().unstack(fill_value=0)
for col in ['Cancelled', 'Returned', 'Completed']:
    if col not in status_counts.columns:
        status_counts[col] = 0
status_counts['cancel_return_rate'] = (status_counts['Cancelled'] + status_counts['Returned']) / (
    status_counts['Cancelled'] + status_counts['Returned'] + status_counts['Completed']
).replace(0, np.nan)
status_counts = status_counts.reset_index()[['customer_id', 'cancel_return_rate']]

df = eligible.merge(feats, on='customer_id', how='left').merge(status_counts, on='customer_id', how='left')
df['cancel_return_rate'] = df['cancel_return_rate'].fillna(0)

# ---- Label: churned = no order in outcome window ----
churned_customers = set(outcome_orders['customer_id'].unique())
df['churned'] = (~df['customer_id'].isin(churned_customers)).astype(int)

print(f"Churn rate: {df['churned'].mean()*100:.1f}%")

df.to_csv('churn_features.csv', index=False)
print(df[['customer_id','segment','acquisition_channel','frequency','monetary',
          'recency_days','tenure_days','cancel_return_rate','churned']].head())
print("\nColumns:", list(df.columns))
