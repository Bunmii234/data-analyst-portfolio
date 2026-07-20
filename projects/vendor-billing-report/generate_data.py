"""
Synthetic vendor invoice dataset built to practice the kind of vendor
billing anomaly detection common in accounts payable audits.

Design: each vendor has a contracted rate per unit (hourly rate, per-seat
license fee, etc.) for a given service category. Invoices should bill at
that contracted rate x quantity, but real vendor billing rarely does --
rates drift, quantities get padded, and duplicate invoices slip through.
The point of this dataset is to have enough realistic billing noise that
a variance/anomaly analysis actually finds something.
"""
import random
import csv
import os
from datetime import date, timedelta

random.seed(21)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(OUT_DIR, exist_ok=True)

START_DATE = date(2025, 1, 1)
END_DATE = date(2025, 12, 31)
TOTAL_DAYS = (END_DATE - START_DATE).days

CATEGORIES = ["IT Services", "Office Supplies", "Facilities", "Professional Services", "Software Licensing", "Logistics & Shipping"]

VENDORS = [
    ("Apex IT Consulting", "IT Services", 145.00, "hourly"),
    ("Meridian Systems Group", "IT Services", 130.00, "hourly"),
    ("Staples Business Advantage", "Office Supplies", 1.00, "per_unit"),
    ("OfficeMax Direct", "Office Supplies", 1.00, "per_unit"),
    ("Reliant Facilities Mgmt", "Facilities", 62.00, "hourly"),
    ("ClearView Janitorial", "Facilities", 38.00, "hourly"),
    ("Hartwell Legal Advisors", "Professional Services", 310.00, "hourly"),
    ("Beacon Consulting Partners", "Professional Services", 220.00, "hourly"),
    ("Vantage Software Inc", "Software Licensing", 42.00, "per_seat"),
    ("CloudSuite Solutions", "Software Licensing", 55.00, "per_seat"),
    ("Swift Freight Logistics", "Logistics & Shipping", 18.50, "per_shipment"),
    ("Regional Courier Co", "Logistics & Shipping", 14.00, "per_shipment"),
]

N_INVOICES = 1400
invoices = []
invoice_id = 1

for i in range(N_INVOICES):
    vendor_name, category, contracted_rate, unit_type = random.choice(VENDORS)
    invoice_date = START_DATE + timedelta(days=random.randint(0, TOTAL_DAYS))

    if unit_type == "hourly":
        quantity = round(random.uniform(4, 80), 1)
    elif unit_type == "per_unit":
        quantity = random.randint(20, 800)
    elif unit_type == "per_seat":
        quantity = random.randint(5, 250)
    else:  # per_shipment
        quantity = random.randint(10, 400)

    expected_amount = round(contracted_rate * quantity, 2)

    # Decide the "fate" of this invoice
    fate = random.choices(
        ["clean", "rate_drift_small", "rate_drift_large", "quantity_padding", "duplicate", "late_fee_undisclosed"],
        weights=[0.68, 0.12, 0.05, 0.06, 0.04, 0.05],
    )[0]

    billed_rate = contracted_rate
    billed_quantity = quantity
    note = ""

    if fate == "rate_drift_small":
        # small, easy-to-miss rate creep (e.g. vendor quietly raised rates)
        billed_rate = round(contracted_rate * random.uniform(1.02, 1.06), 2)
        note = "rate above contract"
    elif fate == "rate_drift_large":
        # a clear, large rate error -- data entry mistake or renegotiation not reflected in contract
        billed_rate = round(contracted_rate * random.uniform(1.15, 1.40), 2)
        note = "rate significantly above contract"
    elif fate == "quantity_padding":
        billed_quantity = round(quantity * random.uniform(1.08, 1.25), 1)
        note = "billed quantity exceeds recorded usage"
    elif fate == "late_fee_undisclosed":
        note = "late fee applied without prior notice"

    billed_amount = round(billed_rate * billed_quantity, 2)
    if fate == "late_fee_undisclosed":
        billed_amount = round(billed_amount + random.uniform(25, 150), 2)

    variance = round(billed_amount - expected_amount, 2)

    invoices.append({
        "invoice_id": f"INV{invoice_id:05d}",
        "vendor_name": vendor_name,
        "category": category,
        "invoice_date": invoice_date.isoformat(),
        "unit_type": unit_type,
        "contracted_rate": contracted_rate,
        "billed_rate": billed_rate,
        "quantity": billed_quantity,
        "expected_amount": expected_amount,
        "billed_amount": billed_amount,
        "variance": variance,
        "flag": fate,
        "note": note,
        "approval_status": random.choices(["Approved", "Pending Review", "Rejected"], weights=[0.82, 0.13, 0.05])[0],
    })
    invoice_id += 1

    if fate == "duplicate":
        # exact duplicate invoice, different invoice_id, submitted a few days later
        dup_date = invoice_date + timedelta(days=random.randint(2, 10))
        invoices.append({
            "invoice_id": f"INV{invoice_id:05d}",
            "vendor_name": vendor_name,
            "category": category,
            "invoice_date": dup_date.isoformat(),
            "unit_type": unit_type,
            "contracted_rate": contracted_rate,
            "billed_rate": billed_rate,
            "quantity": billed_quantity,
            "expected_amount": expected_amount,
            "billed_amount": billed_amount,
            "variance": variance,
            "flag": "duplicate",
            "note": "likely duplicate of " + f"INV{invoice_id-1:05d}",
            "approval_status": random.choices(["Approved", "Pending Review"], weights=[0.6, 0.4])[0],
        })
        invoice_id += 1

with open(os.path.join(OUT_DIR, "vendor_invoices.csv"), "w", newline="") as f:
    fieldnames = list(invoices[0].keys())
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(invoices)

print(f"invoices: {len(invoices)}")
from collections import Counter
print("flags:", Counter(i["flag"] for i in invoices))
total_variance = sum(i["variance"] for i in invoices if i["variance"] > 0)
print(f"total positive variance (overbilled): ${total_variance:,.2f}")
