"""
Synthetic dataset modeled on an insured jewelry-shipping operation
(the domain from the Jewelers Mutual Operations Analyst Intern role).

The core domain insight this dataset is built to surface: insurance
carriers price and underwrite shipments based on the SECURITY TIER of
the courier relative to the DECLARED VALUE of the shipment. A policy
violation -- routing a high-value shipment through a courier whose
security tier is too low for that value -- is a much stronger predictor
of loss/claims than carrier identity or season alone. That's a finding
that only makes sense if you understand how insured logistics actually
works, which is the point of this project.

Tables: customers, carriers, shipments, claims
"""
import random
import csv
import os
from datetime import date, timedelta

random.seed(7)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(OUT_DIR, exist_ok=True)

START_DATE = date(2024, 1, 1)
END_DATE = date(2026, 6, 30)
TOTAL_DAYS = (END_DATE - START_DATE).days

# ---- Carriers: security tier drives both suitability and cost ----
# tier_rank: 1 = Standard, 2 = Enhanced (signature required), 3 = High-Security (armored/specialty)
CARRIERS = [
    {"carrier_id": 1, "carrier_name": "USPS Registered Mail",        "tier": "Standard",      "tier_rank": 1, "sla_days": 5, "premium_rate_pct": 1.95},
    {"carrier_id": 2, "carrier_name": "UPS Next Day Air",            "tier": "Standard",      "tier_rank": 1, "sla_days": 1, "premium_rate_pct": 2.15},
    {"carrier_id": 3, "carrier_name": "FedEx Priority Overnight",    "tier": "Standard",      "tier_rank": 1, "sla_days": 1, "premium_rate_pct": 2.15},
    {"carrier_id": 4, "carrier_name": "UPS Next Day Air Early (Sig)","tier": "Enhanced",      "tier_rank": 2, "sla_days": 1, "premium_rate_pct": 1.45},
    {"carrier_id": 5, "carrier_name": "FedEx Custom Critical",       "tier": "Enhanced",      "tier_rank": 2, "sla_days": 2, "premium_rate_pct": 1.55},
    {"carrier_id": 6, "carrier_name": "Brink's Global Services",     "tier": "High-Security", "tier_rank": 3, "sla_days": 3, "premium_rate_pct": 0.95},
    {"carrier_id": 7, "carrier_name": "Malca-Amit",                  "tier": "High-Security", "tier_rank": 3, "sla_days": 4, "premium_rate_pct": 1.05},
]
CARRIER_BY_ID = {c["carrier_id"]: c for c in CARRIERS}

def required_tier_rank(value):
    """Underwriting rule of thumb modeled after real jewelry-insurance
    policy: the higher the declared value, the higher the minimum
    courier security tier required to keep coverage in good standing."""
    if value >= 50000:
        return 3  # must use High-Security
    if value >= 10000:
        return 2  # must use at least Enhanced (signature required)
    return 1      # Standard is acceptable

CUSTOMER_TYPES = ["Retailer", "Wholesaler", "Manufacturer", "Individual Collector"]
STATES = ["NY","NJ","CA","FL","IL","TX","MA","PA","GA","WA","CO","AZ"]
BUSINESS_NAME_PARTS_1 = ["Sterling","Golden","Regal","Heritage","Luxe","Crown","Windsor","Meridian","Pearl","Diamond"]
BUSINESS_NAME_PARTS_2 = ["Jewelers","Gems","Fine Jewelry","& Co.","Estate Jewelry","Diamond House","Atelier"]

N_CUSTOMERS = 260
customers = []
for cid in range(1, N_CUSTOMERS + 1):
    ctype = random.choices(CUSTOMER_TYPES, weights=[0.45, 0.2, 0.1, 0.25])[0]
    name = f"{random.choice(BUSINESS_NAME_PARTS_1)} {random.choice(BUSINESS_NAME_PARTS_2)}" if ctype != "Individual Collector" \
        else f"{random.choice(['J.','M.','A.','R.','S.','T.'])} {random.choice(['Collector','Estate','Private Client'])}"
    # risk_rating loosely correlates with how disciplined the customer is about following carrier policy
    risk_rating = random.choices(["Low", "Medium", "High"], weights=[0.55, 0.3, 0.15])[0]
    customers.append({
        "customer_id": cid,
        "business_name": name,
        "customer_type": ctype,
        "state": random.choice(STATES),
        "risk_rating": risk_rating,
    })

def seasonal_weight(d):
    # Valentine's Day run-up (Jan-Feb), Mother's Day (Apr-May), holiday season (Nov-Dec)
    if d.month in (1, 2):
        return 2.0
    if d.month in (4, 5):
        return 1.6
    if d.month in (11, 12):
        return 1.8
    return 1.0

def rand_ship_date():
    for _ in range(20):
        offset = random.randint(0, TOTAL_DAYS)
        d = START_DATE + timedelta(days=offset)
        if random.random() < seasonal_weight(d) / 2.0:
            return d
    return START_DATE + timedelta(days=random.randint(0, TOTAL_DAYS))

def sample_declared_value():
    # Heavy right tail: most shipments are modest, some are very high value
    r = random.random()
    if r < 0.55:
        return round(random.uniform(500, 9999), 2)
    elif r < 0.85:
        return round(random.uniform(10000, 49999), 2)
    elif r < 0.97:
        return round(random.uniform(50000, 149999), 2)
    else:
        return round(random.uniform(150000, 500000), 2)

N_SHIPMENTS = 5200
shipments = []
claims = []
claim_id = 1

CLAIM_REASONS_LOST = ["Lost in Transit", "Theft", "Carrier Misdelivery"]
CLAIM_REASONS_DAMAGED = ["Damaged in Transit", "Water Damage", "Crushed Packaging"]

for sid in range(1, N_SHIPMENTS + 1):
    customer = random.choice(customers)
    ship_date = rand_ship_date()
    value = sample_declared_value()
    req_tier = required_tier_rank(value)

    # Customer discipline about following carrier policy depends on risk_rating.
    # Low risk customers follow policy almost always; High risk customers cut
    # corners on carrier choice meaningfully more often.
    follow_policy_prob = {"Low": 0.94, "Medium": 0.82, "High": 0.60}[customer["risk_rating"]]

    if random.random() < follow_policy_prob:
        # pick a carrier that meets or exceeds the required tier
        eligible = [c for c in CARRIERS if c["tier_rank"] >= req_tier]
    else:
        # policy violation: pick a carrier below the required tier (if any exist below)
        below = [c for c in CARRIERS if c["tier_rank"] < req_tier]
        eligible = below if below else [c for c in CARRIERS if c["tier_rank"] >= req_tier]

    carrier = random.choice(eligible)
    policy_violation = carrier["tier_rank"] < req_tier

    premium_amount = round(value * carrier["premium_rate_pct"] / 100, 2)

    sla_days = carrier["sla_days"]
    # Peak season adds transit variability/delay risk across the board
    season_factor = seasonal_weight(ship_date)
    delay_chance = 0.06 * season_factor
    is_late = random.random() < delay_chance
    actual_transit = sla_days + (random.randint(1, 4) if is_late else random.choice([-1, 0, 0, 0, 1]))
    actual_transit = max(actual_transit, 1)

    # Loss/damage risk model -- this is the central domain insight:
    # baseline risk is low, high-value shipments are modestly more attractive
    # targets, peak season adds carrier-network strain, and POLICY VIOLATIONS
    # are by far the largest risk multiplier.
    base_risk = 0.004
    value_factor = 1.0 + (value / 400000)           # higher value -> modestly higher risk
    season_risk_factor = 1.0 + (season_factor - 1.0) * 0.5
    violation_factor = 6.0 if policy_violation else 1.0
    loss_prob = min(base_risk * value_factor * season_risk_factor * violation_factor, 0.4)

    damage_prob = loss_prob * 0.9  # damage roughly as likely as outright loss, modeled separately

    roll = random.random()
    if roll < loss_prob:
        status = "Lost"
    elif roll < loss_prob + damage_prob:
        status = "Damaged"
    elif is_late:
        status = "Delivered Late"
    else:
        status = "Delivered On-Time"

    shipments.append({
        "shipment_id": sid,
        "customer_id": customer["customer_id"],
        "carrier_id": carrier["carrier_id"],
        "ship_date": ship_date.isoformat(),
        "declared_value": value,
        "required_tier_rank": req_tier,
        "carrier_tier_rank": carrier["tier_rank"],
        "policy_violation": int(policy_violation),
        "sla_days": sla_days,
        "actual_transit_days": actual_transit,
        "premium_amount": premium_amount,
        "status": status,
    })

    if status in ("Lost", "Damaged"):
        if status == "Lost":
            reason = random.choice(CLAIM_REASONS_LOST)
            claim_amount = round(value * random.uniform(0.9, 1.0), 2)  # near-total loss
        else:
            reason = random.choice(CLAIM_REASONS_DAMAGED)
            claim_amount = round(value * random.uniform(0.15, 0.6), 2)  # partial loss

        claim_status = random.choices(["Paid", "Denied", "Pending"], weights=[0.78, 0.1, 0.12])[0]
        days_to_resolve = random.randint(7, 60) if claim_status != "Pending" else None

        claims.append({
            "claim_id": claim_id,
            "shipment_id": sid,
            "claim_reason": reason,
            "claim_amount": claim_amount,
            "claim_status": claim_status,
            "days_to_resolve": days_to_resolve if days_to_resolve is not None else "",
        })
        claim_id += 1

def write_csv(path, rows, fieldnames):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

write_csv(os.path.join(OUT_DIR, "customers.csv"), customers, list(customers[0].keys()))
write_csv(os.path.join(OUT_DIR, "carriers.csv"), CARRIERS, list(CARRIERS[0].keys()))
write_csv(os.path.join(OUT_DIR, "shipments.csv"), shipments, list(shipments[0].keys()))
write_csv(os.path.join(OUT_DIR, "claims.csv"), claims, list(claims[0].keys()))

print(f"customers: {len(customers)}")
print(f"carriers: {len(CARRIERS)}")
print(f"shipments: {len(shipments)}")
print(f"claims: {len(claims)}")
print(f"policy violations: {sum(s['policy_violation'] for s in shipments)} ({100*sum(s['policy_violation'] for s in shipments)/len(shipments):.1f}%)")
lost_damaged = sum(1 for s in shipments if s['status'] in ('Lost','Damaged'))
print(f"lost/damaged: {lost_damaged} ({100*lost_damaged/len(shipments):.1f}%)")
