"""
Synthetic dataset modeled on Medicaid HCBS (Home & Community-Based Services)
waiver operations for an IDD (intellectual/developmental disability) services
provider -- the domain from the Data & Reporting Analyst role at Arc of Morris.

The core domain insight this dataset is built to surface: under state HCBS
waiver rules, every billed service unit must be backed by an Electronic Visit
Verification (EVV) record confirming the visit actually happened, and total
billed hours in a month cannot exceed the hours authorized in the individual's
ISP (Individual Service Plan). A "billing compliance violation" -- billing
hours that exceed what EVV actually verified, or billing without a matching
EVV record at all -- is a much stronger predictor of claim denial and audit
risk than site or program type alone. That's a finding that only makes sense
if you understand how Medicaid HCBS billing actually works, which is the
point of this project.

Tables: sites, individuals, visits (EVV logs), claims
"""
import random
import csv
import os
from datetime import date, timedelta

random.seed(11)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(OUT_DIR, exist_ok=True)

START_DATE = date(2025, 1, 1)
END_DATE = date(2026, 6, 30)
TOTAL_DAYS = (END_DATE - START_DATE).days

# ---- Sites: residential group homes and day programs ----
SITE_TYPES = ["Residential Group Home", "Day Program", "Supported Employment"]
SITES = []
site_names_res = ["Cedar Grove", "Maplewood", "Birchwood", "Fernbrook", "Hillcrest", "Oakridge", "Willow Lane"]
site_names_day = ["Morris Day Center", "Parsippany Community Hub", "Denville Activity Center"]
site_names_emp = ["JobLink Morris", "Community Works"]

sid = 1
for n in site_names_res:
    SITES.append({"site_id": sid, "site_name": f"{n} Group Home", "site_type": "Residential Group Home"})
    sid += 1
for n in site_names_day:
    SITES.append({"site_id": sid, "site_name": n, "site_type": "Day Program"})
    sid += 1
for n in site_names_emp:
    SITES.append({"site_id": sid, "site_name": n, "site_type": "Supported Employment"})
    sid += 1

SITE_BY_ID = {s["site_id"]: s for s in SITES}

# ---- Individuals served, each with an ISP-authorized monthly hour cap ----
WAIVER_TYPES = ["Supports Program", "Community Care Program (CCP)"]
N_INDIVIDUALS = 180
individuals = []
for iid in range(1, N_INDIVIDUALS + 1):
    site = random.choice(SITES)
    waiver = random.choices(WAIVER_TYPES, weights=[0.4, 0.6])[0]
    if site["site_type"] == "Residential Group Home":
        authorized_hours = round(random.uniform(160, 200), 1)  # near-continuous support
    elif site["site_type"] == "Day Program":
        authorized_hours = round(random.uniform(60, 90), 1)
    else:
        authorized_hours = round(random.uniform(20, 40), 1)
    # Site-level documentation discipline: some sites are much more careful
    # with EVV clock-in/out and billing-to-visit matching than others.
    individuals.append({
        "individual_id": iid,
        "site_id": site["site_id"],
        "waiver_type": waiver,
        "monthly_authorized_hours": authorized_hours,
    })

INDIV_BY_ID = {i["individual_id"]: i for i in individuals}

# Site-level "documentation discipline" factor -- modeled as a property of
# the site (staffing consistency, EVV device reliability, training quality)
SITE_DISCIPLINE = {}
for s in SITES:
    # Most sites are solid; a handful are meaningfully weaker
    SITE_DISCIPLINE[s["site_id"]] = random.choices(
        ["High", "Medium", "Low"], weights=[0.55, 0.30, 0.15]
    )[0]

def month_range(start, end):
    months = []
    cur = date(start.year, start.month, 1)
    while cur <= end:
        months.append(cur)
        if cur.month == 12:
            cur = date(cur.year + 1, 1, 1)
        else:
            cur = date(cur.year, cur.month + 1, 1)
    return months

MONTHS = month_range(START_DATE, END_DATE)

# ---- Visits (EVV logs) + Claims, generated per individual per month ----
visits = []
claims = []
visit_id = 1
claim_id = 1

EVV_MISS_RATE = {"High": 0.02, "Medium": 0.06, "Low": 0.16}
OVERBILL_RATE = {"High": 0.015, "Medium": 0.05, "Low": 0.14}
DENIAL_REASONS_EVV = ["No matching EVV record", "EVV clock-in/out mismatch", "Visit outside authorized window"]
DENIAL_REASONS_AUTH = ["Exceeds monthly ISP authorization", "Service not in approved ISP", "Missing prior authorization"]

for ind in individuals:
    discipline = SITE_DISCIPLINE[ind["site_id"]]
    evv_miss_rate = EVV_MISS_RATE[discipline]
    overbill_rate = OVERBILL_RATE[discipline]

    for m in MONTHS:
        # number of service days that month for this individual, scaled to authorized hours
        avg_daily_hours = ind["monthly_authorized_hours"] / 22  # ~22 service days/month baseline
        n_visits = random.randint(18, 23)
        month_billed_total = 0.0
        month_delivered_total = 0.0

        for v in range(n_visits):
            day_offset = random.randint(0, 27)
            try:
                visit_date = date(m.year, m.month, 1 + day_offset)
            except ValueError:
                visit_date = m

            scheduled_hours = round(max(avg_daily_hours + random.uniform(-0.5, 0.5), 0.5), 2)

            # EVV verification: whether the visit has a valid matching EVV record
            evv_verified = random.random() > evv_miss_rate

            # Delivered hours per EVV (if verified) -- small natural variance
            delivered_hours = round(scheduled_hours * random.uniform(0.92, 1.03), 2) if evv_verified else 0.0

            # Billed hours: usually matches delivered, but overbilling happens
            # at a rate driven by site documentation discipline
            if random.random() < overbill_rate:
                billed_hours = round(scheduled_hours * random.uniform(1.05, 1.35), 2)
            else:
                billed_hours = delivered_hours if evv_verified else scheduled_hours  # billed without EVV backup

            is_violation = (not evv_verified) or (billed_hours > delivered_hours * 1.02)

            visits.append({
                "visit_id": visit_id,
                "individual_id": ind["individual_id"],
                "site_id": ind["site_id"],
                "visit_date": visit_date.isoformat(),
                "scheduled_hours": scheduled_hours,
                "evv_verified": int(evv_verified),
                "delivered_hours": delivered_hours,
                "billed_hours": billed_hours,
                "compliance_violation": int(is_violation),
            })

            month_billed_total += billed_hours
            month_delivered_total += delivered_hours

            # Claim generated per visit
            claim_amount = round(billed_hours * random.uniform(28, 34), 2)  # $ per unit-hour billing rate

            if is_violation:
                if not evv_verified:
                    denial_reason = random.choice(DENIAL_REASONS_EVV)
                else:
                    denial_reason = random.choice(DENIAL_REASONS_AUTH)
                claim_status = random.choices(["Denied", "Pending Review", "Paid"], weights=[0.62, 0.23, 0.15])[0]
            else:
                denial_reason = ""
                claim_status = random.choices(["Paid", "Pending Review", "Denied"], weights=[0.94, 0.05, 0.01])[0]

            claims.append({
                "claim_id": claim_id,
                "visit_id": visit_id,
                "individual_id": ind["individual_id"],
                "site_id": ind["site_id"],
                "billed_hours": billed_hours,
                "claim_amount": claim_amount,
                "claim_status": claim_status,
                "denial_reason": denial_reason,
            })

            visit_id += 1
            claim_id += 1

        # Separate check: did total monthly billed hours exceed ISP authorization?
        if month_billed_total > ind["monthly_authorized_hours"] * 1.03:
            pass  # captured implicitly via per-visit overbilling above; monthly figure used in analysis script

def write_csv(path, rows, fieldnames):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

write_csv(os.path.join(OUT_DIR, "sites.csv"), SITES, list(SITES[0].keys()))
write_csv(os.path.join(OUT_DIR, "individuals.csv"), individuals, list(individuals[0].keys()))
write_csv(os.path.join(OUT_DIR, "visits.csv"), visits, list(visits[0].keys()))
write_csv(os.path.join(OUT_DIR, "claims.csv"), claims, list(claims[0].keys()))

print(f"sites: {len(SITES)}")
print(f"individuals: {len(individuals)}")
print(f"visits: {len(visits)}")
print(f"claims: {len(claims)}")
violations = sum(v["compliance_violation"] for v in visits)
print(f"compliance violations: {violations} ({100*violations/len(visits):.1f}%)")
