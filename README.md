# Data Analyst Portfolio

Three projects, each built to showcase one thing — not a grab-bag of
charts. All use synthetic data built around the industries I've
actually worked in (insurance, vendor/ops), not a generic public
dataset, because the metrics and edge cases only mean something if
they're grounded in a real domain's rules. Two of the three map
directly to a job on my resume; the third rounds out the skill set with
Excel and interactive dashboard reporting.

**Open `index.html` in a browser** — it's a small 3-page site (Home / About / Work), not just a project list. `work.html` has the project grid linking to all three projects below.

## Projects

1. **[Vendor Billing Trend & Anomaly Report](projects/vendor-billing-report/)**
   — *Excel & interactive dashboard reporting.* An Excel workbook (Power
   Query-style cleaning, PivotTable summaries, native charts) plus a
   browsable dashboard companion, auditing 1,462 vendor invoices for
   rate drift, quantity padding, duplicate billing, and undisclosed
   fees. Found $225K in flagged overbilling, concentrated in 5 vendors.
   An extension of the vendor billing audit work at Ascendo Resources.

2. **[Claims Frequency Forecasting](projects/claims-forecasting/)**
   — *technical model.* Trend + seasonal decomposition built from first
   principles with NumPy, forecasting claims volume and reserve dollars
   6 months forward, allocated across value tiers. Upfront about the
   limits of forecasting from 30 monthly data points rather than
   overselling precision. Paired with Ascendo Resources on the resume.

3. **[Insured Jewelry Logistics Dashboard](projects/insured-jewelry-logistics/)**
   — *domain expertise.* An interactive dashboard built around a real
   underwriting rule (courier security tier must match declared shipment
   value). Surfaces that policy violations are only 6.2% of shipments
   but drive 26.4% of claims dollars — an insight that only makes sense
   if you understand insured logistics, not just logistics. Modeled on
   my Operations Analyst Intern work at Jewelers Mutual.

An [archive](archive/) folder holds earlier project versions no longer
part of the active portfolio (a generic e-commerce SQL/dashboard pair,
and a banking transaction reconciliation project) — kept for reference.

## Suggested resume bullets

- *Vendor Billing Report*: "Built an Excel-based, interactively
  dashboarded vendor billing audit covering 1,462 invoices; identified $225K in flagged
  overbilling from rate drift, quantity padding, and duplicate invoices,
  concentrated in 5 of 12 vendors."
- *Claims Forecasting*: "Built a trend + seasonal decomposition model
  from first principles in NumPy to forecast insurance claims volume
  and reserve requirements 6 months out, allocated across risk tiers
  for underwriting planning."
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
│   ├── claims-forecasting/
│   │   ├── README.md
│   │   ├── forecast.py                     # the centerpiece
│   │   ├── index.html                      # charts + scenario write-ups
│   │   ├── data/
│   │   └── output/
│   └── insured-jewelry-logistics/
│       ├── README.md
│       ├── generate_data.py
│       ├── index.html                      # dashboard
│       └── data/
└── archive/                                # earlier project versions (not active)
```

## How to run locally

Open `index.html` directly in a browser (double-click it, or `open index.html` on macOS), or serve the folder so relative links behave exactly like a real site:

```bash
cd data-analyst-portfolio
python3 -m http.server 8000
# then visit http://localhost:8000 in your browser
```
