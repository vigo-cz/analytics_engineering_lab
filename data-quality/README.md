# Data Quality

This folder contains data quality testing and validation tools.

## Structure

- **`great-expectations/`** - Great Expectations suites
  - Expectation suites
  - Validation results
  - Data docs

- **`soda/`** - Soda Core checks
  - YAML check definitions
  - Scan results
  - Metrics

- **`custom/`** - Custom data quality checks
  - Python validation scripts
  - SQL quality queries
  - Custom metrics

## Philosophy

Data quality is critical for analytics. This folder complements dbt tests with more comprehensive validation.

### Testing Layers

| Layer | Tool | Purpose |
|-------|------|---------|
| **dbt tests** | dbt | Schema tests, uniqueness, relationships |
| **Data Quality** | Great Expectations/Soda | Comprehensive validation, anomaly detection |
| **Integration tests** | pytest | End-to-end pipeline tests |

## Great Expectations

Great Expectations provides comprehensive data validation.

### Setup
```bash
pip install great-expectations
great_expectations init
```

### Example Expectation Suite
```python
import great_expectations as gx

context = gx.get_context()

# Create expectation suite
suite = context.add_expectation_suite("customers_suite")

# Add expectations
validator = context.get_validator(
    batch_request=batch_request,
    expectation_suite_name="customers_suite"
)

validator.expect_column_values_to_not_be_null("customer_id")
validator.expect_column_values_to_be_unique("customer_id")
validator.expect_column_values_to_be_between("age", min_value=0, max_value=120)

validator.save_expectation_suite()
```

### Run Validations
```bash
great_expectations checkpoint run customers_checkpoint
```

## Soda Core

Soda Core uses YAML to define data quality checks.

### Setup
```bash
pip install soda-core-duckdb  # or your database
```

### Example Checks (`soda/checks.yml`)
```yaml
checks for customers:
  - row_count > 0
  - missing_count(customer_id) = 0
  - duplicate_count(customer_id) = 0
  - invalid_count(email) = 0:
      valid format: email
  - avg(age) between 18 and 80
  - freshness(created_at) < 1d
```

### Run Checks
```bash
soda scan -d my_warehouse -c soda/configuration.yml soda/checks.yml
```

## Custom Checks

For checks not covered by GE or Soda, write custom Python scripts.

### Example
```python
import pandas as pd

def check_revenue_anomaly(df: pd.DataFrame) -> bool:
    """Check if today's revenue is within 3 std devs of mean"""
    mean = df['revenue'].mean()
    std = df['revenue'].std()
    today = df['revenue'].iloc[-1]
    
    return abs(today - mean) <= 3 * std
```

## Integration with Prefect

Run data quality checks as part of your Prefect flows:

```python
from prefect import flow, task
import great_expectations as gx

@task
def validate_data():
    context = gx.get_context()
    results = context.run_checkpoint("customers_checkpoint")
    
    if not results["success"]:
        raise ValueError("Data quality check failed!")

@flow
def etl_pipeline():
    extract_data()
    load_data()
    validate_data()  # Run after loading
    run_dbt()
```

## Best Practices

1. **Test early** - Validate data at ingestion
2. **Test often** - Run checks after every transformation
3. **Alert on failures** - Integrate with Slack/email notifications
4. **Document expectations** - Make data contracts explicit
5. **Version control** - Commit all check definitions

## Resources

- [Great Expectations Documentation](https://docs.greatexpectations.io/)
- [Soda Core Documentation](https://docs.soda.io/)
