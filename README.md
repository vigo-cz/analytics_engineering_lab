# Analytics Engineering Lab

A comprehensive workspace for experimenting with modern data stack technologies, analytics engineering, and machine learning workflows.

## 🎯 Purpose

This repository serves as a sandbox for:
- **Analytics Engineering**: dbt models, transformations, and data modeling
- **Workflow Orchestration**: Airflow, Prefect, Dagster experiments
- **Database Technologies**: DuckDB, ClickHouse, TimescaleDB, PostgreSQL
- **Data Science & ML**: Jupyter notebooks, model training, and experiments
- **ETL/ELT Pipelines**: Data extraction, transformation, and loading scripts
- **Stream Processing**: Kafka, Flink, Spark streaming

## 🏗️ Structure

```
analytics_engineering_lab/
├── dbt/                    # dbt projects
├── airflow/                # Airflow DAGs and configs
├── databases/              # Database experiments
├── data-science/           # Data science projects
├── ml/                     # Machine learning projects
├── etl/                    # ETL/ELT scripts
├── streaming/              # Stream processing
├── orchestration/          # Workflow orchestration
├── infrastructure/         # Infrastructure as Code
├── scripts/                # Utility scripts
├── tests/                  # Integration/E2E tests
├── docs/                   # Documentation
└── config/                 # Shared configurations
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose (optional)
- Git

### Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd analytics_engineering_lab

# Set up Python virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies (per project)
cd dbt/analytics && pip install -r requirements.txt
```

## 🛠️ Technologies

### Data Transformation
- **dbt**: Data transformation and modeling
- **SQL**: DuckDB, PostgreSQL, ClickHouse, TimescaleDB

### Orchestration
- **Apache Airflow**: Workflow orchestration
- **Prefect**: Modern workflow orchestration
- **Dagster**: Data orchestration platform

### Data Science & ML
- **Jupyter**: Interactive notebooks
- **scikit-learn**: Machine learning
- **pandas**: Data manipulation
- **MLflow**: ML experiment tracking

### Databases
- **DuckDB**: Embedded analytical database
- **ClickHouse**: OLAP database
- **TimescaleDB**: Time-series database
- **PostgreSQL**: Relational database

## 📚 Documentation

See the [docs/](./docs/) folder for:
- Architecture diagrams
- How-to guides
- Decision records (ADRs)

## 🤝 Contributing

This is a personal learning lab, but feel free to fork and adapt for your own use!

## 📝 License

MIT License - feel free to use and modify as needed.
