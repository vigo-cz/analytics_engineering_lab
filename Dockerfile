# Analytics Engineering Lab - Docker Image
# Base: Python 3.11 slim (Debian-based)

FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /workspace

# Install system dependencies
# - git: for dbt packages and version control
# - curl: for downloading tools
# - build-essential: for compiling Python packages
# - postgresql-client: for database connections
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    build-essential \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# Copy requirements files first for better layer caching
COPY requirements.txt* ./

# Install base Python packages
RUN pip install --upgrade pip && \
    pip install \
    # Core data tools
    dbt-core \
    dbt-duckdb \
    dbt-postgres \
    # Orchestration
    prefect \
    # Data quality
    great-expectations \
    soda-core-duckdb \
    # Data science & ML
    pandas \
    numpy \
    scikit-learn \
    jupyter \
    jupyterlab \
    matplotlib \
    seaborn \
    # Data apps
    streamlit \
    plotly \
    dash \
    # Data sources
    kaggle \
    clickhouse-connect \
    # Utilities
    python-dotenv \
    pyyaml \
    requests

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p \
    /workspace/data \
    /workspace/logs \
    /workspace/.dbt

# Expose ports
# 8501: Streamlit
# 8050: Dash
# 8888: Jupyter
# 4200: Prefect UI
EXPOSE 8501 8050 8888 4200

# Default command: bash (for interactive use)
CMD ["/bin/bash"]
