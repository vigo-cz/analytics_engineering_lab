#!/usr/bin/env python3
"""
Olist Brazilian E-commerce Dataset Loader for DuckDB
Downloads and loads the Olist dataset from Kaggle into DuckDB

Usage:
    python scripts/data-generation/load_olist_to_duckdb.py
"""

import os
import zipfile
import urllib.request
from pathlib import Path
import duckdb
import pandas as pd

# Configuration
DATA_DIR = Path("/workspace/data/raw/olist")
DUCKDB_PATH = Path("/workspace/data/olist_ecommerce.duckdb")
KAGGLE_DATASET_URL = "https://www.kaggle.com/api/v1/datasets/download/olistbr/brazilian-ecommerce"

# Dataset CSV files (from the Olist dataset)
CSV_FILES = {
    "customers": "olist_customers_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "product_category_name_translation": "product_category_name_translation.csv",
}


def download_dataset():
    """Download Olist dataset from Kaggle"""
    print("📥 Downloading Olist dataset from Kaggle...")
    
    # Check if Kaggle credentials exist
    kaggle_json = Path.home() / ".kaggle" / "kaggle.json"
    if not kaggle_json.exists():
        print("❌ Kaggle credentials not found!")
        print("\nTo download the dataset, you need to:")
        print("1. Go to https://www.kaggle.com/settings/account")
        print("2. Click 'Create New API Token'")
        print("3. Place kaggle.json in ~/.kaggle/")
        print("\nAlternatively, download manually from:")
        print("https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/data")
        print(f"And extract to: {DATA_DIR}")
        return False
    
    # Create data directory
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Download using Kaggle API
    try:
        import kaggle
        kaggle.api.dataset_download_files(
            'olistbr/brazilian-ecommerce',
            path=DATA_DIR,
            unzip=True
        )
        print("✅ Dataset downloaded successfully!")
        return True
    except Exception as e:
        print(f"❌ Error downloading dataset: {e}")
        print("\nPlease download manually from:")
        print("https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/data")
        print(f"And extract to: {DATA_DIR}")
        return False


def check_csv_files():
    """Check if all required CSV files exist"""
    print("\n🔍 Checking for CSV files...")
    missing_files = []
    
    for table_name, csv_file in CSV_FILES.items():
        file_path = DATA_DIR / csv_file
        if file_path.exists():
            print(f"  ✅ {csv_file}")
        else:
            print(f"  ❌ {csv_file} - MISSING")
            missing_files.append(csv_file)
    
    if missing_files:
        print(f"\n❌ Missing {len(missing_files)} files. Please download the dataset.")
        return False
    
    print("\n✅ All CSV files found!")
    return True


def create_duckdb_schema(conn):
    """Create schema in DuckDB"""
    print("\n🗄️  Creating DuckDB schema...")
    
    # Create schema
    conn.execute("CREATE SCHEMA IF NOT EXISTS raw")
    conn.execute("CREATE SCHEMA IF NOT EXISTS staging")
    
    print("✅ Schemas created: raw, staging")


def load_csv_to_duckdb(conn, table_name, csv_file):
    """Load a CSV file into DuckDB"""
    file_path = DATA_DIR / csv_file
    
    print(f"  📊 Loading {table_name}...", end=" ")
    
    try:
        # Read CSV with pandas first to handle encoding issues
        df = pd.read_csv(file_path, encoding='utf-8', low_memory=False)
        
        # Load into DuckDB
        conn.execute(f"DROP TABLE IF EXISTS raw.{table_name}")
        conn.execute(f"CREATE TABLE raw.{table_name} AS SELECT * FROM df")
        
        # Get row count
        row_count = conn.execute(f"SELECT COUNT(*) FROM raw.{table_name}").fetchone()[0]
        print(f"✅ {row_count:,} rows")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def load_all_tables(conn):
    """Load all CSV files into DuckDB"""
    print("\n📥 Loading data into DuckDB...")
    
    success_count = 0
    for table_name, csv_file in CSV_FILES.items():
        if load_csv_to_duckdb(conn, table_name, csv_file):
            success_count += 1
    
    print(f"\n✅ Loaded {success_count}/{len(CSV_FILES)} tables successfully!")
    return success_count == len(CSV_FILES)


def create_summary_views(conn):
    """Create useful summary views"""
    print("\n📊 Creating summary views...")
    
    # Orders summary
    conn.execute("""
        CREATE OR REPLACE VIEW staging.orders_summary AS
        SELECT 
            DATE_TRUNC('month', order_purchase_timestamp) as order_month,
            COUNT(*) as total_orders,
            COUNT(DISTINCT customer_id) as unique_customers,
            SUM(CASE WHEN order_status = 'delivered' THEN 1 ELSE 0 END) as delivered_orders
        FROM raw.orders
        WHERE order_purchase_timestamp IS NOT NULL
        GROUP BY 1
        ORDER BY 1
    """)
    
    # Revenue summary
    conn.execute("""
        CREATE OR REPLACE VIEW staging.revenue_summary AS
        SELECT 
            DATE_TRUNC('month', o.order_purchase_timestamp) as order_month,
            SUM(oi.price) as total_revenue,
            SUM(oi.freight_value) as total_freight,
            COUNT(DISTINCT oi.order_id) as orders_with_items,
            COUNT(*) as total_items
        FROM raw.orders o
        JOIN raw.order_items oi ON o.order_id = oi.order_id
        WHERE o.order_purchase_timestamp IS NOT NULL
        GROUP BY 1
        ORDER BY 1
    """)
    
    print("✅ Summary views created!")


def print_database_info(conn):
    """Print database statistics"""
    print("\n" + "="*60)
    print("📊 DATABASE SUMMARY")
    print("="*60)
    
    # List all tables
    tables = conn.execute("""
        SELECT table_schema, table_name, 
               (SELECT COUNT(*) FROM information_schema.tables t2 
                WHERE t2.table_schema = t1.table_schema 
                AND t2.table_name = t1.table_name) as row_count
        FROM information_schema.tables t1
        WHERE table_schema IN ('raw', 'staging')
        ORDER BY table_schema, table_name
    """).fetchall()
    
    print("\nTables:")
    for schema, table, _ in tables:
        row_count = conn.execute(f"SELECT COUNT(*) FROM {schema}.{table}").fetchone()[0]
        print(f"  {schema}.{table}: {row_count:,} rows")
    
    # Date range
    date_range = conn.execute("""
        SELECT 
            MIN(order_purchase_timestamp) as first_order,
            MAX(order_purchase_timestamp) as last_order
        FROM raw.orders
    """).fetchone()
    
    if date_range[0]:
        print(f"\nDate Range: {date_range[0]} to {date_range[1]}")
    
    print(f"\nDatabase location: {DUCKDB_PATH}")
    print("="*60)


def main():
    """Main execution function"""
    print("🚀 Olist E-commerce Dataset Loader for DuckDB")
    print("="*60)
    
    # Step 1: Check if data exists, if not try to download
    if not check_csv_files():
        print("\n📥 Attempting to download dataset...")
        if not download_dataset():
            print("\n❌ Setup failed. Please download the dataset manually.")
            return
        
        # Check again after download
        if not check_csv_files():
            print("\n❌ Setup failed. CSV files not found after download.")
            return
    
    # Step 2: Create DuckDB database
    print(f"\n🦆 Creating DuckDB database: {DUCKDB_PATH}")
    DUCKDB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = duckdb.connect(str(DUCKDB_PATH))
    
    # Step 3: Create schema
    create_duckdb_schema(conn)
    
    # Step 4: Load all tables
    if not load_all_tables(conn):
        print("\n❌ Some tables failed to load")
        return
    
    # Step 5: Create summary views
    create_summary_views(conn)
    
    # Step 6: Print summary
    print_database_info(conn)
    
    # Close connection
    conn.close()
    
    print("\n✅ Setup complete! You can now query the database:")
    print(f"\n   duckdb {DUCKDB_PATH}")
    print("\nExample queries:")
    print("   SELECT * FROM raw.orders LIMIT 5;")
    print("   SELECT * FROM staging.orders_summary;")
    print("   SELECT * FROM staging.revenue_summary;")


if __name__ == "__main__":
    main()
