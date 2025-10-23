WITH ORDERS AS (
  SELECT * FROM `serious-music-469407-f1`.`banking_silver`.`stg_ecom_orders`
)

, CUSTOMERS AS (
  SELECT * FROM `serious-music-469407-f1`.`banking_silver`.`stg_ecom_customers`
)

, PRODUCTS AS (
  SELECT * FROM `serious-music-469407-f1`.`banking_silver`.`stg_ecom_products`
)

SELECT
    CAST('2025-10-23' AS DATE) AS position_date,
    CUSTOMERS.customer_id,
    CUSTOMERS.first_name || ' ' || CUSTOMERS.last_name AS customer_name,
    CUSTOMERS.email,
    CUSTOMERS.signup_date,
    ORDERS.id as order_id,
    ORDERS.order_date,
    ORDERS.quantity,
    ORDERS.total_amount,
    
    CASE
        WHEN ORDERS.total_amount > 1000 THEN 'HIGH VALUE'
        WHEN ORDERS.total_amount BETWEEN 500 AND 1000 THEN 'MEDUM VALUE'
        ELSE 'LOW VALUE'
    END AS order_value_segment,

    PRODUCTS.product_name,
    PRODUCTS.category,
    PRODUCTS.price

FROM CUSTOMERS
LEFT JOIN ORDERS
    ON CUSTOMERS.customer_id = ORDERS.customer_id
LEFT JOIN PRODUCTS
    ON ORDERS.product_id = PRODUCTS.product_id