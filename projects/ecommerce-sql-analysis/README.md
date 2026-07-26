# E-Commerce Business Performance Analysis (SQL)

An end-to-end SQL analysis of an online retail business, answering six
concrete business questions using nothing but SQL against a relational
dataset. Built to demonstrate query design, business framing, and the
judgment to know when a metric needs a caveat.

## Dataset

Synthetic e-commerce dataset (`data/ecommerce.db`, SQLite) covering
Jan 2024 - Jun 2026:

| Table | Rows | Description |
|---|---|---|
| `customers` | 1,200 | Signup date, city/state, acquisition channel, segment (New/Returning/VIP) |
| `products` | 24 | 5 categories, unit price, unit cost |
| `orders` | 3,436 | Order date, channel, status (Completed/Cancelled/Returned), total |
| `order_items` | 8,605 | Line items with quantity, discount, line total |

CSVs of the same tables are also included for portability. The dataset was
generated with realistic seasonality (holiday spike in Nov-Dec, summer
bump in July), segment-driven purchase frequency, and category-level
return/cancellation noise, so the SQL has real patterns to surface rather
than random data.

## The hard part

Honestly, all three of the trickier queries gave me trouble in different
ways. The `LAG`/cohort queries (03 and 04) took the longest to get the
syntax and join logic right — window functions weren't something I'd
used much before this. Designing the RFM/segmentation query meant
deciding what actually counts as "VIP" vs "Returning" in SQL terms, which
took some trial and error against the raw data before the buckets looked
right. And the cohort right-censoring issue (query 04) wasn't something
I spotted immediately — the first version of that query made recent
cohorts look like a retention problem, and it took a while to realize the
real explanation was just that those customers hadn't had time to
reorder yet, not that anything was actually wrong.

## Business questions answered

Each query lives in `sql/` as a standalone, commented `.sql` file.

1. **`01_monthly_revenue_trend.sql`** — Revenue and order volume by month, with month-over-month growth.
2. **`02_top_products_by_revenue_and_margin.sql`** — Top 10 products by revenue, cross-checked against gross margin.
3. **`03_customer_segmentation_rfm.sql`** — Revenue contribution and spend per customer by segment.
4. **`04_repeat_purchase_rate_by_cohort.sql`** — Repeat purchase rate by signup cohort month.
5. **`05_channel_performance.sql`** — Revenue, AOV, and revenue-per-customer by acquisition channel.
6. **`06_cancellation_return_rate_by_category.sql`** — Cancellation/return rate by product category.

## Key findings

**Revenue is seasonal and growing.** Monthly revenue climbs from ~$430 in
Jan 2024 to a steady $27K-$34K/month by late 2025 through mid-2026, with
clear holiday peaks (Dec 2024: +32% MoM, Dec 2025: +17% MoM). This mostly
reflects the customer base scaling up over the period rather than a
seasonal swing in an already-mature base — worth flagging to stakeholders
so growth isn't mistaken for pure seasonality.

**Revenue concentrates in "Returning" and "VIP" segments.** Returning and
VIP customers are only 52% of customers (627 of 1,200) but drive 79.5% of
completed revenue. VIPs alone average $1,293 lifetime revenue per
customer vs. $301 for New customers — a ~4.3x gap that makes the case for
retention/loyalty investment over pure acquisition spend.

**Best-sellers are also the most profitable.** The top revenue product
(Smart Watch, $94.8K) also carries a healthy 61.2% margin, and every item
in the top 10 sits between 55-69% margin — no red flags of a "loss-leader
best-seller" in this dataset, which is itself a useful negative finding
(confirms pricing strategy isn't quietly eroding margin on hero products).

**Repeat purchase rate hovers around 60-80% for mature cohorts** (customers
who signed up more than ~4 months before the data cutoff), but drops off
sharply for cohorts from Feb 2026 onward. That drop is **not** a real
retention problem — those customers simply haven't had enough time since
signup to place a second order before the data window ends (right-censoring).
Any real analysis needs to exclude cohorts younger than the typical
repeat-purchase window when reporting this metric.

**Paid Search and Email are the strongest channels**, both by total
revenue (~$130K each) and revenue per customer (~$654-694), meaningfully
ahead of Direct ($560/customer). Organic Search has the fewest customers
but a competitive AOV ($233.80), suggesting it's a smaller but efficient
channel worth not deprioritizing.

**Return/cancellation rates are fairly uniform across categories**
(11.0%-12.1%), with Sports & Outdoors and Apparel slightly higher. No
category is a clear outlier, so this doesn't point to a specific quality
problem — more likely a baseline "cost of doing business" rate worth
monitoring for drift rather than acting on immediately.

## How to reproduce

```bash
# From this folder, using Python (no sqlite3 CLI required):
python3 -c "
import sqlite3
conn = sqlite3.connect('data/ecommerce.db')
print(conn.execute(open('sql/01_monthly_revenue_trend.sql').read()).fetchall())
"
```

Or open `data/ecommerce.db` in any SQLite browser (e.g., DB Browser for
SQLite, TablePlus, or the SQLite VS Code extension) and run the queries
in `sql/` directly.

## Skills demonstrated

Window functions (`LAG`), multi-table joins, CTEs, cohort analysis,
aggregate + derived metrics, and — importantly — calling out a metric
artifact (cohort right-censoring) rather than reporting it at face value.
