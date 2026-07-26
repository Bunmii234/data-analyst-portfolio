# Data Analyst Portfolio

Five projects, split into two groups intentionally: three are
domain-grounded (built around real business rules from insurance
logistics and Medicaid HCBS billing, modeled on actual work
experience), and two are general-purpose e-commerce/SQL projects aimed
at roles where domain-specific work is less relevant — a pure
e-commerce, tech-product, or general analyst opening. A sixth,
Customer Churn Prediction, adds a scikit-learn classification model on
top of the same e-commerce data. Each project uses synthetic data with
real structure (seasonality, cohort effects, business rules) rather
than a generic public dataset.

**Open `index.html` in a browser** — it's a small 3-page site (Home / About / Work), not just a project list. `work.html` has the full project grid, filterable by category.

## Projects

**Domain-grounded** (insurance / healthcare compliance):

1. **[HCBS Waiver Billing Compliance Dashboard](projects/hcbs-billing-compliance/)**
   — *domain expertise.* An interactive dashboard built around a real
   Medicaid HCBS rule (billed hours must match EVV-verified visits and
   stay within ISP-authorized limits). Surfaces that compliance
   violations are only 13.3% of visits but drive 92.1% of denied claim
   dollars, concentrated in 3 of 12 sites — modeled on my Data &
   Reporting Analyst work at Arc of Morris.

2. **[Insured Jewelry Logistics Dashboard](projects/insured-jewelry-logistics/)**
   — *domain expertise.* An interactive dashboard built around a real
   underwriting rule (courier security tier must match declared shipment
   value). Surfaces that policy violations are only 6.2% of shipments
   but drive 26.4% of claims dollars — modeled on my Operations Analyst
   Intern work at Jewelers Mutual.

3. **[Vendor Billing Trend & Anomaly Report](projects/vendor-billing-report/)**
   — *Excel & interactive dashboard reporting.* An Excel workbook (Power
   Query-style cleaning, PivotTable summaries, native charts) plus a
   browsable dashboard companion, auditing 1,462 vendor invoices for
   rate drift, quantity padding, duplicate billing, and undisclosed
   fees. Found $225K in flagged overbilling, concentrated in 5 vendors.

**General-purpose** (e-commerce / tech-product analyst roles):

4. **[E-Commerce Business Performance Analysis](projects/ecommerce-sql-analysis/)**
   — *SQL.* Six business questions answered in standalone SQL against a
   relational e-commerce dataset — monthly revenue trend, RFM
   segmentation, cohort repeat-purchase rate, channel performance. VIP
   customers drive 4.3x the lifetime revenue of new customers; flags a
   cohort right-censoring artifact rather than reporting it at face
   value.

5. **[E-Commerce Performance Dashboard](projects/ecommerce-bi-dashboard/)**
   — *interactive dashboard.* KPI cards, revenue trend, category/channel/
   segment breakdowns, and a sortable table, filterable by channel,
   segment, category, and order status. Uses the same dataset as the
   SQL project above.

6. **[Customer Churn Prediction](projects/customer-churn-prediction/)**
   — *predictive modeling.* A scikit-learn classification model (Random
   Forest + Logistic Regression) predicting which customers won't
   return, using a leakage-aware feature/outcome time split. Reaches
   0.954 ROC-AUC and 87.7% accuracy against a 77.3% majority-class
   baseline; recency and tenure are the top predictive features.

An [archive](archive/) folder holds earlier project versions no longer
part of the active portfolio (a banking transaction reconciliation
project and the retired Claims Frequency Forecasting model) — kept for
reference.

## Suggested resume bullets

- *Vendor Billing Report*: "Built an Excel-based, interactively
  dashboarded vendor billing audit covering 1,462 invoices; identified $225K in flagged
  overbilling from rate drift, quantity padding, and duplicate invoices,
  concentrated in 5 of 12 vendors."
- *HCBS Billing Compliance Dashboard*: "Built an interactive dashboard
  modeling Medicaid HCBS billing compliance; identified that visits
  lacking matching EVV records or exceeding ISP-authorized hours
  carried a 66x higher claim denial rate and drove 92% of denied
  dollars from just 13% of visits."
- *Insured Logistics Dashboard*: "Built an interactive dashboard
  modeling insured-shipment risk; identified that policy-violating
  shipments (under-secured for their declared value) carried a 3.5x
  higher loss rate and drove 26% of claims dollars from just 6% of
  volume."
- *E-Commerce SQL Analysis*: "Wrote six standalone SQL queries (window
  functions, CTEs, cohort analysis) against a 1,200-customer e-commerce
  dataset; found VIP customers drive 4.3x the lifetime revenue of new
  customers and that Paid Search/Email are the strongest acquisition
  channels by revenue-per-customer."
- *E-Commerce Dashboard*: "Built a filterable KPI dashboard (Chart.js)
  covering revenue trend, channel, segment, and category performance
  across 3,436 orders, with a sortable detail table."
- *Customer Churn Prediction*: "Built a scikit-learn classification
  model (Random Forest, Logistic Regression) predicting customer churn
  from a leakage-aware feature/outcome time split; reached 0.954
  ROC-AUC and 87.7% accuracy, with recency and tenure as the top
  predictive features."

## Repo structure

```
data-analyst-portfolio/
├── index.html                              # Home -- open this first
├── about.html                              # About (bio, experience, skills)
├── work.html                               # Work (project grid, filterable)
├── README.md
├── projects/
│   ├── vendor-billing-report/
│   │   ├── README.md
│   │   ├── generate_data.py
│   │   ├── build_excel_report.py
│   │   ├── Vendor_Billing_Report.xlsx      # the centerpiece
│   │   ├── index.html                      # dashboard + scenario write-ups
│   │   └── data/
│   ├── hcbs-billing-compliance/
│   │   ├── README.md
│   │   ├── generate_data.py
│   │   ├── index.html                      # dashboard
│   │   └── data/
│   ├── insured-jewelry-logistics/
│   │   ├── README.md
│   │   ├── generate_data.py
│   │   ├── index.html                      # dashboard
│   │   └── data/
│   ├── ecommerce-sql-analysis/
│   │   ├── README.md
│   │   ├── sql/                            # 6 standalone .sql files
│   │   ├── analysis/
│   │   └── data/                           # ecommerce.db (SQLite) + CSVs
│   └── ecommerce-bi-dashboard/
│       ├── README.md
│       ├── index.html                      # dashboard
│       └── data/
│   └── customer-churn-prediction/
│       ├── README.md
│       ├── build_features.py               # leakage-aware feature engineering
│       ├── train_model.py                  # trains + evaluates models
│       ├── index.html                      # dashboard (ROC curve, confusion matrix, feature importance)
│       ├── churn_features.csv
│       └── model_results.json
└── archive/                                # earlier project versions (not active)
    ├── claims-forecasting/                 # retired -- see note below
    └── banking-reconciliation/
```

## How to run locally

Open `index.html` directly in a browser (double-click it, or `open index.html` on macOS), or serve the folder so relative links behave exactly like a real site:

```bash
cd data-analyst-portfolio
python3 -m http.server 8000
# then visit http://localhost:8000 in your browser
```
