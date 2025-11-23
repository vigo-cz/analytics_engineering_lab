# Airflow

Apache Airflow DAGs and configurations for workflow orchestration.

## Structure

- `dags/` - DAG definitions
- `plugins/` - Custom operators, hooks, and sensors
- `config/` - Airflow configuration files
- `tests/` - DAG unit tests

## Setup

```bash
pip install apache-airflow
airflow db init
airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com
```

## Usage

```bash
# Start webserver
airflow webserver --port 8080

# Start scheduler
airflow scheduler

# Test DAG
airflow dags test my_dag 2024-01-01
```
