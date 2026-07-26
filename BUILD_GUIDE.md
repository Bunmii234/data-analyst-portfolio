# Portfolio Build & Screenshot Guide

Purpose: (1) walk through what's actually implemented in each project so
you can explain it fluently in an interview, (2) tell you exactly what to
click/run yourself, and (3) tell you exactly what real screenshots to take
and where they go so the site stops using placeholder SVG art.

Work through projects top to bottom. Each one ends with a "Screenshot
checklist" — do that step before moving on, so you're not doing a giant
screenshot session at the end.

---

## 0. One-time setup

```bash
cd /Users/bunmi/Work/PORTFOLIO
python3 -m http.server 8000
# visit http://localhost:8000 in your browser, leave this running
```

Create a folder for real images so they don't clash with existing files:

```bash
mkdir -p /Users/bunmi/Work/PORTFOLIO/screenshots
```

Every screenshot below: **Cmd+Shift+4** (Mac) to drag-select an area, or
**Cmd+Shift+4 then Space** to capture a whole window cleanly (gets the
window chrome/shadow, looks more "real"). Save straight into the
`screenshots/` folder with the filenames given in each checklist.

---

## 1. Vendor Billing Trend & Anomaly Report

**Elevator pitch:** "I audited 1,462 vendor invoices in Excel against
their contracted rate — found $225K in flagged overbilling, and 5 of 12
vendors accounted for 75%+ of it. Built it as a standalone Excel workbook
with PivotTable-style summaries and native charts, plus a browsable
dashboard version."

**Numbers to have cold:** 1,462 invoices · $225,120.72 flagged · 519
invoices flagged (35.5%) · Hartwell Legal Advisors = ~26% of all flagged
variance alone.

**What's already built:** everything. `Vendor_Billing_Report.xlsx` and
`index.html` both exist and work.

### Steps to actually do

1. Open the workbook:
   ```bash
   open /Users/bunmi/Work/PORTFOLIO/projects/vendor-billing-report/Vendor_Billing_Report.xlsx
   ```
2. Click through each sheet tab in this order — **Raw Data → Clean Data →
   Vendor Summary → Category Summary → Dashboard**. Read the Dashboard
   sheet's KPI cards and charts closely; this is the sheet you'll be
   asked about.
3. In the browser, open `http://localhost:8000/projects/vendor-billing-report/index.html`
   and click through the scenario write-ups (the 4 "real scenarios"
   listed in the README — rate overcharge, hours-exceeded, duplicate
   invoice, undisclosed fee). Be able to describe one from memory.

### Talking points to rehearse

- Why Excel and not just a script: it's a self-contained audit tool a
  non-technical AP person could reuse without you — no BI license needed.
- What "flagged" means mechanically: invoice amount vs. (contracted rate
  × billed quantity), plus separate duplicate-detection and fee-disclosure
  checks.
- One concrete example: the 38% rate overcharge on the Hartwell invoice.

### Screenshot checklist

- [ ] `vendor-01-dashboard-sheet.png` — the Excel **Dashboard** sheet, full
      window, showing KPI cards + charts.
- [ ] `vendor-02-vendor-summary.png` — the **Vendor Summary** sheet
      (proves the PivotTable-style aggregation is real).
- [ ] `vendor-03-web-dashboard.png` — the browser view of the project's
      `index.html`.

---

## 2. HCBS Waiver Billing Compliance Dashboard

**Elevator pitch:** "Modeled on my actual work at Arc of Morris — a
Medicaid HCBS billing rule where a visit only 'counts' if EVV verifies it
happened and it's within ISP-authorized hours. Violations are only 13.3%
of visits but drive 92% of denied claim dollars, and it's concentrated in
3 of 12 sites — so the fix is targeted retraining, not a policy overhaul."

**Numbers to have cold:** 66,547 visits · 13.3% violation rate · 92.1% of
denied dollars · 66x higher denial rate on violation visits · 3 of 12
sites (Morris Day Center, Willow Lane Group Home, Maplewood Group Home)
run 27–28% violation rates.

**What's already built:** everything — `index.html` dashboard, full
dataset.

### Steps to actually do

1. ```bash
   open http://localhost:8000/projects/hcbs-billing-compliance/index.html
   ```
   (or just open it in the browser tab you already have running)
2. Toggle the site-type filter and watch the KPI cards + charts
   recalculate — this is the interaction you'll want to describe
   ("it's not a static image, filters recompute the KPIs client-side").
3. Look specifically at the "violation rate by site" chart and find the
   3 outlier sites — be ready to name them.

### Talking points to rehearse

- The two-part compliance rule: EVV match **and** within ISP-authorized
  hours — either failure alone is a violation.
- Why site-level concentration matters more than the raw 13.3% headline:
  it changes the recommended fix.
- Waiver type (Community Care vs. Supports) turned out **not** to matter
  (13.4% vs. 13.2%) — a good example of ruling something out, not just
  finding a pattern.

### Screenshot checklist

- [ ] `hcbs-01-full-dashboard.png` — full-page screenshot (browser
      Cmd+Shift+4, or use dev tools' "Capture full size screenshot" for a
      true full-page capture).
- [ ] `hcbs-02-site-chart-filtered.png` — the violation-by-site chart
      with a site-type filter applied, to show interactivity.

---

## 3. Insured Jewelry Logistics Dashboard

**Elevator pitch:** "Modeled on my internship at Jewelers Mutual — the
rule here is that a shipment's declared value has to match the courier's
security tier. Only 6.2% of shipments violate that, but they drive 26.4%
of claims dollars — 3.5x the loss rate of compliant shipments."

**Numbers to have cold:** 5,200 shipments · 6.2% violation rate · 26.4% of
claims dollars · 3.5x loss rate · 64.2% portfolio loss ratio.

**What's already built:** everything.

### Steps to actually do

1. ```bash
   open http://localhost:8000/projects/insured-jewelry-logistics/index.html
   ```
2. Find the flagged-shipment table — this is the actual deliverable an
   underwriting team would work from. Sort/filter it by carrier tier and
   value tier.
3. Note the Enhanced-tier loss ratio anomaly (117.3%, small-sample driven,
   56 paid claims total) — practice explaining *why* you didn't just
   report that number as "Enhanced tier is risky."

### Talking points to rehearse

- The tiering rule itself (under $10K any carrier; $10K–$50K needs
  signature-required Enhanced; $50K+ needs High-Security/armored).
- Why you flagged the Enhanced-tier loss ratio as a small-sample artifact
  instead of reporting it at face value — this is a judgment example,
  good interview material.
- The flagged-shipment table as the actual actionable output, not the
  charts.

### Screenshot checklist

- [ ] `jewelry-01-full-dashboard.png` — full dashboard view.
- [ ] `jewelry-02-flagged-table.png` — the flagged-shipment table,
      sorted by declared value descending.

---

## 4. E-Commerce Business Performance Analysis (SQL)

**Elevator pitch:** "Six standalone SQL business questions against a
relational e-commerce dataset — window functions, CTEs, cohort analysis.
VIP customers drive 4.3x the lifetime revenue of new customers, and I
flagged a cohort right-censoring artifact instead of reporting a
misleading repeat-purchase drop-off as a real trend."

**Numbers to have cold:** 3,436 orders · 1,200 customers · VIP = 4.3x new
customer revenue · Paid Search/Email ≈ $654–694 revenue/customer.

**What's already built:** everything — 6 `.sql` files, SQLite db, CSVs.

### Steps to actually do

1. Open a SQL browser against the db — DB Browser for SQLite (free) or
   the SQLite VS Code extension both work well for taking a clean
   screenshot with results visible:
   ```bash
   open -a "DB Browser for SQLite" /Users/bunmi/Work/PORTFOLIO/projects/ecommerce-sql-analysis/data/ecommerce.db
   ```
   If you don't have it: `brew install --cask db-browser-for-sqlite`
2. In the "Execute SQL" tab, paste in `sql/03_customer_segmentation_rfm.sql`
   and run it — this is the one with the clearest "wow" number (4.3x).
3. Also run `sql/04_repeat_purchase_rate_by_cohort.sql` and be ready to
   explain the right-censoring issue live, pointing at the actual output
   rows where recent cohorts look artificially low.

### Talking points to rehearse

- What a CTE and a window function (`LAG`) are doing in plain English,
  not just "I used CTEs."
- The cohort right-censoring explanation — this is your best "I know when
  a number is lying to you" story, use it in behavioral questions too.

### Screenshot checklist

- [ ] `sql-01-rfm-query-results.png` — DB Browser (or your SQL tool) with
      the RFM/segmentation query and its results both visible.
- [ ] `sql-02-cohort-query-results.png` — the cohort repeat-purchase
      query and results.

---

## 5. E-Commerce Performance Dashboard

**Elevator pitch:** "A fully offline, filterable KPI dashboard — Chart.js,
client-side filtering, sortable table — over the same e-commerce dataset
as the SQL project."

**What's already built:** everything.

### Steps to actually do

1. ```bash
   open http://localhost:8000/projects/ecommerce-bi-dashboard/index.html
   ```
2. Apply 2–3 filters together (channel + segment) and confirm the KPI
   cards, charts, and table all move together — that's the thing worth
   screenshotting and worth mentioning ("filters compose with AND logic").
3. Be ready to explain the "Unique Customers" KPI caveat in the README —
   it's currently a proxy (order count) because customer_id isn't carried
   into the order-item table. Naming this limitation unprompted is a good
   interview moment.

### Screenshot checklist

- [ ] `ecomm-dash-01-default.png` — unfiltered view.
- [ ] `ecomm-dash-02-filtered.png` — same view with filters applied, to
      show the interaction.

---

## 6. Customer Churn Prediction

**Elevator pitch:** "A scikit-learn Random Forest classifier predicting
which customers won't order again in the next 90 days — built with a
leakage-aware feature/outcome time split so it's an honest model, not a
circular one. 0.954 ROC-AUC, and recency + tenure carry the majority of
the predictive weight."

**Numbers to have cold:** 77.3% majority-class baseline · Random Forest:
87.7% accuracy, 0.954 ROC-AUC · recency_days = 40% feature importance.

**What's already built:** everything, including a stray `venv/` folder
you should delete (see cleanup below).

### Steps to actually do

1. Cleanup first:
   ```bash
   rm -rf /Users/bunmi/Work/PORTFOLIO/projects/customer-churn-prediction/venv
   ```
2. Re-run the pipeline yourself so you've actually executed it, not just
   inherited the output files:
   ```bash
   cd /Users/bunmi/Work/PORTFOLIO/projects/customer-churn-prediction
   python3 -m venv venv && source venv/bin/activate
   pip install pandas scikit-learn
   python3 build_features.py
   python3 train_model.py
   ```
   Watch the terminal output — it should print the accuracy/ROC-AUC
   numbers, matching the README table.
3. Open the dashboard:
   ```bash
   open http://localhost:8000/projects/customer-churn-prediction/index.html
   ```
   Look at the confusion matrix and feature-importance chart specifically.

### Talking points to rehearse

- The leakage explanation in your own words: features computed only from
  data *before* the cutoff, label computed only from what happens *after*
  it. Practice this — it's the single most important thing to get right
  verbally, since a lot of candidates get feature/label leakage wrong.
- Why accuracy alone is misleading here (77.3% baseline) and why ROC-AUC
  is the number that actually shows the model learned something.
- The two honest caveats already written into the README (class
  imbalance conflating one-time buyers with true churn; segment being
  partly definitional) — say these unprompted, don't wait to be asked.

### Screenshot checklist

- [ ] `churn-01-terminal-training.png` — terminal output from
      `train_model.py` showing the metrics printing live.
- [ ] `churn-02-dashboard.png` — the dashboard (confusion matrix + ROC
      curve + feature importance visible).

---

## 7. BBBS Mentor Gender Gap Analysis — build from scratch

This one doesn't exist yet. `data/` is empty and none of the three
promised deliverables (Excel workbook, Tableau Public dashboard, slide
deck) have been built. `work.html` already links to it on GitHub, so
finish this before anyone clicks that link.

**Elevator pitch (once built):** "A volunteer consulting-style project
for Big Brothers Big Sisters, calibrated to real, publicly reported
chapter statistics — boys make up 90.5% of the waitlist and wait 10.1
months on average vs. 4.6 for girls, driven by a structural mismatch
(only 38% of volunteers are men, but 70% of kids who sign up are boys),
not a seasonal dip."

### Step 1 — Generate the data

```bash
cd /Users/bunmi/Work/PORTFOLIO/projects/bbbs-mentor-gap-analysis
python3 generate_data.py
```

This writes `volunteers.csv`, `littles.csv`, `matches.csv` into `data/`.
Confirm the printed summary roughly matches: ~1,300 volunteers (~38%
male), ~1,080 littles (~70% boys), ~315 currently waitlisted.

### Step 2 — Build the Excel workbook

Target file: `BBBS_Mentor_Gap_Analysis.xlsx`, saved in this project
folder. Structure it like the Vendor Billing workbook (Raw Data / Clean
sheets / Summary sheets / Dashboard):

1. **Import each CSV as its own sheet** (Data → Get Data → From Text/CSV
   for each of the 3 files, or just copy/paste). Name the sheets
   `Volunteers`, `Littles`, `Matches`.
2. **Build a `Waitlist Summary` sheet** with formulas (not hardcoded
   numbers — the README explicitly calls out "zero hardcoded results"):
   - `=COUNTIFS(Littles!waitlist_status,"Waitlisted",Littles!gender,"Boy")`
   - same for `"Girl"`
   - `=COUNTIFS(Littles!waitlist_status,"Waitlisted")` for the total
   - a `% Boys` cell = boys waitlisted / total waitlisted
3. **Build a `Wait Time Summary` sheet**:
   - `=AVERAGEIFS(Matches!wait_days,Matches!little_gender,"Boy")/30` for
     average boy wait time in months (same for Girl)
4. **Build a `Volunteer Supply` sheet**:
   - `=COUNTIFS(Volunteers!status,"Active",Volunteers!gender,"Male")` vs
     `"Female"`, and each as a % of active volunteers
5. **Build the `Dashboard` sheet** with:
   - 4 KPI cells pulling from the summary sheets above (waitlist %
     boys, avg wait gap in months, % male volunteers, current waitlist
     count)
   - A bar chart: waitlist count by gender
   - A bar chart: average wait time by gender
   - A pie/donut chart: volunteer gender split
   - A bar chart: waitlisted count by region (use a `COUNTIFS` per
     region as helper cells, then chart those)

### Step 3 — Build the Tableau Public dashboard

You already have a full walkthrough for this — open and follow it
exactly:

```bash
open /Users/bunmi/Work/PORTFOLIO/projects/bbbs-mentor-gap-analysis/TABLEAU_GUIDE.md
```

It covers: connecting/joining the 3 CSVs, building all 4 sheets, and
assembling + publishing the dashboard. Once published, keep the
Tableau Public URL — you'll need it for the portfolio card.

### Step 4 — Build the slide deck

Target file: `BBBS_Mentor_Gap_Analysis.pptx`, 8 slides, aimed at a
non-technical chapter director:

1. **Title** — "BBBS Mentor Gender Gap Analysis" + your name
2. **The problem** — one sentence + the 90.5%/boys stat, big and bold
3. **Method** — 1-2 lines: synthetic chapter dataset calibrated to
   real, cited BBBS statistics (name 2-3 of the real chapters from the
   README as sources)
4. **Finding 1** — waitlist composition chart (boys vs girls)
5. **Finding 2** — wait-time gap chart (10.1 vs 4.6 months)
6. **Finding 3** — the root cause: volunteer supply chart (38% male vs
   70% of kids being boys) — this is the slide that makes the
   recommendation land
7. **Recommendations** — the 3 from the README (targeted male
   recruitment; track wait time by gender as a KPI; protect match
   durability/screening quality)
8. **Skills demonstrated / thank you**

I can build this actual .pptx file for you once the Excel and Tableau
numbers are final — just ask, and paste in your Tableau Public link
first so slide 4-6 can reference it.

### Step 5 — Screenshot checklist

- [ ] `bbbs-01-excel-dashboard.png`
- [ ] `bbbs-02-tableau-dashboard.png` (or a screenshot of the published
      Tableau Public page itself)
- [ ] `bbbs-03-deck-slide4.png` — one representative slide from the deck

### Step 6 — Wire it back into the site

Once all three deliverables exist and you have the Tableau Public URL,
tell me and I'll:
- swap the BBBS card's placeholder SVG for a real screenshot
- add working links to the Excel file, Tableau Public dashboard, and
  the deck on the project's own page (it currently has no `index.html`
  at all — the work.html card links straight to GitHub)
- commit and push all of it

---

## Swapping real screenshots into the site (do this last, once you have images)

Each project card in `work.html` (and the 3 featured ones on `index.html`)
currently renders an inline SVG as its cover image. To swap in a real
screenshot instead, tell me which project + which screenshot filename
from `screenshots/`, and I'll replace the `<div class="preview-cover">` /
`<div class="card-cover">` SVG block with:

```html
<div class="card-cover">
  <span class="badge">Featured</span>
  <img src="../../screenshots/vendor-01-dashboard-sheet.png" alt="..." style="width:100%;height:100%;object-fit:cover;">
</div>
```

I'll also resize/crop as needed so the 16:10 aspect ratio isn't distorted
— just hand me the raw screenshot and I'll handle the HTML.

---

## Suggested order to tackle this in

Given your Infosys interview is imminent, do these in this order:

1. **Talking points for all 6 finished projects** (re-read the "Talking
   points to rehearse" sections above) — highest interview ROI, costs
   you no build time.
2. Screenshot the 6 finished projects (quick, ~20 min total).
3. Only after the interview: build BBBS from scratch (Steps 1-6 above) —
   it's the most time-consuming piece and isn't needed for tomorrow's
   conversation.
