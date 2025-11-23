# dbt Projects

This directory contains dbt projects for analytics engineering.

## Structure

- `analytics/` - Main production analytics project
- `experiments/` - Experimental models and POCs

## Setup

```bash
cd analytics
python3.11 -m venv venv
source venv/bin/activate
pip install dbt-core dbt-duckdb dbt-snowflake dbt-postgres
```

## Usage

```bash
# Run all models
dbt run

# Run specific model
dbt run --select my_model

# Test models
dbt test

# Build (run + test)
dbt build

# Generate documentation
dbt docs generate
dbt docs serve
```
