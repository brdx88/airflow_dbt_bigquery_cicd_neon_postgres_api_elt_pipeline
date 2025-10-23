

SELECT
    CAST('2025-10-23' AS DATE) AS position_date,
    DATE_TRUNC(order_date, MONTH) AS order_month,
    category,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(quantity) AS total_items_sold,
    SUM(total_amount) AS total_revenue,
    ROUND(AVG(total_amount), 2) AS avg_order_value
FROM `serious-music-469407-f1`.`banking_silver`.`int_ecom_orders_enriched`
WHERE position_date = '2025-10-23'
GROUP BY 1, 2, 3