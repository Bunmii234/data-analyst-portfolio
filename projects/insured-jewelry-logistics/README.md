# Insured Jewelry Logistics Dashboard

**Focus of this project: domain expertise.** The point isn't the chart
library — it's that the metrics and the flagged-shipment list only make
sense if you understand how insured, high-value logistics actually
works. This is modeled on the world I worked in as an Operations Analyst
Intern at a jewelry insurer (Excel/Power Query cleaning of shipping and
carrier data, Tableau/Power BI dashboards on logistics bottlenecks).

## The domain insight this is built around

In general e-commerce logistics, the question is usually "did it arrive
on time?" In **insured** logistics, the question that actually matters
is: **was this shipment's declared value appropriately matched to the
courier's security tier?** A $200K diamond parcel sent via standard
UPS ground and a $200K parcel sent via Brink's armored transport carry
wildly different risk profiles, even if both arrive "on time." Treating
them the same — which a generic logistics dashboard would do — misses
the entire point of underwriting.

## The hard part

Three things slowed this one down, honestly. First, figuring out where
the carrier-tier thresholds should actually sit ($10K, $50K) took some
back and forth — it's easy to state a rule, harder to pick cutoffs that
produce a realistic violation rate instead of an obviously-fake one.
Second, the loss ratio math (claims paid / premium written, then
splitting it by carrier tier) took a bit to get right, especially once
I noticed the Enhanced-tier number looked inflated and had to figure out
why before deciding it was a small-sample issue rather than a real
finding. Third — plainly — I'm still building up my JavaScript, so the
Chart.js filtering logic in the dashboard took longer for me than the
analysis side did. That's an area I'm actively working on, not something
I'd claim to have mastered.

This dataset encodes a policy rule that mirrors how jewelry-transit
insurance actually prices risk: shipments under $10K can use any
carrier; $10K–$50K requires at least a signature-required "Enhanced"
service; $50K+ requires a "High-Security" carrier (armored transport or
a specialty valuables courier like Brink's or Malca-Amit). A **policy
violation** is a shipment where the carrier tier used was below what
the declared value required.

## Key findings (from the live data)

**Policy violations are rare but disproportionately costly.** Only
6.2% of shipments (321 of 5,200) violate the carrier-tier policy, but
they account for **26.4% of all dollars paid out in claims**. Violating
shipments have a 4.36% loss/damage rate vs. 1.23% for compliant
shipments — **3.5x higher risk**, concentrated almost entirely in the
$10K–$150K value bands (13.5% and 15.5% violation rates respectively),
where the temptation to save on a cheaper standard carrier is highest.

**Portfolio-wide loss ratio sits at 64.2%** (claims paid / premium
written) — in a healthy range for a P&C-style line of business, which
was an intentional calibration target for this synthetic data rather
than an accident.

**Loss ratio by carrier tier tells a nuanced story.** High-Security
carriers run a 60.7% loss ratio and Standard carriers run 21.2% —
expected, since Standard is only used for genuinely low-value, low-risk
shipments under this policy. Enhanced tier shows an inflated 117.3%
loss ratio, but that's driven by a small sample (56 paid claims total
across the whole dataset) rather than a real structural problem —
flagging that distinction, instead of reporting the number at face
value, is itself the kind of judgment a domain analyst is expected to
bring.

**The actionable output is the flagged-shipment table**, not a chart.
The dashboard surfaces every policy-violating shipment (carrier used,
declared value, status, claim paid) sorted by value — this is the list
an underwriting or ops team would actually work from to follow up with
a broker or customer *before* a loss happens, not after.

## Dataset

Synthetic, but built with real underwriting logic (`generate_data.py`):

| Table | Rows | Description |
|---|---|---|
| `customers.csv` | 260 | Jeweler accounts — retailer/wholesaler/manufacturer/individual collector, risk rating |
| `carriers.csv` | 7 | Security tier (Standard/Enhanced/High-Security), SLA days, premium rate |
| `shipments.csv` | 5,200 | Declared value, carrier used, required tier, policy violation flag, transit status |
| `claims.csv` | 74 | Claim reason, amount, status (Paid/Denied/Pending) |

Customer `risk_rating` drives how often that account follows carrier
policy (Low-risk accounts comply ~94% of the time, High-risk accounts
only ~60%) — a deliberate simulation of the real-world pattern where a
handful of accounts generate a disproportionate share of underwriting
risk.

## Dashboard

Open `index.html` in any browser. KPI cards (premium written,
claims paid, loss ratio, violation rate), an underwriting-signal
callout that recalculates with your filters, four charts, and the
flagged-shipment table. Filterable by carrier tier, value tier,
customer type, and policy compliance.

## Skills demonstrated

Domain-driven metric design (loss ratio, violation-adjusted risk,
value-tier segmentation), building a dataset that encodes real business
rules rather than random noise, calling out a small-sample artifact
instead of overstating it, and turning analysis into an actionable list
rather than just a chart.
