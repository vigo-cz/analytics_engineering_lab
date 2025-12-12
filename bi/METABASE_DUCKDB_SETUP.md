# Connecting Metabase to DuckDB

This guide shows you how to connect Metabase to your DuckDB Olist e-commerce database.

## Prerequisites

- ✅ Metabase running at `http://localhost:3000`
- ✅ DuckDB database at `/workspace/data/olist_ecommerce.duckdb`
- ✅ Docker containers running (`docker compose up -d`)

## Step 1: Access Metabase

1. Open your browser: `http://localhost:3000`
2. If first time, complete the setup wizard:
   - Create admin account
   - Skip "Add your data" for now

## Step 2: Add DuckDB Database

### Option A: Using DuckDB JDBC (Recommended)

1. Click **Settings** (gear icon) → **Admin settings**
2. Go to **Databases** → **Add database**
3. Select **Other** (or search for DuckDB if available)
4. Configure:
   ```
   Display name: Olist E-commerce
   Database type: DuckDB (or Other)
   Host: analytics-lab
   Port: (leave empty)
   Database name: /workspace/data/olist_ecommerce.duckdb
   ```

### Option B: Using SQLite Driver (Workaround)

Since Metabase doesn't have native DuckDB support, you can:

1. Export DuckDB tables to SQLite
2. Connect Metabase to SQLite

**Export Script** (run in container):
```bash
docker exec -it analytics-lab python << 'EOF'
import duckdb
import sqlite3

# Connect to both databases
duck_conn = duckdb.connect('/workspace/data/olist_ecommerce.duckdb')
sqlite_conn = sqlite3.connect('/workspace/data/olist_metabase.db')

# Get all tables
tables = duck_conn.execute("""
    SELECT table_schema, table_name 
    FROM information_schema.tables 
    WHERE table_schema IN ('raw', 'staging')
""").fetchall()

# Export each table
for schema, table in tables:
    df = duck_conn.execute(f"SELECT * FROM {schema}.{table}").df()
    df.to_sql(f"{schema}_{table}", sqlite_conn, if_exists='replace', index=False)
    print(f"✅ Exported {schema}.{table}")

sqlite_conn.close()
duck_conn.close()
print("\n✅ Export complete!")
EOF
```

Then in Metabase:
1. **Add database** → **SQLite**
2. **Database file**: `/workspace/data/olist_metabase.db`
3. **Save**

### Option C: Use PostgreSQL Instead (Most Compatible)

Load data into PostgreSQL for full Metabase compatibility:

```bash
docker exec -it analytics-lab python << 'EOF'
import duckdb
import psycopg2
from psycopg2 import sql

# Connect to DuckDB
duck_conn = duckdb.connect('/workspace/data/olist_ecommerce.duckdb')

# Connect to PostgreSQL
pg_conn = psycopg2.connect(
    host='postgres',
    database='analytics_db',
    user='analytics',
    password='analytics_password'
)
pg_cursor = pg_conn.cursor()

# Create schemas
pg_cursor.execute("CREATE SCHEMA IF NOT EXISTS raw")
pg_cursor.execute("CREATE SCHEMA IF NOT EXISTS staging")
pg_conn.commit()

# Get all tables
tables = duck_conn.execute("""
    SELECT table_schema, table_name 
    FROM information_schema.tables 
    WHERE table_schema IN ('raw', 'staging')
""").fetchall()

# Copy each table
for schema, table in tables:
    df = duck_conn.execute(f"SELECT * FROM {schema}.{table}").df()
    
    # Drop if exists
    pg_cursor.execute(f"DROP TABLE IF EXISTS {schema}.{table}")
    
    # Create table from DataFrame
    from sqlalchemy import create_engine
    engine = create_engine('postgresql://analytics:analytics_password@postgres:5432/analytics_db')
    df.to_sql(table, engine, schema=schema, if_exists='replace', index=False)
    
    print(f"✅ Copied {schema}.{table} ({len(df)} rows)")

pg_conn.close()
duck_conn.close()
print("\n✅ Copy complete!")
EOF
```

Then in Metabase:
1. **Add database** → **PostgreSQL**
2. Configure:
   ```
   Display name: Olist Analytics
   Host: postgres
   Port: 5432
   Database name: analytics_db
   Username: analytics
   Password: analytics_password
   ```
3. **Save**

## Step 3: Explore Your Data

1. Click **Browse data** → Select your database
2. You should see:
   - `raw` schema with 9 tables
   - `staging` schema with summary views

## Step 4: Create Your First Question

1. Click **New** → **Question**
2. Select **Olist E-commerce** (or your database name)
3. Choose a table (e.g., `raw.orders`)
4. Build your query or switch to **Native query** for SQL

## Recommended Workflow

### For Ad-hoc Analysis:
- Use Metabase's visual query builder
- Or write SQL in "Native query" mode

### For Production Queries:
1. Prototype in Metabase
2. Move to dbt models (`dbt/models/`)
3. Run `dbt run` to materialize
4. Query dbt models in Metabase

## Troubleshooting

### Can't Connect to Database
- Ensure containers are running: `docker ps`
- Check database file exists: `docker exec analytics-lab ls -la /workspace/data/`

### Tables Not Showing
- Verify schemas exist: Run SQL in Metabase: `SHOW SCHEMAS;`
- Check table count: `SELECT COUNT(*) FROM information_schema.tables;`

### Slow Queries
- DuckDB is fast, but large joins can be slow
- Consider creating dbt models for complex queries
- Use staging tables for aggregations

## Next Steps

1. ✅ Connect Metabase to your database
2. 📊 Create dashboards for key metrics
3. 🔄 Set up dbt models for transformations
4. 📈 Build visualizations

See `dbt/models/olist/` for starter dbt models!
