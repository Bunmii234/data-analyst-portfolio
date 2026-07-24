"""
CLAIMS FREQUENCY FORECASTING
=============================
Focus of this project: a technical model, applied to a domain problem an
underwriting/reserving team actually cares about -- how many claims (and
how many claim dollars) should we expect next month, so reserves can be
set appropriately before the fact rather than reacted to after.

Built on the same insured-jewelry-logistics dataset as project 1
(insured-jewelry-logistics), joining claims to their originating
shipment to recover a claim date, since the source data models when a
loss occurred at the shipment level.

Method: classical trend + seasonal decomposition, implemented directly
with numpy rather than an off-the-shelf time-series library (statsmodels
isn't available in this environment) -- which also makes every step of
the model auditable rather than a black box call.

  1. Build a monthly claims-count time series.
  2. Fit a linear trend via least squares.
  3. Compute a seasonal index per calendar month (ratio of actual to
     trend, averaged across the years present).
  4. Forecast forward = trend projection x seasonal index.
  5. Build a simple prediction interval from in-sample residual spread.
  6. Convert the frequency forecast into a $ reserve forecast using
     historical average claim severity and the historical mix of claims
     across declared-value tiers.

This is explicitly NOT presented as a production-grade forecast --
2.5 years of monthly data (30 points) is a thin base for seasonal
estimation, and the write-up says so. The point is demonstrating the
technique and being honest about its limits, which matters more here
than raw accuracy on a synthetic dataset.
"""
import csv
import json
import os
from datetime import date
from collections import defaultdict, Counter

import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUT_DIR, exist_ok=True)


def value_tier(v):
    v = float(v)
    if v < 10000: return "Under $10K"
    if v < 50000: return "$10K-$50K"
    if v < 150000: return "$50K-$150K"
    return "$150K+"


def load_data():
    shipments = {}
    with open(os.path.join(DATA_DIR, "shipments.csv")) as f:
        for r in csv.DictReader(f):
            shipments[r["shipment_id"]] = r

    claims = []
    with open(os.path.join(DATA_DIR, "claims.csv")) as f:
        for r in csv.DictReader(f):
            ship = shipments.get(r["shipment_id"])
            if not ship:
                continue
            claims.append({
                "claim_id": r["claim_id"],
                "claim_date": ship["ship_date"],  # loss modeled as occurring at/near ship date
                "claim_amount": float(r["claim_amount"]),
                "claim_status": r["claim_status"],
                "value_tier": value_tier(ship["declared_value"]),
            })
    return shipments, claims


def month_range(start, end):
    months = []
    y, m = start.year, start.month
    while (y, m) <= (end.year, end.month):
        months.append(f"{y:04d}-{m:02d}")
        m += 1
        if m > 12:
            m = 1
            y += 1
    return months


def main():
    shipments, claims = load_data()

    all_months_data = month_range(date(2024, 1, 1), date(2026, 6, 1))
    counts_by_month = Counter(c["claim_date"][:7] for c in claims)
    series = np.array([counts_by_month.get(m, 0) for m in all_months_data], dtype=float)
    n = len(series)
    x = np.arange(n)

    # ---- Step 1: linear trend via least squares ----
    slope, intercept = np.polyfit(x, series, 1)
    trend = slope * x + intercept

    # ---- Step 2: seasonal index per calendar month ----
    # ratio of actual to trend, averaged across all occurrences of each
    # calendar month in the historical window (guards against div by 0)
    cal_months = [int(m.split("-")[1]) for m in all_months_data]
    ratios_by_cal_month = defaultdict(list)
    for i in range(n):
        if trend[i] > 0.5:  # avoid division blowing up near-zero trend values early on
            ratios_by_cal_month[cal_months[i]].append(series[i] / trend[i])
    seasonal_index = {}
    for cm in range(1, 13):
        vals = ratios_by_cal_month.get(cm, [])
        seasonal_index[cm] = float(np.mean(vals)) if vals else 1.0
    # normalize so the average seasonal index is 1.0
    avg_idx = np.mean(list(seasonal_index.values()))
    seasonal_index = {k: v / avg_idx for k, v in seasonal_index.items()}

    # ---- Step 3: in-sample fitted values + residual spread ----
    fitted = np.array([trend[i] * seasonal_index[cal_months[i]] for i in range(n)])
    residuals = series - fitted
    resid_std = float(np.std(residuals))

    # ---- Step 4: forecast next 6 months ----
    forecast_months = month_range(date(2026, 7, 1), date(2026, 12, 1))
    forecast = []
    for j, m in enumerate(forecast_months):
        i = n + j
        cm = int(m.split("-")[1])
        trend_val = slope * i + intercept
        point = max(trend_val * seasonal_index[cm], 0)
        lower = max(point - 1.28 * resid_std, 0)   # ~80% interval, normal approx
        upper = point + 1.28 * resid_std
        forecast.append({"month": m, "forecast_claims": round(point, 2),
                          "lower_80": round(lower, 2), "upper_80": round(upper, 2)})

    # ---- Step 5: convert frequency forecast to a $ reserve forecast ----
    paid_claims = [c for c in claims if c["claim_status"] == "Paid"]
    avg_severity = float(np.mean([c["claim_amount"] for c in paid_claims])) if paid_claims else 0.0
    paid_rate = len(paid_claims) / len(claims) if claims else 0.0  # share of claims that end up Paid

    tier_counts = Counter(c["value_tier"] for c in claims)
    total_claims_n = sum(tier_counts.values())
    tier_mix = {t: tier_counts.get(t, 0) / total_claims_n for t in
                ["Under $10K", "$10K-$50K", "$50K-$150K", "$150K+"]}

    for row in forecast:
        expected_paid_claims = row["forecast_claims"] * paid_rate
        row["forecast_reserve_usd"] = round(expected_paid_claims * avg_severity, 2)
        row["tier_mix_allocation"] = {
            t: round(row["forecast_reserve_usd"] * share, 2) for t, share in tier_mix.items()
        }

    # ---- Write outputs ----
    with open(os.path.join(OUT_DIR, "monthly_history.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["month", "actual_claims", "trend", "seasonal_index", "fitted", "residual"])
        for i in range(n):
            w.writerow([all_months_data[i], series[i], round(trend[i], 2),
                        round(seasonal_index[cal_months[i]], 3), round(fitted[i], 2), round(residuals[i], 2)])

    with open(os.path.join(OUT_DIR, "forecast.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["month", "forecast_claims", "lower_80", "upper_80", "forecast_reserve_usd"])
        for row in forecast:
            w.writerow([row["month"], row["forecast_claims"], row["lower_80"], row["upper_80"], row["forecast_reserve_usd"]])

    with open(os.path.join(OUT_DIR, "model_summary.json"), "w") as f:
        json.dump({
            "slope_claims_per_month": round(float(slope), 4),
            "intercept": round(float(intercept), 3),
            "seasonal_index_by_month": {k: round(v, 3) for k, v in seasonal_index.items()},
            "residual_std": round(resid_std, 3),
            "avg_claim_severity_usd": round(avg_severity, 2),
            "paid_claim_rate": round(paid_rate, 3),
            "tier_mix": {k: round(v, 3) for k, v in tier_mix.items()},
            "forecast": forecast,
            "history": [{"month": all_months_data[i], "actual": series[i], "fitted": round(fitted[i], 2)} for i in range(n)],
        }, f, indent=2)

    print(f"Trend: {slope:+.3f} claims/month, intercept {intercept:.2f}")
    print(f"Residual std dev: {resid_std:.2f} claims")
    print(f"Avg paid claim severity: ${avg_severity:,.2f}  |  Paid rate: {paid_rate:.1%}")
    print("\nSeasonal index by calendar month:")
    for cm in range(1, 13):
        print(f"  {cm:02d}: {seasonal_index[cm]:.2f}")
    print("\n6-month forecast:")
    for row in forecast:
        print(f"  {row['month']}: {row['forecast_claims']:.2f} claims "
              f"(80% CI {row['lower_80']:.2f}-{row['upper_80']:.2f})  "
              f"-> reserve ${row['forecast_reserve_usd']:,.2f}")


if __name__ == "__main__":
    main()
