# Quick Start Guide - Olist Dataset

## 🚀 Get Started in 3 Steps

### Step 1: Start Docker Containers
```bash
docker compose up -d
```

### Step 2: Download Olist Dataset

**Option A: Manual Download (Easiest)**
1. Go to https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/data
2. Click "Download" (requires Kaggle account)
3. Extract the ZIP file
4. Copy all CSV files to: `data/raw/olist/`

**Option B: Automatic Download (Requires Kaggle API)**
```bash
# Get Kaggle API credentials
# 1. Go to https://www.kaggle.com/settings/account
# 2. Click "Create New API Token"
# 3. Save kaggle.json

# Copy credentials into container
docker cp ~/Downloads/kaggle.json analytics-lab:/root/.kaggle/kaggle.json
```

### Step 3: Load Data into DuckDB
```bash
# Enter container
docker exec -it analytics-lab bash

# Run setup script
./scripts/data-generation/setup_olist.sh
```

## ✅ You're Done!

The database is now ready at: `/workspace/data/olist_ecommerce.duckdb`

## 🔍 Query the Data

### Option 1: DuckDB CLI
```bash
docker exec -it analytics-lab duckdb /workspace/data/olist_ecommerce.duckdb
```

```sql
-- Show all tables
SHOW TABLES;

-- View orders
SELECT * FROM raw.orders LIMIT 5;

-- Monthly revenue
SELECT * FROM staging.revenue_summary;
```

### Option 2: Python
```bash
docker exec -it analytics-lab python
```

```python
import duckdb
conn = duckdb.connect('/workspace/data/olist_ecommerce.duckdb')
df = conn.execute("SELECT * FROM raw.orders LIMIT 10").df()
print(df)
```

### Option 3: Jupyter Lab
1. Get Jupyter URL: `docker exec analytics-lab jupyter lab list`
2. Open in browser: `http://localhost:8888`
3. Create new notebook and query!

## 📊 What's in the Database?

**Schemas**:
- `raw.*` - Raw CSV data (9 tables)
- `staging.*` - Aggregated views

**Key Tables**:
- `raw.orders` - 99,441 orders
- `raw.order_items` - 112,650 items
- `raw.customers` - 99,441 customers
- `raw.products` - 32,951 products
- `raw.sellers` - 3,095 sellers

**Date Range**: September 2016 - October 2018

## 🎯 Next Steps

1. **Explore** the data with SQL
2. **Build dbt models** for transformations
3. **Create dashboards** in Metabase (http://localhost:3000)
4. **Analyze** in Jupyter notebooks

## 📚 Full Documentation

See `scripts/data-generation/README.md` for detailed information.
