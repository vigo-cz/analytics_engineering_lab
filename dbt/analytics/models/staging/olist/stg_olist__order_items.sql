{{
    config(
        materialized='view'
    )
}}

-- Staging model for order items
-- Includes pricing and shipping information

SELECT
    order_id,
    order_item_id,
    product_id,
    seller_id,
    CAST(shipping_limit_date AS TIMESTAMP) AS shipping_limit_at,
    price,
    freight_value
FROM {{ source('olist_raw', 'order_items') }}
