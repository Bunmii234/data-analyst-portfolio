# HCBS Waiver Billing Compliance Dashboard

**Focus of this project: domain expertise.** Like the insured-logistics
project, the point isn't the chart library — it's that the metrics only
make sense if you understand how Medicaid HCBS (Home & Community-Based
Services) billing actually works. This is modeled on the world I work in
as a Data & Reporting Analyst at Arc of Morris, an IDD (intellectual and
developmental disability) services provider — querying EHR backend data
with SQL/Python, building Power BI dashboards on waiver utilization and
compliance, and automating EVV/billing reconciliations.

## The domain insight this is built around

Under state Medicaid HCBS waiver rules, a billed service hour isn't
automatically valid just because staff showed up. Two conditions have to
hold: (1) an Electronic Visit Verification (EVV) record has to confirm
the visit actually happened, matching the billed time window, and (2) the
individual's total billed hours for the month can't exceed what their ISP
(Individual Service Plan) authorizes. A **compliance violation** — billing
without a matching EVV record, or billing above the EVV-verified/ISP-
authorized amount — is what actually drives claim denials, not which site
or waiver program the visit belongs to.

## Key findings (from the live data)

**Violations are a small share of visits but drive almost all the denied
dollars.** Only 13.3% of visits (8,867 of 66,547) have a compliance
violation, but they account for **92.1% of all denied claim dollars**.
Violation visits get denied at a **61.7% rate**, vs. just 0.9% for
compliant visits — a **66x** higher denial rate.

**The problem is concentrated in 3 of 12 sites.** Morris Day Center,
Willow Lane Group Home, and Maplewood Group Home each run 27–28%
violation rates, while the other nine sites sit at 3–11%. That's a
staffing/training/EVV-device pattern at three specific locations, not a
program-wide problem — which changes what the fix looks like (targeted
retraining vs. a system-wide policy change).

**Denial dollars split fairly evenly across three root causes**: EVV
documentation gaps (clock-in/out mismatches, no matching record, visit
outside the authorized window) and authorization gaps (exceeding ISP
hours, service not in the approved plan, missing prior authorization)
each account for roughly half of denied dollars — meaning both EVV
discipline *and* ISP-authorization tracking need attention, not just one.

**Waiver type barely matters.** Community Care Program and Supports
Program visits have nearly identical violation rates (13.4% vs. 13.2%) —
ruling out "it's just this one waiver's paperwork is more complex" as an
explanation, and pointing back to site-level practices as the real driver.

## Dataset

Synthetic, but built around real HCBS billing/EVV rules
(`generate_data.py`):

| Table | Rows | Description |
|---|---|---|
| `sites.csv` | 12 | Residential group homes, day programs, supported employment sites |
| `individuals.csv` | 180 | Individuals served, waiver type, ISP-authorized monthly hours |
| `visits.csv` | 66,547 | EVV visit logs — scheduled/delivered/billed hours, EVV verification flag, compliance violation flag |
| `claims.csv` | 66,547 | One claim per visit — billed amount, claim status, denial reason |

Site-level "documentation discipline" (High/Medium/Low) drives EVV-miss
rate and overbilling rate per site — a deliberate simulation of the
real-world pattern where a handful of sites generate a disproportionate
share of compliance risk.

## Dashboard

Open `index.html` in any browser. KPI cards (violation rate, total
billed, denied $, denial-rate risk multiplier), a callout that states the
core finding in plain language, four charts (violation rate by site,
denied $ by denial reason, monthly violation trend, paid/denied/pending
split), and a site-level detail table — filterable by site type.

## Skills demonstrated

Domain-driven metric design (violation-linked denial rate, risk
multiplier, site-level concentration analysis), building a dataset that
encodes real Medicaid billing/EVV rules rather than random noise, and
turning the analysis into a targeted, actionable finding (3 specific
sites need retraining) rather than a generic dashboard.
