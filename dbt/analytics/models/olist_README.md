# Olist dbt Models

This folder contains dbt models for the Olist Brazilian E-commerce dataset.

## Structure

```
models/
├── staging/
│   └── olist/
│       ├── stg_olist__orders.sql
│       ├── stg_olist__order_items.sql
│       ├── stg_olist__customers.sql
│       ├── stg_olist__products.sql
│       └── schema.yml
└── marts/
    └── core/
        ├── fct_order_items.sql
        ├── monthly_revenue.sql
        ├── product_category_performance.sql
        └── schema.yml
```

## Models

### Staging Layer (`staging/olist/`)

Cleans and standardizes raw data:

- **`stg_olist__orders`**: Order data with cleaned timestamps
- **`stg_olist__order_items`**: Order items with pricing
- **`stg_olist__customers`**: Customer information
- **`stg_olist__products`**: Products with English category names

### Marts Layer (`marts/core/`)

Business logic and aggregations:

- **`fct_order_items`**: Denormalized fact table for BI tools
- **`monthly_revenue`**: Monthly revenue and order metrics
- **`product_category_performance`**: Category-level performance

## Running dbt

### Inside Docker Container

```bash
# Enter container
docker exec -it analytics-lab bash

# Navigate to dbt project
cd /workspace/dbt/analytics

# Install dependencies (if any)
dbt deps

# Run all models
dbt run

# Run specific model
dbt run --select stg_olist__orders

# Run staging only
dbt run --select staging.olist.*

# Run marts only
dbt run --select marts.core.*

# Test models
dbt test

# Generate documentation
dbt docs generate
dbt docs serve --port 8080
```

### From Host Machine

```bash
# Run dbt inside container
docker exec -it analytics-lab dbt run --project-dir /workspace/dbt/analytics
```

## Querying dbt Models

### In DuckDB CLI

```bash
docker exec -it analytics-lab duckdb /workspace/data/olist_ecommerce.duckdb
```

```sql
-- Query staging models
SELECT * FROM staging.stg_olist__orders LIMIT 5;

-- Query mart models
SELECT * FROM marts.fct_order_items LIMIT 5;
SELECT * FROM marts.monthly_revenue;
SELECT * FROM marts.product_category_performance;
```

### In Metabase

1. Connect Metabase to DuckDB (see `bi/METABASE_DUCKDB_SETUP.md`)
2. Browse to `staging` or `marts` schema
3. Query the dbt models directly

### In Jupyter

```python
import duckdb

conn = duckdb.connect('/workspace/data/olist_ecommerce.duckdb')

# Query dbt models
df = conn.execute("SELECT * FROM marts.monthly_revenue").df()
display(df)
```

## Development Workflow

1. **Explore in Metabase**: Write ad-hoc SQL queries
2. **Prototype in dbt**: Create new models in `staging/` or `marts/`
3. **Test**: Add tests in `schema.yml`
4. **Run**: `dbt run --select your_model`
5. **Commit**: Version control your SQL
6. **Query in Metabase**: Use the dbt models for dashboards

## Example Queries

### Monthly Revenue Trend

```sql
SELECT 
    order_month,
    total_revenue,
    total_orders,
    avg_order_value
FROM marts.monthly_revenue
ORDER BY order_month;
```

### Top Product Categories

```sql
SELECT 
    product_category,
    total_revenue,
    total_items_sold
FROM marts.product_category_performance
ORDER BY total_revenue DESC
LIMIT 10;
```

### Customer Lifetime Value

```sql
SELECT 
    customer_unique_id,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(item_total) AS lifetime_value
FROM marts.fct_order_items
GROUP BY 1
HAVING COUNT(DISTINCT order_id) > 1
ORDER BY lifetime_value DESC
LIMIT 10;
```

## Next Steps

1. ✅ Run `dbt run` to build models
2. 📊 Connect Metabase to query dbt models
3. 🔄 Add more models as needed
4. ✅ Add dbt tests for data quality
5. 📈 Build dashboards in Metabase

## Troubleshooting

### Models Not Found

```bash
# Check if models ran successfully
dbt run

# Check DuckDB schemas
docker exec -it analytics-lab duckdb /workspace/data/olist_ecommerce.duckdb -c "SHOW SCHEMAS;"
```

### Compilation Errors

```bash
# Compile without running
dbt compile

# Debug specific model
dbt run --select your_model --debug
```

### Connection Issues

Check `profiles.yml` configuration (should point to DuckDB file).
