# Olist Dataset CSV Files

Place the Olist Brazilian E-commerce dataset CSV files in this directory.

## Download Instructions

1. Go to: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/data
2. Click "Download" (requires free Kaggle account)
3. Extract the ZIP file
4. Copy all CSV files to this directory

## Expected Files

- olist_customers_dataset.csv
- olist_geolocation_dataset.csv
- olist_order_items_dataset.csv
- olist_order_payments_dataset.csv
- olist_order_reviews_dataset.csv
- olist_orders_dataset.csv
- olist_products_dataset.csv
- olist_sellers_dataset.csv
- product_category_name_translation.csv

## After Downloading

Run the setup script:
```bash
docker exec -it analytics-lab ./scripts/data-generation/setup_olist.sh
```

This will load all CSV files into DuckDB at `/workspace/data/olist_ecommerce.duckdb`
