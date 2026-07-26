# E-Commerce Performance Dashboard (Interactive)

A self-contained, interactive HTML dashboard built to answer the same
kind of question a marketing or ops stakeholder would ask in a standup:
"where is revenue coming from, and is it healthy?" No server, no
install — open `dashboard.html` in any browser.

## What it shows

- **KPI cards**: total revenue, order count, average order value, and
  order volume — all recalculated live as filters change.
- **Monthly revenue trend** (line chart) — spot growth and seasonality.
- **Revenue by category** (doughnut) — composition of the business.
- **Revenue by channel** (bar) — which acquisition channels earn their
  keep.
- **Revenue by customer segment** (bar) — New vs. Returning vs. VIP.
- **Top 8 products by revenue** (bar) — best sellers at a glance.
- **Sortable category x channel table** — the detail view beneath the
  charts, click any header to re-sort.

## Filters

Channel, customer segment, product category, and order status (defaults
to "Completed" — cancelled/returned orders are excluded from revenue by
default, matching how the business would actually report it, but can be
switched to "All Statuses" to inspect cancellation/return patterns).
Filters compose (AND logic) and update every card, chart, and the table
together.

## Data

Uses the same synthetic e-commerce dataset as the SQL analysis project
(`../01-sql-business-analysis`) — 8,605 order line items across 3,436
orders, Jan 2024–Jun 2026. Source CSVs are in `data/` for reference; the
dashboard itself has the data embedded directly in the HTML (~800KB),
so it works fully offline with no fetch calls.

## Note on the "Unique Customers" KPI

That card currently uses order count as a proxy rather than a true
distinct-customer count, since customer ID isn't carried into the
order-item-level table used for filtering. A production version would
join in `customer_id` for an accurate figure — flagging this here is
intentional: knowing the limits of your own dashboard is itself a
data-analyst skill worth demonstrating.

## How to use

Just open `dashboard.html` in a browser — double-click the file or drag
it into a browser tab. No build step, no dependencies beyond a CDN load
of Chart.js.

## Swapping in real data

Replace the `RAW` array assignment in the `<script>` block with your own
data in the same column order:

```
[order_id, date, channel, segment, category, product, status, quantity, line_total]
```

Re-open the file — no other changes needed.

## Skills demonstrated

Dashboard design (KPI-first layout), Chart.js, client-side filtering
logic, sortable tables, and being upfront about a metric's limitations
rather than presenting an approximation as exact.
