-- Business question: How much revenue comes from each customer segment
-- (New / Returning / VIP), and how does average spend per customer differ?
-- A lightweight RFM-style view: recency (days since last order), frequency
-- (order count), monetary (lifetime revenue).

SELECT
    c.segment,
    COUNT(DISTINCT c.customer_id)                         AS customers,
    COUNT(DISTINCT o.order_id)                             AS total_orders,
    ROUND(SUM(o.order_total), 2)                           AS total_revenue,
    ROUND(SUM(o.order_total) / COUNT(DISTINCT c.customer_id), 2) AS revenue_per_customer,
    ROUND(1.0 * COUNT(DISTINCT o.order_id) / COUNT(DISTINCT c.customer_id), 2) AS avg_orders_per_customer,
    ROUND(
        100.0 * SUM(o.order_total) / (SELECT SUM(order_total) FROM orders WHERE status = 'Completed'), 1
    )                                                       AS pct_of_total_revenue
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id AND o.status = 'Completed'
GROUP BY c.segment
ORDER BY total_revenue DESC;
