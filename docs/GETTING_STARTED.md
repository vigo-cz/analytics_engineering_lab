# Getting Started

Welcome to the Analytics Engineering Lab! This guide will help you get started.

## Prerequisites

- **Python 3.11+**: Required for most projects
- **Docker**: Optional, for containerized services
- **Git**: Version control

## Initial Setup

### 1. Clone and Navigate
```bash
git clone <your-repo-url>
cd analytics_engineering_lab
```

### 2. Choose Your Path

#### For dbt Development
```bash
cd dbt/analytics
python3.11 -m venv venv
source venv/bin/activate
pip install dbt-core dbt-duckdb
dbt debug
```

#### For Airflow
```bash
cd airflow
pip install apache-airflow
airflow db init
```

#### For Data Science
```bash
cd data-science
pip install jupyter pandas numpy matplotlib seaborn
jupyter notebook
```

## Project Organization Tips

1. **Use virtual environments** for each project
2. **Document your experiments** in notebooks or markdown
3. **Commit often** with descriptive messages
4. **Keep data files small** or use .gitignore
5. **Add README files** to new directories

## Next Steps

- Explore the [dbt/](../dbt/) directory for analytics engineering
- Check out [airflow/](../airflow/) for orchestration examples
- Browse [data-science/notebooks/](../data-science/notebooks/) for analysis templates

## Resources

- [dbt Documentation](https://docs.getdbt.com/)
- [Airflow Documentation](https://airflow.apache.org/docs/)
- [DuckDB Documentation](https://duckdb.org/docs/)
