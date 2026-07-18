# Data Analyst Portfolio

Three projects, each built to showcase one thing — not a grab-bag of
charts. All use synthetic data built around the industries I've
actually worked in (banking/financial services, insured logistics), not
a generic public dataset, because the metrics and edge cases only mean
something if they're grounded in a real domain's rules.

## Projects

1. **[Insured Jewelry Logistics Dashboard](01-insured-logistics-dashboard/)**
   — *domain expertise.* An interactive dashboard built around a real
   underwriting rule (courier security tier must match declared shipment
   value). Surfaces that policy violations are only 6.2% of shipments
   but drive 26.4% of claims dollars — an insight that only makes sense
   if you understand insured logistics, not just logistics. Modeled on
   my Operations Analyst Intern work at Jewelers Mutual.

2. **[Banking Transaction Reconciliation](02-banking-reconciliation/)**
   — *data prep and cleaning.* No dashboard, on purpose. Two messy,
   independently-formatted exports of the same transactions get cleaned
   (defensive date parsing, currency normalization, deduplication) and
   reconciled into six actionable categories, isolating $16.7K in real
   discrepancies from $3.6M+ in timing/formatting noise. Modeled on my
   Data Analyst Intern work in Banking & Financial Services at Quintrix
   Solutions.

3. **[Claims Frequency Forecasting](03-claims-forecasting/)**
   — *technical model.* Trend + seasonal decomposition built from first
   principles with NumPy, forecasting claims volume and reserve dollars
   6 months forward, allocated across value tiers. Shares its dataset
   with project 1, and is upfront about the limits of forecasting from
   30 monthly data points rather than overselling precision.

An [archive](archive/) folder holds an earlier, more generic e-commerce
SQL/dashboard pair — kept for reference, not part of the active
portfolio.

## Suggested resume bullets

- *Insured Logistics Dashboard*: "Built an interactive dashboard
  modeling insured-shipment risk; identified that policy-violating
  shipments (under-secured for their declared value) carried a 3.5x
  higher loss rate and drove 26% of claims dollars from just 6% of
  volume."
- *Banking Reconciliation*: "Designed a Python reconciliation pipeline
  to clean and match 12,000+ transaction records across two
  inconsistently-formatted banking systems, isolating $16.7K in genuine
  discrepancies from timing and formatting noise."
- *Claims Forecasting*: "Built a trend + seasonal decomposition model
  from first principles in NumPy to forecast insurance claims volume
  and reserve requirements 6 months out, allocated across risk tiers
  for underwriting planning."

## Repo structure

```
data-analyst-portfolio/
├── 01-insured-logistics-dashboard/
│   ├── README.md
│   ├── generate_data.py
│   ├── dashboard.html            # open this in a browser
│   └── data/
├── 02-banking-reconciliation/
│   ├── README.md
│   ├── generate_data.py
│   ├── reconcile.py              # the centerpiece
│   ├── index.html                # open this in a browser
│   ├── data/{raw,clean}/
│   └── analysis/summary.md
├── 03-claims-forecasting/
│   ├── README.md
│   ├── forecast.py               # the centerpiece
│   ├── index.html                # open this in a browser
│   ├── data/
│   └── output/
├── portfolio-site/
│   └── work.html                 # portfolio landing page, links all three projects
└── archive/                      # earlier generic e-commerce version (not active)
```
