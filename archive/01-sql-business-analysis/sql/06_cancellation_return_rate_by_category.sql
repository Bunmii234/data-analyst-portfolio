-- Business question: Which product categories have the highest cancellation
-- and return rates? High rates in a category can point to quality issues,
-- pricing mismatch, or poor product-page expectations.

WITH order_category AS (
    SELECT DISTINCT o.order_id, o.status, p.category
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    JOIN products p ON p.product_id = oi.product_id
)
SELECT
    category,
    COUNT(*)                                                        AS total_orders,
    SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END)           AS cancelled,
    SUM(CASE WHEN status = 'Returned' THEN 1 ELSE 0 END)            AS returned,
    ROUND(100.0 * SUM(CASE WHEN status IN ('Cancelled','Returned') THEN 1 ELSE 0 END) / COUNT(*), 1) AS problem_rate_pct
FROM order_category
GROUP BY category
ORDER BY problem_rate_pct DESC;
