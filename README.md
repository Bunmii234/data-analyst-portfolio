# Data Analyst Portfolio

Three featured projects on the live site, two of them modeled directly
on real work I've done: Medicaid HCBS billing compliance (my current
role at Arc of Morris) and insurance-logistics underwriting (my
internship at Jewelers Mutual), plus a general vendor-billing audit
project to show the same skills outside a specific domain. Each project
uses synthetic data with real structure (seasonality, cohort effects,
business rules) rather than a generic public dataset.

**Open `index.html` in a browser** — it's a small 3-page site (Home / About / Work), not just a project list. `work.html` has the full project grid, filterable by category.

## Featured projects

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

## Other projects (not currently featured on the live site)

These still exist in `projects/` and still work — I'm keeping them out
of the main site for now to keep the portfolio to a small number of
projects I can talk about in real depth, not because they're bad work:

- **[E-Commerce Business Performance Analysis](projects/ecommerce-sql-analysis/)** — SQL, window functions, cohort analysis
- **[E-Commerce Performance Dashboard](projects/ecommerce-bi-dashboard/)** — interactive Chart.js dashboard
- **[Customer Churn Prediction](projects/customer-churn-prediction/)** — scikit-learn classification model

An [archive](archive/) folder holds earlier project versions no longer
part of the active portfolio (a banking transaction reconciliation
project and the retired Claims Frequency Forecasting model) — kept for
reference. `projects/bbbs-mentor-gap-analysis/` also exists but isn't
finished or linked anywhere yet.

## Suggested resume bullets (for the 3 featured projects)

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
- *Vendor Billing Report*: "Built an Excel-based, interactively
  dashboarded vendor billing audit covering 1,462 invoices; identified $225K in flagged
  overbilling from rate drift, quantity padding, and duplicate invoices,
  concentrated in 5 of 12 vendors."

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
