"""
Generates two DELIBERATELY MESSY, independently-formatted exports of the
same underlying set of banking transactions:

  data/raw/internal_ledger_raw.csv   -- how the bank's internal GL/ledger
                                         system exports transactions
  data/raw/bank_statement_raw.csv    -- how the correspondent bank's
                                         settlement/statement feed exports
                                         the "same" transactions

This mirrors a real banking data-quality problem (and the Quintrix Data
Analyst Intern work this project is modeled on): two systems that are
supposed to agree, but don't, because of format drift, timing
differences, duplicate postings, and a handful of genuine discrepancies
that need to be found and explained. The point of this project is the
CLEANING AND RECONCILIATION CODE in reconcile.py, not this generator --
this script exists only to produce realistic mess to clean up.

Messiness deliberately introduced:
  - Three different date formats across the two systems (and mixed
    within the bank file, simulating a batch feed from multiple sources)
  - Account numbers formatted differently (dashes, spaces, leading zeros)
  - Amounts as strings with $ signs, commas, parentheses for negatives
  - Inconsistent debit/credit sign convention
  - Whitespace and case inconsistency in reference numbers
  - Duplicate postings in the ledger (double-keyed entries)
  - Timing differences: some transactions post 1-3 days apart between
    systems (in-transit items)
  - Bank-only items: fees/interest the bank recorded that never hit the
    internal ledger
  - Ledger-only items: internal adjustments/reversals never sent to the
    bank
  - A small number of genuine amount discrepancies (the real errors this
    process should catch)
"""
import random
import csv
import os
from datetime import date, timedelta

random.seed(11)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

START_DATE = date(2025, 1, 1)
END_DATE = date(2025, 6, 30)
TOTAL_DAYS = (END_DATE - START_DATE).days

N_TRUE_TRANSACTIONS = 6000
BRANCHES = ["0112", "0245", "0389", "0501", "0678"]
TXN_TYPES_DESC = [
    ("ACH Credit", "Payroll Deposit"),
    ("ACH Debit", "Vendor Payment"),
    ("Wire Transfer", "Outgoing Wire"),
    ("Wire Transfer", "Incoming Wire"),
    ("Check Deposit", "Check Deposit"),
    ("Debit Card", "POS Purchase"),
    ("ATM Withdrawal", "ATM Cash Withdrawal"),
    ("Internal Transfer", "Account Transfer"),
]

def rand_account():
    return random.randint(1000000000, 9999999999)  # 10-digit account number

def rand_date():
    return START_DATE + timedelta(days=random.randint(0, TOTAL_DAYS))

def fmt_date_ledger(d):
    # Ledger system always exports ISO format
    return d.isoformat()

def fmt_date_bank(d):
    # Bank feed is inconsistent -- mixes two formats depending on batch source
    if random.random() < 0.6:
        return d.strftime("%m/%d/%Y")
    else:
        return d.strftime("%d-%b-%Y")  # e.g. 14-Mar-2025

def fmt_account_ledger(acct):
    return str(acct)  # plain digits

def fmt_account_bank(acct):
    s = str(acct)
    # Bank feed formats as XXX-XXX-XXXX with occasional leading/trailing whitespace
    formatted = f"{s[:3]}-{s[3:6]}-{s[6:]}"
    if random.random() < 0.08:
        formatted = " " + formatted + " "
    return formatted

def fmt_amount_ledger(amount, direction):
    # Ledger exports signed decimal with 2 decimal places, Debit = negative
    signed = -abs(amount) if direction == "Debit" else abs(amount)
    return f"{signed:.2f}"

def fmt_amount_bank(amount, direction):
    # Bank feed uses accounting notation: parentheses for debits, $ and
    # commas, and occasionally omits the sign convention correctly
    val = abs(amount)
    s = f"${val:,.2f}"
    if direction == "Debit":
        s = f"({s})"
    return s

def rand_ref(i):
    return f"TXN{i:07d}"

def fmt_ref_bank(ref):
    # bank feed sometimes lowercases or pads with whitespace
    r = ref
    if random.random() < 0.15:
        r = r.lower()
    if random.random() < 0.1:
        r = " " + r
    return r

ledger_rows = []
bank_rows = []

for i in range(1, N_TRUE_TRANSACTIONS + 1):
    ref = rand_ref(i)
    acct = rand_account()
    txn_type, desc = random.choice(TXN_TYPES_DESC)
    direction = "Debit" if txn_type in ("ACH Debit", "Wire Transfer", "Debit Card", "ATM Withdrawal") and random.random() < 0.9 else random.choice(["Debit", "Credit"])
    if txn_type == "ACH Credit" or txn_type == "Check Deposit":
        direction = "Credit"
    amount = round(random.uniform(25, 45000), 2)
    txn_date = rand_date()
    branch = random.choice(BRANCHES)

    # Decide the "fate" of this transaction across the two systems
    fate = random.choices(
        ["clean_match", "timing_diff", "amount_discrepancy", "ledger_only", "bank_only", "ledger_duplicate"],
        weights=[0.80, 0.09, 0.02, 0.03, 0.03, 0.03],
    )[0]

    ledger_date = txn_date
    bank_date = txn_date
    ledger_amount = amount
    bank_amount = amount

    if fate == "timing_diff":
        # Bank posts 1-3 days after the ledger records it (in-transit item)
        bank_date = txn_date + timedelta(days=random.randint(1, 3))
    elif fate == "amount_discrepancy":
        # A genuine error: bank settled a slightly different amount
        # (e.g. a fee not reflected, or a data entry error upstream)
        bank_amount = round(amount + random.choice([-1, 1]) * random.uniform(5, 250), 2)

    # Ledger row (always written unless bank_only)
    if fate != "bank_only":
        ledger_rows.append({
            "TxnRef": ref,
            "AccountNumber": fmt_account_ledger(acct),
            "PostDate": fmt_date_ledger(ledger_date),
            "Amount": fmt_amount_ledger(ledger_amount, direction),
            "Direction": direction,
            "Description": desc,
            "BranchCode": branch,
        })
        if fate == "ledger_duplicate":
            # Simulate an accidental double-post in the ledger system
            ledger_rows.append({
                "TxnRef": ref,
                "AccountNumber": fmt_account_ledger(acct),
                "PostDate": fmt_date_ledger(ledger_date),
                "Amount": fmt_amount_ledger(ledger_amount, direction),
                "Direction": direction,
                "Description": desc,
                "BranchCode": branch,
            })

    # Bank row (always written unless ledger_only)
    if fate != "ledger_only":
        bank_rows.append({
            "RefNumber": fmt_ref_bank(ref),
            "AcctNumber": fmt_account_bank(acct),
            "StatementDate": fmt_date_bank(bank_date),
            "Amount": fmt_amount_bank(bank_amount, direction),
            "TxnType": txn_type,
            "Memo": desc.upper() if random.random() < 0.3 else desc,
        })

# Add pure bank-side items with no ledger counterpart at all (fees/interest)
N_BANK_FEES = 140
FEE_TYPES = [("Monthly Maintenance Fee", "Service Charge"), ("Wire Fee", "Service Charge"),
             ("Interest Credit", "Interest Payment"), ("NSF Fee", "Service Charge"),
             ("Overdraft Fee", "Service Charge")]
for j in range(N_BANK_FEES):
    desc, txn_type = random.choice(FEE_TYPES)
    acct = rand_account()
    d = rand_date()
    amount = round(random.uniform(5, 75), 2)
    direction = "Credit" if desc == "Interest Credit" else "Debit"
    bank_rows.append({
        "RefNumber": fmt_ref_bank(f"FEE{j:05d}"),
        "AcctNumber": fmt_account_bank(acct),
        "StatementDate": fmt_date_bank(d),
        "Amount": fmt_amount_bank(amount, direction),
        "TxnType": txn_type,
        "Memo": desc,
    })

random.shuffle(ledger_rows)
random.shuffle(bank_rows)

def write_csv(path, rows, fieldnames):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

write_csv(os.path.join(RAW_DIR, "internal_ledger_raw.csv"), ledger_rows,
          ["TxnRef","AccountNumber","PostDate","Amount","Direction","Description","BranchCode"])
write_csv(os.path.join(RAW_DIR, "bank_statement_raw.csv"), bank_rows,
          ["RefNumber","AcctNumber","StatementDate","Amount","TxnType","Memo"])

print(f"ledger rows: {len(ledger_rows)}")
print(f"bank rows: {len(bank_rows)}")
