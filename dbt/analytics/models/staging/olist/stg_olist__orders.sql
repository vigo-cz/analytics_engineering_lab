{{
    config(
        materialized='view'
    )
}}

-- Staging model for orders
-- Cleans and standardizes the raw orders data

SELECT
    order_id,
    customer_id,
    order_status,
    CAST(order_purchase_timestamp AS TIMESTAMP) AS order_purchased_at,
    CAST(order_approved_at AS TIMESTAMP) AS order_approved_at,
    CAST(order_delivered_carrier_date AS TIMESTAMP) AS order_delivered_to_carrier_at,
    CAST(order_delivered_customer_date AS TIMESTAMP) AS order_delivered_to_customer_at,
    CAST(order_estimated_delivery_date AS TIMESTAMP) AS order_estimated_delivery_at
FROM {{ source('olist_raw', 'orders') }}
WHERE order_purchase_timestamp IS NOT NULL
