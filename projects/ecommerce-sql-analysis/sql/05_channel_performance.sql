-- Business question: Which acquisition channels bring in customers who
-- generate the most revenue and the highest average order value? Useful
-- for guiding marketing spend allocation.

SELECT
    o.channel,
    COUNT(DISTINCT o.customer_id)                AS customers,
    COUNT(DISTINCT o.order_id)                   AS orders,
    ROUND(SUM(o.order_total), 2)                 AS total_revenue,
    ROUND(AVG(o.order_total), 2)                 AS avg_order_value,
    ROUND(SUM(o.order_total) / COUNT(DISTINCT o.customer_id), 2) AS revenue_per_customer
FROM orders o
WHERE o.status = 'Completed'
GROUP BY o.channel
ORDER BY total_revenue DESC;
