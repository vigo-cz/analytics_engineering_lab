# Prefect Orchestration - Quick Start

Complete guide for running Prefect orchestration in your analytics lab.

## What's Included

### Flows

1. **`dbt_clickhouse_pipeline.py`** - Main pipeline
   - Runs dbt models (staging + marts)
   - Runs dbt tests
   - Syncs to ClickHouse
   - Generates dbt docs
   - Includes retries and error handling

2. **`monitoring_and_alerts.py`** - Health monitoring
   - DuckDB health checks
   - Data freshness validation
   - Data quality checks
   - ClickHouse sync status
   - Automated alerts

## Quick Start

### 1. Start Prefect Server

```bash
# Inside Docker container
docker exec -it analytics-lab bash

# Start Prefect server
prefect server start --host 0.0.0.0
```

**Prefect UI**: http://localhost:4200

### 2. Run Flows Manually (Testing)

```bash
# Test main pipeline
docker exec -it analytics-lab python /workspace/prefect/flows/dbt_clickhouse_pipeline.py

# Test monitoring
docker exec -it analytics-lab python /workspace/prefect/flows/monitoring_and_alerts.py
```

### 3. Deploy Flows (Automated)

```bash
# Run setup script
docker exec -it analytics-lab bash /workspace/prefect/setup_prefect.sh
```

This creates:
- **dbt-clickhouse-daily**: Runs at 2 AM daily
- **monitoring-hourly**: Runs every hour

### 4. Start Worker

```bash
# In a separate terminal
docker exec -it analytics-lab prefect worker start --pool default-pool
```

## Usage Examples

### Run Full Pipeline

```python
from prefect.deployments import run_deployment

# Trigger deployment
run_deployment(
    name="dbt-clickhouse-pipeline/dbt-clickhouse-daily"
)
```

### Run Specific Steps

```bash
# Run only staging models
docker exec -it analytics-lab python -c "
from prefect.flows.dbt_clickhouse_pipeline import dbt_staging_only
dbt_staging_only()
"

# Run only ClickHouse sync
docker exec -it analytics-lab python -c "
from prefect.flows.dbt_clickhouse_pipeline import clickhouse_sync_only
clickhouse_sync_only()
"
```

### Check Monitoring Status

```bash
docker exec -it analytics-lab python /workspace/prefect/flows/monitoring_and_alerts.py
```

## Pipeline Features

### Retry Logic

- **dbt run**: 2 retries with 30s delay
- **ClickHouse sync**: 3 retries with 60s delay
- **dbt tests**: 1 retry

### Monitoring Checks

✅ DuckDB connectivity  
✅ Table counts (raw, staging, marts)  
✅ Data freshness (latest order date)  
✅ Data quality (nulls, duplicates, counts)  
✅ ClickHouse sync status  

### Notifications

Currently logs to console. To add Slack/Email:

1. **Slack**:
```python
from prefect.blocks.notifications import SlackWebhook

slack_webhook = SlackWebhook(url="your-webhook-url")
slack_webhook.notify("Pipeline failed!")
```

2. **Email** (via Prefect Cloud):
```python
from prefect.blocks.notifications import EmailServerCredentials

email = EmailServerCredentials(...)
email.notify("Pipeline failed!")
```

## Schedules

### Current Schedules

| Flow | Schedule | Cron |
|------|----------|------|
| dbt-clickhouse-daily | Daily at 2 AM | `0 2 * * *` |
| monitoring-hourly | Every hour | `0 * * * *` |

### Change Schedule

Edit deployment YAML:

```yaml
# prefect/deployments/dbt_clickhouse_daily.yaml
schedule:
  cron: "0 6 * * *"  # Change to 6 AM
  timezone: "America/New_York"
```

Then apply:
```bash
prefect deployment apply prefect/deployments/dbt_clickhouse_daily.yaml
```

## Troubleshooting

### Prefect Server Won't Start

```bash
# Check if port 4200 is in use
lsof -i :4200

# Kill existing process
kill -9 <PID>

# Restart server
prefect server start --host 0.0.0.0
```

### Flow Fails

```bash
# Check logs in Prefect UI
# Or view in terminal
prefect flow-run logs <flow-run-id>
```

### Worker Not Picking Up Runs

```bash
# Check work pool
prefect work-pool ls

# Restart worker
prefect worker start --pool default-pool
```

## Advanced Usage

### Run with Custom Parameters

```python
from prefect.flows.dbt_clickhouse_pipeline import dbt_clickhouse_pipeline

# Run with custom config
dbt_clickhouse_pipeline(
    target="prod",
    run_tests=True,
    generate_docs=False,
    sync_clickhouse=True
)
```

### Add Custom Tasks

```python
from prefect import task

@task(name="Custom Task")
def my_custom_task():
    # Your logic here
    pass

# Add to pipeline
@flow
def my_pipeline():
    run_dbt_models()
    my_custom_task()
    sync_to_clickhouse()
```

## Monitoring Dashboard

Access Prefect UI at http://localhost:4200 to see:

- 📊 Flow run history
- ⏱️ Execution times
- ❌ Failed runs
- 📈 Success rates
- 📅 Upcoming scheduled runs

## Next Steps

1. ✅ Test flows manually
2. ✅ Deploy with schedules
3. ✅ Start worker
4. ✅ Monitor in UI
5. 🔔 Add Slack/Email notifications
6. 📊 Create custom dashboards
7. 🔄 Add more flows (data ingestion, etc.)

## Resources

- [Prefect Docs](https://docs.prefect.io/)
- [Prefect Cloud](https://www.prefect.io/cloud/)
- [dbt Docs](https://docs.getdbt.com/)
