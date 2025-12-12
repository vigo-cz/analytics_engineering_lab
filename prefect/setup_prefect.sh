#!/bin/bash
#
# Start Prefect Server and Deploy Flows
# Run this to set up Prefect in Docker
#

set -e

echo "🚀 Starting Prefect Setup"
echo "=" * 60

# Start Prefect server in background
echo "📡 Starting Prefect server..."
prefect server start --host 0.0.0.0 &
PREFECT_PID=$!

# Wait for server to be ready
echo "⏳ Waiting for Prefect server to start..."
sleep 10

# Set Prefect API URL
export PREFECT_API_URL="http://localhost:4200/api"

# Create work pool
echo "🏊 Creating work pool..."
prefect work-pool create --type process default-pool || echo "Work pool already exists"

# Deploy flows
echo "📦 Deploying flows..."

# Deploy main pipeline
prefect deployment build \
    /workspace/prefect/flows/dbt_clickhouse_pipeline.py:dbt_clickhouse_pipeline \
    --name "dbt-clickhouse-daily" \
    --pool default-pool \
    --cron "0 2 * * *" \
    --output /workspace/prefect/deployments/dbt_clickhouse_daily.yaml

prefect deployment apply /workspace/prefect/deployments/dbt_clickhouse_daily.yaml

# Deploy monitoring flow
prefect deployment build \
    /workspace/prefect/flows/monitoring_and_alerts.py:monitoring_and_alerts \
    --name "monitoring-hourly" \
    --pool default-pool \
    --cron "0 * * * *" \
    --output /workspace/prefect/deployments/monitoring_hourly.yaml

prefect deployment apply /workspace/prefect/deployments/monitoring_hourly.yaml

echo "✅ Prefect setup complete!"
echo ""
echo "🌐 Prefect UI: http://localhost:4200"
echo ""
echo "📋 Deployments created:"
echo "  - dbt-clickhouse-daily (runs at 2 AM daily)"
echo "  - monitoring-hourly (runs every hour)"
echo ""
echo "🏃 To start a worker:"
echo "  prefect worker start --pool default-pool"
echo ""
echo "🧪 To test flows manually:"
echo "  python /workspace/prefect/flows/dbt_clickhouse_pipeline.py"
echo "  python /workspace/prefect/flows/monitoring_and_alerts.py"
