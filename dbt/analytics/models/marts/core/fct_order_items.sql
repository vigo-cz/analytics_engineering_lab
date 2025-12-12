{{
    config(
        materialized='table'
    )
}}

-- Fact table for order items with all relevant dimensions
-- Denormalized for easy querying in BI tools

WITH orders AS (
    SELECT * FROM {{ ref('stg_olist__orders') }}
),

order_items AS (
    SELECT * FROM {{ ref('stg_olist__order_items') }}
),

customers AS (
    SELECT * FROM {{ ref('stg_olist__customers') }}
),

products AS (
    SELECT * FROM {{ ref('stg_olist__products') }}
)

SELECT
    -- Order item grain
    oi.order_id,
    oi.order_item_id,
    
    -- Timestamps
    o.order_purchased_at,
    o.order_approved_at,
    o.order_delivered_to_customer_at,
    DATE_TRUNC('month', o.order_purchased_at) AS order_month,
    DATE_TRUNC('week', o.order_purchased_at) AS order_week,
    DATE_TRUNC('day', o.order_purchased_at) AS order_date,
    
    -- Order attributes
    o.order_status,
    
    -- Customer attributes
    c.customer_unique_id,
    c.customer_city,
    c.customer_state,
    
    -- Product attributes
    p.product_id,
    p.product_category_name_english AS product_category,
    
    -- Metrics
    oi.price AS item_price,
    oi.freight_value AS item_freight,
    oi.price + oi.freight_value AS item_total,
    
    -- Delivery metrics
    CASE 
        WHEN o.order_delivered_to_customer_at IS NOT NULL 
        THEN DATE_DIFF('day', o.order_purchased_at, o.order_delivered_to_customer_at)
    END AS days_to_delivery,
    
    CASE
        WHEN o.order_delivered_to_customer_at IS NOT NULL 
             AND o.order_estimated_delivery_at IS NOT NULL
        THEN DATE_DIFF('day', o.order_delivered_to_customer_at, o.order_estimated_delivery_at)
    END AS delivery_vs_estimate_days

FROM order_items oi
INNER JOIN orders o ON oi.order_id = o.order_id
INNER JOIN customers c ON o.customer_id = c.customer_id
LEFT JOIN products p ON oi.product_id = p.product_id
