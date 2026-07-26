-- Business question: Which products drive the most revenue, and do our
-- top sellers by revenue also have healthy margins? (Flags cases where a
-- best-seller is actually a low-margin product.)

SELECT
    p.product_name,
    p.category,
    SUM(oi.quantity)                                            AS units_sold,
    ROUND(SUM(oi.line_total), 2)                                AS total_revenue,
    ROUND(SUM(oi.quantity * p.unit_cost), 2)                    AS total_cost,
    ROUND(SUM(oi.line_total) - SUM(oi.quantity * p.unit_cost), 2) AS gross_profit,
    ROUND(
        100.0 * (SUM(oi.line_total) - SUM(oi.quantity * p.unit_cost)) / SUM(oi.line_total), 1
    )                                                            AS margin_pct
FROM order_items oi
JOIN products p ON p.product_id = oi.product_id
JOIN orders o ON o.order_id = oi.order_id
WHERE o.status = 'Completed'
GROUP BY p.product_id
ORDER BY total_revenue DESC
LIMIT 10;
