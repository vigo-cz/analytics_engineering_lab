# ClickHouse Quick Reference

## Start ClickHouse

```bash
docker compose up -d
```

## Sync Data

```bash
docker exec -it analytics-lab python /workspace/scripts/sync_duckdb_to_clickhouse.py
```

## Query ClickHouse

### Web UI
`http://localhost:8123/play`

### Command Line
```bash
docker exec -it analytics-clickhouse clickhouse-client
```

### Python
```python
import clickhouse_connect
client = clickhouse_connect.get_client(
    host='localhost', port=8123,
    username='analytics', password='analytics_password'
)
df = client.query('SELECT * FROM raw.orders LIMIT 5').result_as_dataframe()
```

## VS Code Connection

**SQLTools Settings**:
```json
{
  "name": "ClickHouse - Olist",
  "driver": "ClickHouse",
  "server": "YOUR_WINDOWS_IP",
  "port": 8123,
  "username": "analytics",
  "password": "analytics_password"
}
```

## Useful Queries

```sql
-- Show all tables
SHOW TABLES FROM raw;

-- Monthly revenue
SELECT * FROM marts.monthly_revenue ORDER BY order_month;

-- Top categories
SELECT * FROM marts.product_category_performance ORDER BY total_revenue DESC LIMIT 10;
```

## Ports

- **8123**: HTTP (queries, web UI)
- **9000**: Native TCP (CLI)

## Credentials

- **User**: `analytics`
- **Password**: `analytics_password`
- **Databases**: `raw`, `staging`, `marts`

---

See `infrastructure/clickhouse/CLICKHOUSE_SETUP.md` for full documentation.
