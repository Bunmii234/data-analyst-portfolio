# Data Analyst Portfolio

Three projects, each built to showcase one thing — not a grab-bag of
charts. Each uses synthetic data grounded in a real domain's rules
rather than a generic public dataset, because the metrics and edge
cases only mean something if they reflect how that domain actually
works. The Insured Jewelry Logistics Dashboard and HCBS Waiver Billing
Compliance Dashboard are modeled on real work experience (Jewelers
Mutual and Arc of Morris, respectively); the Vendor Billing project is
a self-directed build rounding out the skill set with Excel/dashboard
reporting.

**Open `index.html` in a browser** — it's a small 3-page site (Home / About / Work), not just a project list. `work.html` has the project grid linking to all three projects below.

## Projects

1. **[Vendor Billing Trend & Anomaly Report](projects/vendor-billing-report/)**
   — *Excel & interactive dashboard reporting.* An Excel workbook (Power
   Query-style cleaning, PivotTable summaries, native charts) plus a
   browsable dashboard companion, auditing 1,462 vendor invoices for
   rate drift, quantity padding, duplicate billing, and undisclosed
   fees. Found $225K in flagged overbilling, concentrated in 5 vendors.
   A self-directed project practicing the kind of anomaly detection
   common in accounts payable audits.

2. **[HCBS Waiver Billing Compliance Dashboard](projects/hcbs-billing-compliance/)**
   — *domain expertise.* An interactive dashboard built around a real
   Medicaid HCBS rule (billed hours must match EVV-verified visits and
   stay within ISP-authorized limits). Surfaces that compliance
   violations are only 13.3% of visits but drive 92.1% of denied claim
   dollars, concentrated in 3 of 12 sites — modeled on my Data &
   Reporting Analyst work at Arc of Morris.

3. **[Insured Jewelry Logistics Dashboard](projects/insured-jewelry-logistics/)**
   — *domain expertise.* An interactive dashboard built around a real
   underwriting rule (courier security tier must match declared shipment
   value). Surfaces that policy violations are only 6.2% of shipments
   but drive 26.4% of claims dollars — an insight that only makes sense
   if you understand insured logistics, not just logistics. Modeled on
   my Operations Analyst Intern work at Jewelers Mutual.

An [archive](archive/) folder holds earlier project versions no longer
part of the active portfolio (a generic e-commerce SQL/dashboard pair,
a banking transaction reconciliation project, and the retired Claims
Frequency Forecasting model) — kept for reference.

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

## Repo structure

```
data-analyst-portfolio/
├── index.html                              # Home -- open this first
├── about.html                              # About (bio, experience, skills)
├── work.html                               # Work (project grid)
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
│   └── insured-jewelry-logistics/
│       ├── README.md
│       ├── generate_data.py
│       ├── index.html                      # dashboard
│       └── data/
└── archive/                                # earlier project versions (not active)
    └── claims-forecasting/                 # retired -- see note below
```

## How to run locally

Open `index.html` directly in a browser (double-click it, or `open index.html` on macOS), or serve the folder so relative links behave exactly like a real site:

```bash
cd data-analyst-portfolio
python3 -m http.server 8000
# then visit http://localhost:8000 in your browser
```
