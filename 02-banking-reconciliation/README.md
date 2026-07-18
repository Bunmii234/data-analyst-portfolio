# Banking Transaction Reconciliation

**Focus of this project: data prep and cleaning.** There is no
dashboard here on purpose. The deliverable is `reconcile.py` — the
cleaning and matching logic — because that's the work a banking data
analyst actually does most often, and it's the work that generic
portfolio projects almost always skip in favor of a chart. Modeled on
my Data Analyst Intern work in Banking & Financial Services at Quintrix
Solutions (optimizing SQL against 50K+ records, resolving 15% of data
discrepancies in banking datasets).

## The problem

Two systems track the same transactions and are supposed to agree: an
internal ledger/GL export and a correspondent bank's settlement feed.
In practice they never match cleanly, because:

- The two systems format **dates** differently (ledger: ISO `YYYY-MM-DD`;
  bank feed: a mix of `MM/DD/YYYY` and `DD-Mon-YYYY` depending on which
  upstream batch produced the row)
- **Account numbers** are formatted differently (`5685743966` vs
  `568-574-3966`, sometimes with stray whitespace)
- **Amounts** are represented differently (ledger: signed decimal;
  bank: accounting notation like `($1,234.56)` for debits)
- **Reference numbers** have inconsistent case and whitespace
- A handful of transactions were **double-posted** in the ledger
- Some transactions post to each system **1-3 days apart** (in-transit
  items — not errors)
- The bank charges **fees/interest** that never get sent to the
  internal ledger (expected, not errors)
- And a small number of transactions have **genuine amount
  discrepancies** — the real errors this whole process exists to catch

Naively joining the two files on reference number would fail outright
(formats don't match) or silently miscount everything (duplicates,
sign conventions). The cleaning has to happen first, and has to be
deliberate about which mismatches are real problems vs. expected noise.

## What `reconcile.py` actually does

1. **Parses dates defensively** — tries multiple known formats rather
   than assuming one, since a single-format parser would silently
   misparse or crash on ~40% of the bank feed.
2. **Normalizes account numbers** by stripping all non-digit characters.
3. **Normalizes amounts** — strips `$` and commas, and correctly
   converts parenthesized accounting notation to negative values (the
   single most common real-world gotcha in financial CSVs).
4. **Deduplicates the ledger** before matching, so accidental
   double-postings don't corrupt the reconciliation.
5. **Matches on cleaned reference number + account number**, then
   classifies every line into one of six categories — reconciled clean,
   reconciled with a timing difference, amount discrepancy, ledger-only,
   bank-only, or expected bank fee — rather than a flat "matched /
   unmatched" binary that would bury the interesting cases.

## Results (from the live run)

| Category | Count | % |
|---|---|---|
| Reconciled | 4,957 | 80.7% |
| Reconciled (timing difference) | 585 | 9.5% |
| Bank-Only (investigate) | 182 | 3.0% |
| Ledger-Only (investigate) | 155 | 2.5% |
| Bank Fee/Interest (expected, no ledger entry) | 140 | 2.3% |
| **Amount Discrepancy (investigate)** | **121** | **2.0%** |

- 187 duplicate ledger postings were detected and removed before
  matching (6,005 raw rows → 5,818 clean rows).
- **$16,696.54** in flagged amount discrepancies — the genuine errors
  worth escalating, isolated from formatting noise.
- **$3.63M** in ledger-only items (recorded internally, never confirmed
  at the bank) and **$3.61M** in bank-only items (settled at the bank,
  never recorded internally) — both flagged for investigation rather
  than silently dropped.

The key move here isn't the match rate (90.2% reconcile cleanly or with
an expected timing lag) — it's that the remaining ~10% is split into
categories with different next actions: fees just need to be booked,
timing differences need no action at all, and discrepancies/unmatched
items need to go to someone's desk. Collapsing all of that into one
"unreconciled" bucket, which a shallower project would do, is exactly
the kind of shallow analysis this project is trying not to be.

## Files

```
02-banking-reconciliation/
├── generate_data.py              # builds the two messy raw exports (for reproducibility)
├── reconcile.py                  # the actual project: cleaning + reconciliation logic
├── data/
│   ├── raw/                      # internal_ledger_raw.csv, bank_statement_raw.csv (messy, as received)
│   └── clean/                    # ledger_clean.csv, bank_clean.csv, reconciliation_report.csv
└── analysis/
    └── summary.md                # auto-generated run summary with live counts
```

## How to run

```bash
python3 generate_data.py   # regenerates the messy raw exports
python3 reconcile.py       # cleans, reconciles, and writes the report + summary
```

## Skills demonstrated

Defensive parsing of inconsistent real-world formats (dates, currency,
account numbers), deduplication logic, key normalization for joining
across systems with different conventions, and — the part that matters
most — classifying discrepancies into actionable categories instead of
reporting a single pass/fail match rate.
