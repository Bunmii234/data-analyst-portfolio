# Vendor Billing Trend & Anomaly Report

**Focus of this project: Excel and interactive dashboard reporting.** An
extension of the vendor billing audit work from my Administrative &
Operations Specialist role at Ascendo Resources (auditing transaction
and vendor billing records to identify processing discrepancies) into a
repeatable Excel/dashboard tool, rather than a one-off manual check.

## The problem

Vendor invoices are supposed to bill at a contracted rate x quantity,
but real vendor billing drifts: rates creep up without a contract
amendment, billed hours exceed what was actually logged, duplicate
invoices slip through under different invoice numbers, and fees get
added without prior notice. None of these show up if you only sanity
check whether an invoice total looks "about right" — they only show up
when every invoice is checked against what it was actually supposed to
cost.

## What was built

**`Vendor_Billing_Report.xlsx`** — the primary deliverable:
- **Raw Data** sheet — invoices as received, with realistic messiness
  (mixed date formats, inconsistent vendor name casing/whitespace)
- **Clean Data** sheet — normalized and ready for analysis
- **Vendor Summary** and **Category Summary** sheets — PivotTable-style
  aggregations (invoice count, flagged count, total billed vs. expected,
  variance) by vendor and by category
- **Dashboard** sheet — native Excel charts (bar, pie, line) with KPI
  cards, built so the workbook is a standalone reporting tool without
  needing a separate BI license or app

**`index.html`** — a browsable companion dashboard (KPI cards, charts,
a filterable invoice table, and real scenario write-ups) for anyone
viewing the portfolio without opening Excel.

## Results (from the live data)

- **1,462 invoices** across 12 vendors and 6 spend categories, Jan–Dec 2025
- **$225,120.72** in flagged overbilling across **519 invoices (35.5%)**
- **5 vendors account for over 75%** of total flagged variance — this
  isn't spread evenly across the vendor list, it concentrates
- **Hartwell Legal Advisors alone accounts for ~26%** of all flagged
  variance ($58,673.13), split between rate drift and quantity padding
  across 52 flagged invoices

## Real scenarios this audit caught

1. **A 38% rate overcharge** — Hartwell Legal Advisors billed
   $427.48/hour against a $310/hour contracted rate on a single May
   invoice, a $7,965.14 overcharge that was still sitting in "Pending
   Review."
2. **Hours billed that exceeded logged usage** — a separate Hartwell
   invoice billed the correct rate but 90 hours against recorded usage
   that didn't support it — $4,960 in variance, and this one had
   already been *approved* before the audit caught it.
3. **A near-duplicate payment** — ClearView Janitorial's June invoice
   was submitted twice under separate invoice IDs for the identical
   vendor, amount, and service period.
4. **An undisclosed late fee** — Vantage Software's November invoice
   came in $148.70 over expected, not from a rate or quantity error,
   but a late fee applied without prior notice — a contract-terms issue
   flagged separately from billing math errors.

Full detail (including the actual invoice-level entries) is in
`index.html` and the workbook's Clean Data / Vendor Summary sheets.

## Files

```
vendor-billing-report/
├── generate_data.py          # builds the synthetic invoice dataset
├── build_excel_report.py     # builds Vendor_Billing_Report.xlsx
├── Vendor_Billing_Report.xlsx  # the Excel deliverable (native charts + KPIs)
├── index.html                 # browsable dashboard + scenario write-ups
└── data/
    └── vendor_invoices.csv
```

## How to run

```bash
python3 generate_data.py         # regenerates the invoice dataset
python3 build_excel_report.py    # rebuilds the Excel workbook
```

## Skills demonstrated

Excel-native reporting (PivotTable-style aggregation, native charts, KPI
dashboarding) without relying on a separate BI tool license, rate/
quantity/duplicate/fee anomaly detection logic, and — consistent with
the rest of this portfolio — flagging exactly which invoices need human
review rather than just reporting a total variance number.
