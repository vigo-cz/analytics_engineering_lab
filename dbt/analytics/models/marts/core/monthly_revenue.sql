{{
    config(
        materialized='table'
    )
}}

-- Monthly revenue and order metrics
-- Aggregated for dashboards and reporting

SELECT
    order_month,
    
    -- Order metrics
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_unique_id) AS unique_customers,
    COUNT(*) AS total_items,
    
    -- Revenue metrics
    SUM(item_price) AS total_revenue,
    SUM(item_freight) AS total_freight,
    SUM(item_total) AS total_revenue_with_freight,
    
    -- Average metrics
    AVG(item_price) AS avg_item_price,
    SUM(item_total) / COUNT(DISTINCT order_id) AS avg_order_value,
    
    -- Delivery metrics
    AVG(days_to_delivery) AS avg_days_to_delivery,
    AVG(delivery_vs_estimate_days) AS avg_delivery_vs_estimate

FROM {{ ref('fct_order_items') }}
WHERE order_status = 'delivered'
GROUP BY 1
ORDER BY 1
