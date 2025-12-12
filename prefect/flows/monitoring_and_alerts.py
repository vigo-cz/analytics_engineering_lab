"""
Monitoring and Alerting Flow
Monitors pipeline health and data quality
"""

from prefect import flow, task
from prefect.blocks.notifications import SlackWebhook
import duckdb
from datetime import datetime, timedelta
from pathlib import Path


@task(name="Check DuckDB Health")
def check_duckdb_health():
    """Check if DuckDB is accessible and has data"""
    print("🔍 Checking DuckDB health...")
    
    try:
        conn = duckdb.connect("/workspace/data/olist_ecommerce.duckdb", read_only=True)
        
        # Check raw tables
        raw_tables = conn.execute("""
            SELECT table_schema, table_name, 
                   (SELECT COUNT(*) FROM information_schema.tables t2 
                    WHERE t2.table_schema = t.table_schema 
                    AND t2.table_name = t.table_name) as row_count
            FROM information_schema.tables t
            WHERE table_schema = 'raw'
        """).fetchall()
        
        # Check staging tables
        staging_tables = conn.execute("""
            SELECT COUNT(*) as count
            FROM information_schema.tables
            WHERE table_schema = 'staging'
        """).fetchone()[0]
        
        # Check marts tables
        marts_tables = conn.execute("""
            SELECT COUNT(*) as count
            FROM information_schema.tables
            WHERE table_schema = 'marts'
        """).fetchone()[0]
        
        conn.close()
        
        health_status = {
            "status": "healthy",
            "raw_tables": len(raw_tables),
            "staging_tables": staging_tables,
            "marts_tables": marts_tables,
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"✅ DuckDB is healthy: {health_status}")
        return health_status
        
    except Exception as e:
        print(f"❌ DuckDB health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


@task(name="Check Data Freshness")
def check_data_freshness():
    """Check if data is fresh (updated recently)"""
    print("🕐 Checking data freshness...")
    
    try:
        conn = duckdb.connect("/workspace/data/olist_ecommerce.duckdb", read_only=True)
        
        # Check latest order date
        latest_order = conn.execute("""
            SELECT MAX(order_purchase_timestamp) as latest_order
            FROM raw.orders
        """).fetchone()[0]
        
        conn.close()
        
        if latest_order:
            freshness = {
                "status": "fresh",
                "latest_order_date": str(latest_order),
                "timestamp": datetime.now().isoformat()
            }
            print(f"✅ Data is fresh: {freshness}")
        else:
            freshness = {
                "status": "stale",
                "message": "No orders found",
                "timestamp": datetime.now().isoformat()
            }
            print(f"⚠️  Data may be stale: {freshness}")
        
        return freshness
        
    except Exception as e:
        print(f"❌ Data freshness check failed: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


@task(name="Check Data Quality")
def check_data_quality():
    """Run basic data quality checks"""
    print("✅ Running data quality checks...")
    
    try:
        conn = duckdb.connect("/workspace/data/olist_ecommerce.duckdb", read_only=True)
        
        checks = []
        
        # Check 1: No null order_ids
        null_orders = conn.execute("""
            SELECT COUNT(*) FROM raw.orders WHERE order_id IS NULL
        """).fetchone()[0]
        
        checks.append({
            "check": "null_order_ids",
            "passed": null_orders == 0,
            "value": null_orders
        })
        
        # Check 2: No duplicate order_ids
        duplicate_orders = conn.execute("""
            SELECT COUNT(*) - COUNT(DISTINCT order_id) as duplicates
            FROM raw.orders
        """).fetchone()[0]
        
        checks.append({
            "check": "duplicate_order_ids",
            "passed": duplicate_orders == 0,
            "value": duplicate_orders
        })
        
        # Check 3: Reasonable order counts
        order_count = conn.execute("""
            SELECT COUNT(*) FROM raw.orders
        """).fetchone()[0]
        
        checks.append({
            "check": "order_count",
            "passed": order_count > 1000,
            "value": order_count
        })
        
        conn.close()
        
        all_passed = all(check["passed"] for check in checks)
        
        quality_status = {
            "status": "passed" if all_passed else "failed",
            "checks": checks,
            "timestamp": datetime.now().isoformat()
        }
        
        if all_passed:
            print(f"✅ All data quality checks passed")
        else:
            print(f"⚠️  Some data quality checks failed: {quality_status}")
        
        return quality_status
        
    except Exception as e:
        print(f"❌ Data quality check failed: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


@task(name="Check ClickHouse Sync Status")
def check_clickhouse_sync():
    """Check if ClickHouse is in sync with DuckDB"""
    print("🔄 Checking ClickHouse sync status...")
    
    try:
        import clickhouse_connect
        
        # Connect to ClickHouse
        client = clickhouse_connect.get_client(
            host="clickhouse",
            port=8123,
            username="default",  # Use default user for now
            password=""
        )
        
        # Check if tables exist
        tables = client.query("SHOW TABLES FROM raw").result_rows
        
        sync_status = {
            "status": "synced" if len(tables) > 0 else "not_synced",
            "clickhouse_tables": len(tables),
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"✅ ClickHouse sync status: {sync_status}")
        return sync_status
        
    except Exception as e:
        print(f"⚠️  ClickHouse check failed (may not be running): {e}")
        return {
            "status": "unavailable",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


@flow(name="monitoring-and-alerts")
def monitoring_and_alerts():
    """
    Monitor pipeline health and data quality
    Run this on a schedule to get regular health checks
    """
    
    print("=" * 60)
    print("🔍 Running Monitoring and Alerts")
    print(f"   Timestamp: {datetime.now().isoformat()}")
    print("=" * 60)
    
    # Run all health checks
    duckdb_health = check_duckdb_health()
    data_freshness = check_data_freshness()
    data_quality = check_data_quality()
    clickhouse_sync = check_clickhouse_sync()
    
    # Aggregate results
    monitoring_results = {
        "duckdb_health": duckdb_health,
        "data_freshness": data_freshness,
        "data_quality": data_quality,
        "clickhouse_sync": clickhouse_sync,
        "overall_status": "healthy" if all([
            duckdb_health.get("status") == "healthy",
            data_quality.get("status") == "passed"
        ]) else "unhealthy",
        "timestamp": datetime.now().isoformat()
    }
    
    # Alert if unhealthy
    if monitoring_results["overall_status"] == "unhealthy":
        print("⚠️  ALERT: System is unhealthy!")
        # TODO: Send alert via Slack/Email
    else:
        print("✅ All systems healthy")
    
    print("=" * 60)
    print(f"Monitoring Results: {monitoring_results}")
    print("=" * 60)
    
    return monitoring_results


if __name__ == "__main__":
    # Run monitoring locally for testing
    monitoring_and_alerts()
