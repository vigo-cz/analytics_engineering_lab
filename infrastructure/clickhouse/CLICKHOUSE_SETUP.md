# ClickHouse Setup Guide

Complete guide for setting up and using ClickHouse with the Olist dataset.

## Overview

ClickHouse is a high-performance OLAP database perfect for analytics queries. This setup runs alongside DuckDB:

- **DuckDB**: Fast local development, embedded in Python/Jupyter
- **ClickHouse**: Remote SQL access, production queries, Metabase integration

## Architecture

```
CSV Files → DuckDB (fast loading)
              ↓
         ClickHouse (remote queries)
              ↓
    Metabase / VS Code / Remote Tools
```

## Quick Start

### 1. Start ClickHouse

```bash
# Start all services including ClickHouse
docker compose up -d

# Check ClickHouse is running
docker ps | grep clickhouse

# View ClickHouse logs
docker logs analytics-clickhouse
```

### 2. Sync Data from DuckDB

```bash
# Enter analytics container
docker exec -it analytics-lab bash

# Run sync script
python /workspace/scripts/sync_duckdb_to_clickhouse.py
```

This will:
- Copy all raw tables from DuckDB
- Copy dbt staging models (if you've run `dbt run`)
- Copy dbt mart models
- Create appropriate schemas in ClickHouse

### 3. Query ClickHouse

**Option A: HTTP Interface (Browser)**

Open: `http://localhost:8123/play`

```sql
-- Show databases
SHOW DATABASES;

-- Show tables
SHOW TABLES FROM raw;

-- Query data
SELECT * FROM raw.orders LIMIT 5;
SELECT * FROM marts.monthly_revenue;
```

**Option B: Command Line**

```bash
# From host machine
docker exec -it analytics-clickhouse clickhouse-client

# Or with credentials
docker exec -it analytics-clickhouse clickhouse-client \
  --user analytics \
  --password analytics_password \
  --database raw
```

**Option C: Python**

```python
import clickhouse_connect

client = clickhouse_connect.get_client(
    host='localhost',
    port=8123,
    username='analytics',
    password='analytics_password'
)

# Query
result = client.query('SELECT * FROM raw.orders LIMIT 5')
df = result.result_as_dataframe()
print(df)
```

## Remote Access from VS Code

### Install SQLTools Extension

1. Install **SQLTools** extension
2. Install **SQLTools ClickHouse Driver**

### Configure Connection

Add to VS Code settings (`.vscode/settings.json`):

```json
{
  "sqltools.connections": [
    {
      "name": "ClickHouse - Olist",
      "driver": "ClickHouse",
      "server": "YOUR_WINDOWS_IP",
      "port": 8123,
      "username": "analytics",
      "password": "analytics_password",
      "database": "raw",
      "connectionTimeout": 30
    }
  ]
}
```

Replace `YOUR_WINDOWS_IP` with your Windows machine's IP address.

### Query from VS Code

1. Open SQLTools sidebar
2. Connect to "ClickHouse - Olist"
3. Browse schemas: `raw`, `staging`, `marts`
4. Write SQL queries in `.sql` files
5. Run with `Ctrl+E Ctrl+E` (or Cmd+E Cmd+E on Mac)

## Connecting Metabase

### Add ClickHouse Database

1. Go to Metabase: `http://localhost:3000`
2. **Settings** → **Admin** → **Databases** → **Add database**
3. Select **ClickHouse**
4. Configure:
   ```
   Display name: Olist ClickHouse
   Host: clickhouse
   Port: 8123
   Database name: raw
   Username: analytics
   Password: analytics_password
   ```
5. **Save**

### Query in Metabase

- Browse `raw`, `staging`, `marts` schemas
- Use visual query builder or SQL
- Create dashboards with ClickHouse data

## Syncing Data

### Initial Sync

```bash
docker exec -it analytics-lab python /workspace/scripts/sync_duckdb_to_clickhouse.py
```

### After Running dbt

```bash
# Run dbt models in DuckDB
docker exec -it analytics-lab dbt run --project-dir /workspace/dbt/analytics

# Sync to ClickHouse
docker exec -it analytics-lab python /workspace/scripts/sync_duckdb_to_clickhouse.py
```

### Automated Sync (Optional)

Add to `docker-compose.yml` or create a cron job:

```bash
# Sync every hour
0 * * * * docker exec analytics-lab python /workspace/scripts/sync_duckdb_to_clickhouse.py
```

## Example Queries

### Monthly Revenue

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

### Customer Analysis

```sql
SELECT 
    customer_state,
    COUNT(DISTINCT customer_unique_id) as customers,
    SUM(item_total) as total_revenue,
    AVG(item_total) as avg_revenue_per_order
FROM marts.fct_order_items
GROUP BY customer_state
ORDER BY total_revenue DESC;
```

### Time Series Analysis

```sql
SELECT 
    toStartOfWeek(order_purchased_at) as week,
    COUNT(DISTINCT order_id) as orders,
    SUM(item_total) as revenue
FROM marts.fct_order_items
WHERE order_purchased_at >= today() - INTERVAL 90 DAY
GROUP BY week
ORDER BY week;
```

## Performance Tips

### 1. Use Materialized Views

```sql
CREATE MATERIALIZED VIEW raw.orders_daily_mv
ENGINE = SummingMergeTree()
ORDER BY order_date
AS SELECT
    toDate(order_purchased_at) as order_date,
    COUNT(*) as order_count,
    SUM(price) as total_revenue
FROM raw.orders
GROUP BY order_date;
```

### 2. Optimize Table Engines

For large datasets, use `MergeTree` with appropriate `ORDER BY`:

```sql
CREATE TABLE raw.orders_optimized
ENGINE = MergeTree()
ORDER BY (customer_id, order_purchased_at)
AS SELECT * FROM raw.orders;
```

### 3. Use Projections

```sql
ALTER TABLE raw.orders
ADD PROJECTION orders_by_status (
    SELECT *
    ORDER BY order_status
);
```

## Troubleshooting

### ClickHouse Not Starting

```bash
# Check logs
docker logs analytics-clickhouse

# Restart
docker restart analytics-clickhouse
```

### Connection Refused

```bash
# Check if port is exposed
docker port analytics-clickhouse

# Should show:
# 8123/tcp -> 0.0.0.0:8123
# 9000/tcp -> 0.0.0.0:9000
```

### Sync Script Errors

```bash
# Check DuckDB file exists
docker exec analytics-lab ls -la /workspace/data/olist_ecommerce.duckdb

# Check ClickHouse is reachable
docker exec analytics-lab ping -c 3 clickhouse
```

### Out of Memory

Increase Docker memory limit in Docker Desktop settings (recommended: 4GB+).

## Ports Reference

- **8123**: HTTP interface (queries, web UI)
- **9000**: Native TCP protocol (CLI, drivers)
- **8443**: HTTPS (if configured)
- **9440**: Native TCP with TLS (if configured)

## Credentials

- **Username**: `analytics`
- **Password**: `analytics_password`
- **Databases**: `raw`, `staging`, `marts`, `olist`

## Next Steps

1. ✅ Start ClickHouse: `docker compose up -d`
2. ✅ Sync data: `python scripts/sync_duckdb_to_clickhouse.py`
3. 📊 Connect VS Code SQLTools
4. 📈 Connect Metabase
5. 🚀 Run analytics queries!

## Resources

- [ClickHouse Documentation](https://clickhouse.com/docs)
- [ClickHouse SQL Reference](https://clickhouse.com/docs/en/sql-reference/)
- [ClickHouse Functions](https://clickhouse.com/docs/en/sql-reference/functions/)
