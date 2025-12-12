{{
    config(
        materialized='table'
    )
}}

-- Product category performance metrics

SELECT
    product_category,
    
    -- Order metrics
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(*) AS total_items_sold,
    
    -- Revenue metrics
    SUM(item_total) AS total_revenue,
    AVG(item_price) AS avg_item_price,
    
    -- Delivery metrics
    AVG(days_to_delivery) AS avg_days_to_delivery

FROM {{ ref('fct_order_items') }}
WHERE order_status = 'delivered'
  AND product_category IS NOT NULL
GROUP BY 1
ORDER BY total_revenue DESC
