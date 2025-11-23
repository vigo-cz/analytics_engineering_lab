# Analytics Engineering Lab

A comprehensive workspace for experimenting with modern data stack technologies, analytics engineering, and machine learning workflows.

## 🎯 Purpose

This repository serves as a sandbox for:
- **Analytics Engineering**: dbt models, transformations, and data modeling
- **Workflow Orchestration**: Prefect-based pipeline orchestration
- **Database Technologies**: DuckDB, ClickHouse, TimescaleDB, PostgreSQL
- **Data Science & ML**: Jupyter notebooks, model training, and experiments
- **Data Quality**: Great Expectations, Soda Core, and custom validation
- **BI & Analytics**: Metabase, Lightdash dashboards
- **Data Applications**: Streamlit, Dash, Gradio apps
- **Stream Processing**: Kafka, Flink, Spark streaming

## 🏗️ Structure

```
analytics_engineering_lab/
├── prefect/                # Prefect flows & orchestration
│   ├── flows/             # Flow definitions
│   ├── deployments/       # Deployment configs
│   └── blocks/            # Prefect blocks
├── dbt/                    # dbt projects (transformation layer)
├── ingestion/              # Data extraction & loading (EL in ELT)
│   ├── apis/              # API extractors
│   ├── databases/         # Database extractors
│   └── files/             # File extractors
├── bi/                     # BI tools & dashboards
│   ├── metabase/          # Metabase configs
│   └── lightdash/         # Lightdash (dbt-native BI)
├── apps/                   # Data applications
│   ├── streamlit/         # Streamlit apps
│   ├── dash/              # Plotly Dash apps
│   └── gradio/            # Gradio ML apps
├── data-quality/           # Data quality & testing
│   ├── great-expectations/ # GE suites
│   ├── soda/              # Soda Core checks
│   └── custom/            # Custom checks
├── databases/              # Database experiments & configs
├── data-science/           # Ad-hoc analysis & exploratory notebooks
├── ml/                     # Production ML systems & pipelines
│   ├── models/            # Trained models
│   ├── experiments/       # MLflow experiments
│   └── pipelines/         # ML pipelines
├── streaming/              # Stream processing
├── infrastructure/         # Infrastructure as Code
│   ├── docker/            # Docker configs
│   └── terraform/         # Terraform configs
├── scripts/                # Utility scripts
├── tests/                  # Integration/E2E tests
├── docs/                   # Documentation
└── config/                 # Shared configurations
```

### 🔬 Data Science vs ML - What's the Difference?

**`data-science/`** - Exploratory & Ad-hoc Analysis
- 📊 Jupyter notebooks for exploratory data analysis (EDA)
- 📈 One-off analyses and investigations
- 📑 Reports and findings
- 🔍 Prototyping and experimentation
- **Temporary/exploratory** work that may not be productionized

**`ml/`** - Production ML Systems
- 🤖 Production-ready trained models
- 🔄 Automated ML pipelines (training, inference, retraining)
- 📊 MLflow experiment tracking and model registry
- 🚀 Model serving code (APIs, batch inference)
- **Long-lived, versioned, monitored** systems

**Workflow**: Start exploring in `data-science/`, then productionize valuable models in `ml/`.

## 🧪 Testing Strategy

### dbt Tests (`dbt/tests/`)
- **Schema tests**: uniqueness, not_null, relationships
- **Data quality tests**: custom SQL assertions
- **Run with**: `dbt test`
- **Purpose**: Validate transformed data models

### Integration Tests (`tests/`)
- **End-to-end pipeline tests**: ingestion → dbt → BI
- **Prefect flow tests**: orchestration validation
- **Cross-system tests**: database connections, API availability
- **Run with**: `pytest`
- **Purpose**: Validate entire system integration

### Data Quality (`data-quality/`)
- **Great Expectations**: Comprehensive data validation
- **Soda Core**: YAML-based quality checks
- **Custom checks**: Python/SQL validation scripts
- **Purpose**: Continuous data quality monitoring

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
- **Prefect**: Modern workflow orchestration platform

### Data Quality
- **Great Expectations**: Data validation and profiling
- **Soda Core**: Data quality checks

### BI & Visualization
- **Metabase**: General-purpose BI tool
- **Lightdash**: dbt-native BI platform

### Data Applications
- **Streamlit**: Interactive data apps
- **Dash**: Production-grade dashboards
- **Gradio**: ML model interfaces

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

Each major folder also contains its own README with specific guidance.

## 🤝 Contributing

This is a personal learning lab, but feel free to fork and adapt for your own use!

## 📝 License

MIT License - feel free to use and modify as needed.

