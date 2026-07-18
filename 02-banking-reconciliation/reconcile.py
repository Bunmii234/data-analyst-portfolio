"""
BANKING TRANSACTION RECONCILIATION
===================================
This is the centerpiece of the project: cleaning two independently
formatted, messy exports of the same underlying transactions, then
reconciling them and classifying every discrepancy into an actionable
category. Data prep and matching logic matter more here than any chart
would -- there are no charts in this project by design.

Inputs:
  data/raw/internal_ledger_raw.csv  -- internal GL export
  data/raw/bank_statement_raw.csv   -- correspondent bank settlement feed

Outputs:
  data/clean/ledger_clean.csv
  data/clean/bank_clean.csv
  data/clean/reconciliation_report.csv
  analysis/summary.md   (written by this script with live numbers)
"""
import csv
import os
import re
from datetime import datetime
from decimal import Decimal, InvalidOperation

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
CLEAN_DIR = os.path.join(BASE_DIR, "data", "clean")
ANALYSIS_DIR = os.path.join(BASE_DIR, "analysis")
os.makedirs(CLEAN_DIR, exist_ok=True)
os.makedirs(ANALYSIS_DIR, exist_ok=True)


# ---------------------------------------------------------------------
# STEP 1: CLEANING PRIMITIVES
# Each of these exists because the raw data broke a naive parse. That's
# the point -- every function here is a documented response to a real
# format inconsistency found in the source files.
# ---------------------------------------------------------------------

def clean_account_number(raw):
    """Strip whitespace and any non-digit formatting (dashes, spaces)
    so ledger '5685743966' and bank ' 568-574-3966 ' compare equal."""
    return re.sub(r"\D", "", raw.strip())


def clean_ref(raw):
    """Normalize reference numbers to uppercase, no surrounding
    whitespace -- the bank feed randomly lowercases ~15% of refs and
    pads ~10% with leading whitespace."""
    return raw.strip().upper()


def clean_ledger_date(raw):
    """Ledger system consistently exports ISO 8601 (YYYY-MM-DD)."""
    return datetime.strptime(raw.strip(), "%Y-%m-%d").date()


def clean_bank_date(raw):
    """Bank feed mixes two date formats depending on which upstream
    batch produced the row: MM/DD/YYYY and DD-Mon-YYYY. Try both rather
    than assuming a single format -- a naive single-format parse would
    silently fail (or worse, silently misparse) on ~40% of rows."""
    raw = raw.strip()
    for fmt in ("%m/%d/%Y", "%d-%b-%Y"):
        try:
            return datetime.strptime(raw, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Unrecognized date format: {raw!r}")


def clean_ledger_amount(raw):
    """Ledger amount is already a signed decimal string (Debit =
    negative). Just parse it -- but still guard against stray
    whitespace, which showed up in a handful of rows."""
    return Decimal(raw.strip())


def clean_bank_amount(raw):
    """Bank feed uses accounting notation: '$1,234.56' for credits and
    '($1,234.56)' for debits. Strip the currency symbol and thousands
    separators, and convert parenthesized values to negative -- the
    single most common real-world gotcha in financial CSV exports."""
    s = raw.strip()
    is_negative = s.startswith("(") and s.endswith(")")
    s = s.strip("()").replace("$", "").replace(",", "").strip()
    try:
        val = Decimal(s)
    except InvalidOperation:
        raise ValueError(f"Could not parse amount: {raw!r}")
    return -val if is_negative else val


# ---------------------------------------------------------------------
# STEP 2: LOAD + CLEAN EACH SOURCE
# ---------------------------------------------------------------------

def load_and_clean_ledger():
    rows = []
    with open(os.path.join(RAW_DIR, "internal_ledger_raw.csv")) as f:
        for r in csv.DictReader(f):
            rows.append({
                "txn_ref": clean_ref(r["TxnRef"]),
                "account_number": clean_account_number(r["AccountNumber"]),
                "post_date": clean_ledger_date(r["PostDate"]),
                "amount": clean_ledger_amount(r["Amount"]),
                "direction": r["Direction"].strip(),
                "description": r["Description"].strip(),
                "branch_code": r["BranchCode"].strip(),
            })
    return rows


def load_and_clean_bank(fee_ref_prefix="FEE"):
    rows = []
    with open(os.path.join(RAW_DIR, "bank_statement_raw.csv")) as f:
        for r in csv.DictReader(f):
            ref = clean_ref(r["RefNumber"])
            rows.append({
                "ref_number": ref,
                "account_number": clean_account_number(r["AcctNumber"]),
                "statement_date": clean_bank_date(r["StatementDate"]),
                "amount": clean_bank_amount(r["Amount"]),
                "txn_type": r["TxnType"].strip(),
                "memo": r["Memo"].strip(),
                "is_bank_originated_fee": ref.startswith(fee_ref_prefix),
            })
    return rows


# ---------------------------------------------------------------------
# STEP 3: DEDUPLICATE THE LEDGER
# A handful of transactions were accidentally double-posted in the
# internal ledger (same ref, same everything, appearing twice). Flag
# and remove the duplicate copy before matching -- otherwise every
# duplicate would either double-count in the reconciliation or produce
# a false "ledger amount doesn't match bank amount" (2x vs 1x) error.
# ---------------------------------------------------------------------

def dedupe_ledger(ledger_rows):
    seen = {}
    deduped = []
    duplicates_flagged = []
    for row in ledger_rows:
        key = (row["txn_ref"], row["account_number"], row["amount"], row["direction"])
        if key in seen:
            duplicates_flagged.append(row)
        else:
            seen[key] = row
            deduped.append(row)
    return deduped, duplicates_flagged


# ---------------------------------------------------------------------
# STEP 4: RECONCILE
# Match on cleaned txn_ref + account_number (the shared key across both
# systems once normalized). Classify each matched pair by whether the
# amount and date agree; classify unmatched rows by which side they
# came from.
# ---------------------------------------------------------------------

def reconcile(ledger_rows, bank_rows):
    bank_by_ref = {}
    for row in bank_rows:
        bank_by_ref.setdefault(row["ref_number"], []).append(row)

    report = []
    matched_bank_refs = set()

    for l in ledger_rows:
        candidates = bank_by_ref.get(l["txn_ref"], [])
        # Prefer a candidate on the same account; fall back to first available
        match = next((b for b in candidates if b["account_number"] == l["account_number"]), None)
        if match is None and candidates:
            match = candidates[0]  # account mismatch is itself worth flagging

        if match is None:
            report.append({
                "txn_ref": l["txn_ref"], "account_number": l["account_number"],
                "ledger_amount": l["amount"], "bank_amount": "",
                "ledger_date": l["post_date"], "bank_date": "",
                "category": "Ledger-Only (Investigate)",
                "note": "No matching bank record found for this ledger entry.",
            })
            continue

        matched_bank_refs.add(id(match))
        amount_diff = l["amount"] - match["amount"]
        date_diff_days = (match["statement_date"] - l["post_date"]).days

        if match["account_number"] != l["account_number"]:
            category = "Account Mismatch (Investigate)"
            note = f"Ledger account {l['account_number']} vs bank account {match['account_number']}."
        elif abs(amount_diff) > Decimal("0.01"):
            category = "Amount Discrepancy (Investigate)"
            note = f"Ledger {l['amount']} vs bank {match['amount']}, diff {amount_diff}."
        elif date_diff_days != 0:
            category = "Reconciled (Timing Difference)"
            note = f"Posted {date_diff_days} day(s) apart -- in-transit item, not an error."
        else:
            category = "Reconciled"
            note = ""

        report.append({
            "txn_ref": l["txn_ref"], "account_number": l["account_number"],
            "ledger_amount": l["amount"], "bank_amount": match["amount"],
            "ledger_date": l["post_date"], "bank_date": match["statement_date"],
            "category": category, "note": note,
        })

    # Bank rows with no ledger counterpart
    for row in bank_rows:
        if id(row) in matched_bank_refs:
            continue
        if row["is_bank_originated_fee"]:
            category = "Bank Fee/Interest (No Ledger Entry Expected)"
            note = "Bank-originated item (fee/interest) -- needs to be booked to the ledger, not an error."
        else:
            category = "Bank-Only (Investigate)"
            note = "No matching ledger record found for this bank transaction."
        report.append({
            "txn_ref": row["ref_number"], "account_number": row["account_number"],
            "ledger_amount": "", "bank_amount": row["amount"],
            "ledger_date": "", "bank_date": row["statement_date"],
            "category": category, "note": note,
        })

    return report


def write_csv(path, rows, fieldnames):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main():
    ledger_raw = load_and_clean_ledger()
    bank_rows = load_and_clean_bank()

    ledger_rows, duplicates = dedupe_ledger(ledger_raw)

    write_csv(os.path.join(CLEAN_DIR, "ledger_clean.csv"), ledger_rows,
              ["txn_ref","account_number","post_date","amount","direction","description","branch_code"])
    write_csv(os.path.join(CLEAN_DIR, "bank_clean.csv"), bank_rows,
              ["ref_number","account_number","statement_date","amount","txn_type","memo","is_bank_originated_fee"])

    write_csv(os.path.join(CLEAN_DIR, "duplicate_postings_removed.csv"), duplicates,
              ["txn_ref","account_number","post_date","amount","direction","description","branch_code"])

    report = reconcile(ledger_rows, bank_rows)
    write_csv(os.path.join(CLEAN_DIR, "reconciliation_report.csv"), report,
              ["txn_ref","account_number","ledger_amount","bank_amount","ledger_date","bank_date","category","note"])

    # ---- Summary stats ----
    from collections import Counter
    cat_counts = Counter(r["category"] for r in report)
    total = len(report)

    discrepancy_dollar_total = sum(
        abs(Decimal(str(r["ledger_amount"])) - Decimal(str(r["bank_amount"])))
        for r in report if r["category"] == "Amount Discrepancy (Investigate)"
    )
    ledger_only_dollar = sum(abs(r["ledger_amount"]) for r in report if r["category"] == "Ledger-Only (Investigate)")
    bank_only_dollar = sum(abs(r["bank_amount"]) for r in report if r["category"] == "Bank-Only (Investigate)")

    lines = []
    lines.append("# Reconciliation Summary\n")
    lines.append(f"Ledger rows (raw): {len(ledger_raw)}  |  Duplicate postings removed: {len(duplicates)}")
    lines.append(f"Ledger rows (clean, deduped): {len(ledger_rows)}")
    lines.append(f"Bank rows: {len(bank_rows)}")
    lines.append(f"Total reconciliation lines: {total}\n")
    lines.append("## By category\n")
    for cat, n in cat_counts.most_common():
        lines.append(f"- **{cat}**: {n} ({100*n/total:.1f}%)")
    lines.append("")
    lines.append(f"Total $ in amount discrepancies flagged for investigation: ${discrepancy_dollar_total:,.2f}")
    lines.append(f"Total $ in ledger-only (unrecorded at bank) items: ${ledger_only_dollar:,.2f}")
    lines.append(f"Total $ in bank-only (unrecorded in ledger, excluding fees) items: ${bank_only_dollar:,.2f}")

    with open(os.path.join(ANALYSIS_DIR, "summary.md"), "w") as f:
        f.write("\n".join(lines))

    print("\n".join(lines))


if __name__ == "__main__":
    main()
