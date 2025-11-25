# Olist Brazilian E-commerce Dataset Setup

This folder contains scripts to load the **Olist Brazilian E-commerce dataset** into DuckDB for analytics.

## Dataset Information

**Source**: [Kaggle - Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/data)

**Description**: Real commercial data from 100k orders (2016-2018) from the Brazilian e-commerce platform Olist.

**Tables**:
- `customers` - Customer information
- `orders` - Order details and status
- `order_items` - Items in each order
- `order_payments` - Payment information
- `order_reviews` - Customer reviews
- `products` - Product catalog
- `sellers` - Seller information
- `geolocation` - Brazilian zip code geolocation
- `product_category_name_translation` - Category translations

## Quick Start

### Option 1: Automatic Download (Requires Kaggle API)

```bash
# 1. Enter Docker container
docker exec -it analytics-lab bash

# 2. Set up Kaggle credentials (one-time setup)
mkdir -p ~/.kaggle
# Copy your kaggle.json to ~/.kaggle/kaggle.json
# Get it from: https://www.kaggle.com/settings/account

# 3. Run setup script
./scripts/data-generation/setup_olist.sh
```

### Option 2: Manual Download

```bash
# 1. Download dataset from Kaggle:
#    https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/data
#    Click "Download" button

# 2. Extract ZIP to: data/raw/olist/
#    Should contain CSV files like:
#    - olist_customers_dataset.csv
#    - olist_orders_dataset.csv
#    - etc.

# 3. Enter Docker container and run setup
docker exec -it analytics-lab bash
./scripts/data-generation/setup_olist.sh
```

## What Gets Created

### DuckDB Database
**Location**: `/workspace/data/olist_ecommerce.duckdb`

### Schemas
- `raw` - Raw data from CSV files
- `staging` - Transformed views and aggregations

### Tables (in `raw` schema)
- `raw.customers`
- `raw.orders`
- `raw.order_items`
- `raw.order_payments`
- `raw.order_reviews`
- `raw.products`
- `raw.sellers`
- `raw.geolocation`
- `raw.product_category_name_translation`

### Views (in `staging` schema)
- `staging.orders_summary` - Monthly order statistics
- `staging.revenue_summary` - Monthly revenue metrics

## Querying the Data

### Using DuckDB CLI

```bash
# Open database
duckdb /workspace/data/olist_ecommerce.duckdb

# Example queries
SELECT * FROM raw.orders LIMIT 5;
SELECT * FROM staging.orders_summary;
SHOW TABLES;
```

### Using Python

```python
import duckdb

conn = duckdb.connect('/workspace/data/olist_ecommerce.duckdb')

# Get orders
df = conn.execute("SELECT * FROM raw.orders LIMIT 10").df()
print(df)

# Monthly revenue
revenue = conn.execute("SELECT * FROM staging.revenue_summary").df()
print(revenue)
```

### Using Jupyter Lab

```python
# In a Jupyter notebook
import duckdb
import pandas as pd
import matplotlib.pyplot as plt

conn = duckdb.connect('/workspace/data/olist_ecommerce.duckdb')

# Analyze revenue trends
revenue = conn.execute("""
    SELECT 
        order_month,
        total_revenue,
        total_orders
    FROM staging.revenue_summary
    ORDER BY order_month
""").df()

revenue.plot(x='order_month', y='total_revenue', kind='line')
plt.show()
```

## Example Analytics Questions

Use this dataset to practice analytics engineering:

1. **Revenue Analysis**
   - What's the monthly revenue trend?
   - Which product categories generate most revenue?
   - What's the average order value?

2. **Customer Behavior**
   - How many repeat customers?
   - What's the customer lifetime value?
   - Which cities have most customers?

3. **Seller Performance**
   - Top performing sellers?
   - Average delivery time by seller?
   - Seller ratings distribution?

4. **Product Analysis**
   - Most popular product categories?
   - Products with best reviews?
   - Price distribution by category?

## Files

- `load_olist_to_duckdb.py` - Main Python script to load data
- `setup_olist.sh` - Bash wrapper for easy execution
- `README.md` - This file

## Troubleshooting

### Kaggle API Not Working
Download manually from Kaggle and extract to `data/raw/olist/`

### Permission Errors
Make sure scripts are executable:
```bash
chmod +x scripts/data-generation/*.sh
chmod +x scripts/data-generation/*.py
```

### Missing Dependencies
The Docker container should have all dependencies. If not:
```bash
pip install duckdb pandas kaggle
```

## Next Steps

After loading the data:
1. **Explore** with SQL queries
2. **Build dbt models** in `dbt/` folder
3. **Create dashboards** in Metabase
4. **Analyze** in Jupyter notebooks
