# Claims Frequency Forecasting

**Focus of this project: a technical model.** Trend + seasonal
decomposition built from first principles with NumPy (no
`statsmodels`/`sklearn`), forecasting insurance claims volume and
reserve dollars 6 months forward, allocated across declared-value
tiers. Built on the same insured-jewelry-logistics dataset as
[project 1](../01-insured-logistics-dashboard/), joining claims back to
their originating shipment to recover a claim date.

## The question this answers

How many claims — and how many claim dollars — should underwriting
expect next month, so reserves get set *before* the fact instead of
reacted to after?

## Method

1. Build a monthly claims-count time series, Jan 2024–Jun 2026 (30 points).
2. Fit a linear trend via least squares (`numpy.polyfit`).
3. Compute a seasonal index per calendar month — the average ratio of
   actual to trend for that month across all years present.
4. Forecast forward = trend projection × seasonal index.
5. Build an 80% prediction interval from in-sample residual spread
   (normal approximation).
6. Convert the frequency forecast into a $ reserve forecast using
   historical average claim severity and the historical mix of claims
   across value tiers.

**Honest limitation:** 30 monthly observations is a thin base for
estimating 12 separate seasonal indices — some calendar months are
backed by only 2–3 data points. The forecast is directionally useful
(it correctly recovers the Valentine's Day and holiday-season spikes
baked into the underlying shipping volume) but the prediction intervals
are wide, and the write-up says so rather than overselling precision.

## Results (from the live run)

- **Trend**: +0.0125 claims/month (essentially flat over the historical window)
- **Seasonal index**: February peaks at 2.50x baseline (Valentine's Day), December at 1.25x (holidays); June–October run 0.42–0.65x baseline
- **Average paid claim severity**: $23,987.16
- **Paid claim rate**: 75.7% of filed claims end up paid
- **6-month forecast** (Jul–Dec 2026): ranges from 1.16 claims/month (summer) to 3.41 claims/month (December), with December carrying an estimated **$61,899.84** in reserve, allocated 45.9% / 35.1% / 17.6% / 1.4% across the four value tiers

## Files

```
03-claims-forecasting/
├── forecast.py              # the model: trend + seasonal decomposition
├── data/                     shipments.csv, claims.csv (shared with project 1)
└── output/
    ├── monthly_history.csv   actual / trend / seasonal index / fitted / residual
    ├── forecast.csv          6-month forward forecast + reserve $
    └── model_summary.json    full model parameters + forecast, powers index.html
```

## How to run

```bash
python3 forecast.py   # prints the model summary and writes output/*.csv, *.json
```

Open `index.html` for the visualized version (historical vs. fitted vs.
forecast chart, seasonal index chart, and the reserve-allocation table).

## Skills demonstrated

Implementing a time-series decomposition from first principles instead
of just calling a library, being explicit about a model's sample-size
limitations rather than overselling precision, and translating a
statistical forecast into an operational figure (tier-allocated reserve
$) a non-technical stakeholder can actually use.
