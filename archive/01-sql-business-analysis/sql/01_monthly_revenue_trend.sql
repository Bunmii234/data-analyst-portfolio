-- Business question: How is revenue trending month over month, and where
-- are the seasonal peaks/dips? (Completed orders only -- cancelled/returned
-- orders don't represent realized revenue.)

SELECT
    strftime('%Y-%m', order_date)              AS order_month,
    COUNT(DISTINCT order_id)                    AS order_count,
    ROUND(SUM(order_total), 2)                  AS total_revenue,
    ROUND(AVG(order_total), 2)                  AS avg_order_value,
    ROUND(
        100.0 * (SUM(order_total) - LAG(SUM(order_total)) OVER (ORDER BY strftime('%Y-%m', order_date)))
        / LAG(SUM(order_total)) OVER (ORDER BY strftime('%Y-%m', order_date)), 1
    )                                            AS mom_growth_pct
FROM orders
WHERE status = 'Completed'
GROUP BY order_month
ORDER BY order_month;
