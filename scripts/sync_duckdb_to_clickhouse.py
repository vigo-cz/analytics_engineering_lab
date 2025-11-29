#!/usr/bin/env python3
"""
Sync Olist data from DuckDB to ClickHouse
Reads from DuckDB and writes to ClickHouse for remote query access

Usage:
    python scripts/sync_duckdb_to_clickhouse.py
"""

import duckdb
import clickhouse_connect
from pathlib import Path

# Configuration
DUCKDB_PATH = Path("/workspace/data/olist_ecommerce.duckdb")
CLICKHOUSE_HOST = "clickhouse"
CLICKHOUSE_PORT = 8123
CLICKHOUSE_USER = "analytics"
CLICKHOUSE_PASSWORD = "analytics_password"
CLICKHOUSE_DATABASE = "olist"

# Tables to sync (schema.table)
TABLES_TO_SYNC = [
    # Raw tables
    ("raw", "customers"),
    ("raw", "geolocation"),
    ("raw", "order_items"),
    ("raw", "order_payments"),
    ("raw", "order_reviews"),
    ("raw", "orders"),
    ("raw", "products"),
    ("raw", "sellers"),
    ("raw", "product_category_name_translation"),
]


def get_clickhouse_type(duckdb_type):
    """Map DuckDB types to ClickHouse types"""
    type_map = {
        'BIGINT': 'Int64',
        'INTEGER': 'Int32',
        'DOUBLE': 'Float64',
        'VARCHAR': 'String',
        'TIMESTAMP': 'DateTime',
        'DATE': 'Date',
        'BOOLEAN': 'UInt8',
    }
    
    duckdb_type_upper = duckdb_type.upper()
    for duck_type, click_type in type_map.items():
        if duck_type in duckdb_type_upper:
            return click_type
    
    # Default to String for unknown types
    return 'String'


def create_clickhouse_table(ch_client, schema, table, columns):
    """Create ClickHouse table with appropriate schema"""
    
    # Create database if not exists
    ch_client.command(f"CREATE DATABASE IF NOT EXISTS {schema}")
    
    # Build column definitions
    col_defs = []
    for col_name, col_type in columns:
        ch_type = get_clickhouse_type(col_type)
        # Make all columns Nullable for simplicity
        col_defs.append(f"`{col_name}` Nullable({ch_type})")
    
    columns_sql = ",\n    ".join(col_defs)
    
    # Drop and recreate table
    ch_client.command(f"DROP TABLE IF EXISTS {schema}.{table}")
    
    create_sql = f"""
    CREATE TABLE {schema}.{table} (
        {columns_sql}
    ) ENGINE = MergeTree()
    ORDER BY tuple()
    """
    
    ch_client.command(create_sql)
    print(f"  ✅ Created table {schema}.{table}")


def sync_table(duck_conn, ch_client, schema, table):
    """Sync a single table from DuckDB to ClickHouse"""
    
    print(f"\n📊 Syncing {schema}.{table}...")
    
    # Get table schema from DuckDB
    schema_query = f"""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = '{schema}' AND table_name = '{table}'
        ORDER BY ordinal_position
    """
    columns = duck_conn.execute(schema_query).fetchall()
    
    if not columns:
        print(f"  ⚠️  Table {schema}.{table} not found in DuckDB")
        return
    
    # Create ClickHouse table
    create_clickhouse_table(ch_client, schema, table, columns)
    
    # Read data from DuckDB
    df = duck_conn.execute(f"SELECT * FROM {schema}.{table}").df()
    row_count = len(df)
    
    if row_count == 0:
        print(f"  ℹ️  No data to sync")
        return
    
    # Handle NaT and NaN values properly
    # Convert timestamp columns to handle NaT
    import pandas as pd
    import numpy as np
    
    for col in df.columns:
        # Check if column is datetime type
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            # Replace NaT with None
            df[col] = df[col].replace({pd.NaT: None})
        # Replace NaN with None for all columns
        elif df[col].dtype == 'float64' or df[col].dtype == 'float32':
            df[col] = df[col].replace({np.nan: None})
    
    # Convert DataFrame to list of tuples for ClickHouse
    # Use fillna(None) as final safety net
    df = df.fillna(value=None)
    data = [tuple(row) for row in df.values]
    
    # Insert into ClickHouse
    column_names = [col[0] for col in columns]
    ch_client.insert(
        f"{schema}.{table}",
        data,
        column_names=column_names
    )
    
    print(f"  ✅ Synced {row_count:,} rows")


def sync_dbt_models(duck_conn, ch_client):
    """Sync dbt staging and mart models if they exist"""
    
    print("\n🔄 Checking for dbt models...")
    
    # Check if staging schema exists
    staging_tables = duck_conn.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'staging'
    """).fetchall()
    
    if staging_tables:
        print(f"\n📊 Found {len(staging_tables)} staging models")
        for (table,) in staging_tables:
            sync_table(duck_conn, ch_client, 'staging', table)
    
    # Check if marts schema exists
    marts_tables = duck_conn.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'marts'
    """).fetchall()
    
    if marts_tables:
        print(f"\n📊 Found {len(marts_tables)} mart models")
        for (table,) in marts_tables:
            sync_table(duck_conn, ch_client, 'marts', table)


def main():
    """Main sync function"""
    
    print("🚀 DuckDB → ClickHouse Sync")
    print("=" * 60)
    
    # Connect to DuckDB
    print(f"\n🦆 Connecting to DuckDB: {DUCKDB_PATH}")
    duck_conn = duckdb.connect(str(DUCKDB_PATH), read_only=True)
    
    # Connect to ClickHouse
    print(f"🏠 Connecting to ClickHouse: {CLICKHOUSE_HOST}:{CLICKHOUSE_PORT}")
    ch_client = clickhouse_connect.get_client(
        host=CLICKHOUSE_HOST,
        port=CLICKHOUSE_PORT,
        username=CLICKHOUSE_USER,
        password=CLICKHOUSE_PASSWORD
    )
    
    # Sync raw tables
    print("\n" + "=" * 60)
    print("📥 Syncing Raw Tables")
    print("=" * 60)
    
    for schema, table in TABLES_TO_SYNC:
        sync_table(duck_conn, ch_client, schema, table)
    
    # Sync dbt models if they exist
    sync_dbt_models(duck_conn, ch_client)
    
    # Print summary
    print("\n" + "=" * 60)
    print("✅ Sync Complete!")
    print("=" * 60)
    
    # Show table counts
    print("\n📊 ClickHouse Table Summary:")
    
    for schema in ['raw', 'staging', 'marts']:
        tables = ch_client.query(f"""
            SELECT name, total_rows
            FROM system.tables
            WHERE database = '{schema}'
            ORDER BY name
        """).result_rows
        
        if tables:
            print(f"\n{schema.upper()} Schema:")
            for table_name, row_count in tables:
                print(f"  {table_name}: {row_count:,} rows")
    
    # Close connections
    duck_conn.close()
    ch_client.close()
    
    print("\n🎉 You can now query ClickHouse!")
    print(f"   HTTP: http://localhost:8123")
    print(f"   User: {CLICKHOUSE_USER}")
    print(f"   Database: raw, staging, marts")


if __name__ == "__main__":
    main()
