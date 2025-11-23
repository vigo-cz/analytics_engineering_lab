"""
Example Airflow DAG for data pipeline orchestration.

This is a starter template for creating your own DAGs.
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'analytics_engineering_lab',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def extract_data(**context):
    """Extract data from source."""
    print("Extracting data...")
    return {"status": "success", "records": 100}

def transform_data(**context):
    """Transform extracted data."""
    print("Transforming data...")
    return {"status": "success"}

def load_data(**context):
    """Load transformed data."""
    print("Loading data...")
    return {"status": "success"}

with DAG(
    'example_etl_pipeline',
    default_args=default_args,
    description='Example ETL pipeline',
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=['example', 'etl'],
) as dag:

    extract = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
    )

    transform = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
    )

    load = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
    )

    # Define task dependencies
    extract >> transform >> load
