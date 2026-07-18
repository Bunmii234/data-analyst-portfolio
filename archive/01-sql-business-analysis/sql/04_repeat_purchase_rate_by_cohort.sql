-- Business question: What share of customers who signed up in a given
-- month go on to place a second order? A simple cohort-based repeat
-- purchase rate -- a proxy for retention/loyalty.

WITH cohort AS (
    SELECT
        customer_id,
        strftime('%Y-%m', signup_date) AS signup_month
    FROM customers
),
order_counts AS (
    SELECT
        customer_id,
        COUNT(*) AS completed_orders
    FROM orders
    WHERE status = 'Completed'
    GROUP BY customer_id
)
SELECT
    cohort.signup_month,
    COUNT(DISTINCT cohort.customer_id)                                   AS cohort_size,
    COUNT(DISTINCT CASE WHEN oc.completed_orders >= 2 THEN cohort.customer_id END) AS repeat_customers,
    ROUND(
        100.0 * COUNT(DISTINCT CASE WHEN oc.completed_orders >= 2 THEN cohort.customer_id END)
        / COUNT(DISTINCT cohort.customer_id), 1
    )                                                                     AS repeat_purchase_rate_pct
FROM cohort
LEFT JOIN order_counts oc ON oc.customer_id = cohort.customer_id
GROUP BY cohort.signup_month
ORDER BY cohort.signup_month;
