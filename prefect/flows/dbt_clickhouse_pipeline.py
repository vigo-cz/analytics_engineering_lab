"""
dbt + ClickHouse Sync Pipeline
Orchestrates dbt transformations and syncs results to ClickHouse
"""

from prefect import flow, task
from prefect.task_runners import ConcurrentTaskRunner
import subprocess
import sys
from datetime import datetime
from pathlib import Path


@task(name="Run dbt Models", retries=2, retry_delay_seconds=30)
def run_dbt_models(target: str = "dev", select: str = None):
    """
    Run dbt models
    
    Args:
        target: dbt target (dev/prod)
        select: Optional dbt selector (e.g., 'staging.olist', 'marts.core')
    """
    print(f"🔨 Running dbt models (target={target})")
    
    cmd = [
        "dbt", "run",
        "--profiles-dir", "/workspace/dbt",
        "--project-dir", "/workspace/dbt/analytics",
        "--target", target
    ]
    
    if select:
        cmd.extend(["--select", select])
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd="/workspace/dbt/analytics"
    )
    
    if result.returncode != 0:
        print(f"❌ dbt run failed:\n{result.stderr}")
        raise Exception(f"dbt run failed: {result.stderr}")
    
    print(f"✅ dbt run completed successfully")
    print(result.stdout)
    
    return {
        "success": True,
        "output": result.stdout,
        "timestamp": datetime.now().isoformat()
    }


@task(name="Run dbt Tests", retries=1)
def run_dbt_tests(target: str = "dev"):
    """Run dbt tests to validate data quality"""
    print(f"🧪 Running dbt tests (target={target})")
    
    cmd = [
        "dbt", "test",
        "--profiles-dir", "/workspace/dbt",
        "--project-dir", "/workspace/dbt/analytics",
        "--target", target
    ]
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd="/workspace/dbt/analytics"
    )
    
    if result.returncode != 0:
        print(f"⚠️  Some dbt tests failed:\n{result.stderr}")
        # Don't raise exception - tests can fail but we still want to sync
    else:
        print(f"✅ All dbt tests passed")
    
    print(result.stdout)
    
    return {
        "success": result.returncode == 0,
        "output": result.stdout,
        "timestamp": datetime.now().isoformat()
    }


@task(name="Sync to ClickHouse", retries=3, retry_delay_seconds=60)
def sync_to_clickhouse():
    """Sync DuckDB data to ClickHouse"""
    print(f"🔄 Syncing DuckDB → ClickHouse")
    
    result = subprocess.run(
        [sys.executable, "/workspace/scripts/sync_duckdb_to_clickhouse.py"],
        capture_output=True,
        text=True,
        cwd="/workspace"
    )
    
    if result.returncode != 0:
        print(f"❌ ClickHouse sync failed:\n{result.stderr}")
        raise Exception(f"ClickHouse sync failed: {result.stderr}")
    
    print(f"✅ ClickHouse sync completed successfully")
    print(result.stdout)
    
    return {
        "success": True,
        "output": result.stdout,
        "timestamp": datetime.now().isoformat()
    }


@task(name="Generate dbt Docs")
def generate_dbt_docs(target: str = "dev"):
    """Generate dbt documentation"""
    print(f"📚 Generating dbt docs")
    
    cmd = [
        "dbt", "docs", "generate",
        "--profiles-dir", "/workspace/dbt",
        "--project-dir", "/workspace/dbt/analytics",
        "--target", target
    ]
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd="/workspace/dbt/analytics"
    )
    
    if result.returncode != 0:
        print(f"⚠️  dbt docs generation failed:\n{result.stderr}")
    else:
        print(f"✅ dbt docs generated successfully")
    
    return {
        "success": result.returncode == 0,
        "timestamp": datetime.now().isoformat()
    }


@task(name="Send Success Notification")
def send_success_notification(pipeline_results: dict):
    """Send success notification"""
    print("✅ Pipeline completed successfully!")
    print(f"📊 Results: {pipeline_results}")
    
    # TODO: Add email/Slack notification here
    # For now, just log
    
    return {"notification_sent": True}


@task(name="Send Failure Notification")
def send_failure_notification(error: Exception):
    """Send failure notification"""
    print(f"❌ Pipeline failed: {error}")
    
    # TODO: Add email/Slack notification here
    # For now, just log
    
    return {"notification_sent": True}


@flow(
    name="dbt-clickhouse-pipeline",
    description="Run dbt models and sync to ClickHouse",
    task_runner=ConcurrentTaskRunner(),
)
def dbt_clickhouse_pipeline(
    target: str = "dev",
    run_tests: bool = True,
    generate_docs: bool = True,
    sync_clickhouse: bool = True
):
    """
    Main pipeline: dbt transformations + ClickHouse sync
    
    Args:
        target: dbt target environment (dev/prod)
        run_tests: Whether to run dbt tests
        generate_docs: Whether to generate dbt docs
        sync_clickhouse: Whether to sync to ClickHouse
    """
    
    print("=" * 60)
    print("🚀 Starting dbt + ClickHouse Pipeline")
    print(f"   Target: {target}")
    print(f"   Timestamp: {datetime.now().isoformat()}")
    print("=" * 60)
    
    try:
        # Step 1: Run dbt models
        dbt_result = run_dbt_models(target=target)
        
        # Step 2: Run dbt tests (optional)
        test_result = None
        if run_tests:
            test_result = run_dbt_tests(target=target)
        
        # Step 3: Sync to ClickHouse (optional)
        sync_result = None
        if sync_clickhouse:
            sync_result = sync_to_clickhouse()
        
        # Step 4: Generate docs (optional, runs in parallel with sync)
        docs_result = None
        if generate_docs:
            docs_result = generate_dbt_docs(target=target)
        
        # Collect results
        pipeline_results = {
            "dbt_run": dbt_result,
            "dbt_tests": test_result,
            "clickhouse_sync": sync_result,
            "dbt_docs": docs_result,
            "pipeline_status": "SUCCESS"
        }
        
        # Send success notification
        send_success_notification(pipeline_results)
        
        print("=" * 60)
        print("✅ Pipeline completed successfully!")
        print("=" * 60)
        
        return pipeline_results
        
    except Exception as e:
        # Send failure notification
        send_failure_notification(e)
        
        print("=" * 60)
        print(f"❌ Pipeline failed: {e}")
        print("=" * 60)
        
        raise


# Convenience flows for specific use cases
@flow(name="dbt-staging-only")
def dbt_staging_only():
    """Run only staging models"""
    return run_dbt_models(target="dev", select="staging.olist")


@flow(name="dbt-marts-only")
def dbt_marts_only():
    """Run only mart models"""
    return run_dbt_models(target="dev", select="marts.core")


@flow(name="clickhouse-sync-only")
def clickhouse_sync_only():
    """Sync to ClickHouse without running dbt"""
    return sync_to_clickhouse()


if __name__ == "__main__":
    # Run the pipeline locally for testing
    dbt_clickhouse_pipeline(
        target="dev",
        run_tests=True,
        generate_docs=True,
        sync_clickhouse=True
    )
