# Docker Infrastructure

This folder contains Docker-related configurations and documentation for the analytics engineering lab.

## Overview

The Docker setup provides a complete, reproducible analytics environment with:
- **Python 3.11** analytics workspace
- **PostgreSQL** database
- **Metabase** BI tool
- All necessary Python packages pre-installed

## Quick Start

### Build and Run

```bash
# Build the Docker image
docker-compose build

# Start all services
docker-compose up -d

# Access the analytics workspace
docker-compose exec analytics-lab bash
```

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (⚠️ deletes data)
docker-compose down -v
```

## Services

### 1. Analytics Lab (Main Workspace)

**Container**: `analytics-lab`  
**Base Image**: `python:3.11-slim`  
**Ports**:
- `8501` - Streamlit apps
- `8050` - Dash apps
- `8888` - Jupyter Lab
- `4200` - Prefect UI

**Access**:
```bash
# Interactive shell
docker-compose exec analytics-lab bash

# Run Jupyter Lab
docker-compose exec analytics-lab jupyter lab --ip=0.0.0.0 --allow-root

# Run Streamlit app
docker-compose exec analytics-lab streamlit run apps/streamlit/my_app.py
```

### 2. PostgreSQL

**Container**: `analytics-postgres`  
**Port**: `5432`  
**Credentials**:
- User: `analytics`
- Password: `analytics_password`
- Database: `analytics_db`

**Connect from host**:
```bash
psql -h localhost -U analytics -d analytics_db
```

**Connect from analytics-lab container**:
```bash
psql -h postgres -U analytics -d analytics_db
```

### 3. Metabase

**Container**: `analytics-metabase`  
**Port**: `3000`  
**Access**: http://localhost:3000

First-time setup:
1. Open http://localhost:3000
2. Create admin account
3. Connect to PostgreSQL:
   - Host: `postgres`
   - Port: `5432`
   - Database: `analytics_db`
   - User: `analytics`
   - Password: `analytics_password`

## Development Workflow

### 1. Start Environment

```bash
docker-compose up -d
```

### 2. Work in Container

```bash
# Enter container
docker-compose exec analytics-lab bash

# Your code is mounted at /workspace
cd /workspace

# Run dbt
cd dbt/analytics
dbt run

# Run Prefect flow
python prefect/flows/my_flow.py

# Start Jupyter
jupyter lab --ip=0.0.0.0 --allow-root
```

### 3. Access Services

- **Jupyter Lab**: http://localhost:8888
- **Streamlit**: http://localhost:8501
- **Metabase**: http://localhost:3000
- **PostgreSQL**: `localhost:5432`

## Customization

### Add Python Packages

**Option 1: Temporary (lost on rebuild)**
```bash
docker-compose exec analytics-lab pip install package-name
```

**Option 2: Permanent (edit Dockerfile)**
```dockerfile
# In Dockerfile, add to pip install section
RUN pip install \
    existing-package \
    new-package
```

Then rebuild:
```bash
docker-compose build analytics-lab
```

### Add System Packages

Edit `Dockerfile`:
```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    existing-package \
    new-package \
    && rm -rf /var/lib/apt/lists/*
```

## Volumes

Persistent data is stored in Docker volumes:

- `analytics-data` - Data files
- `dbt-artifacts` - dbt compiled models
- `postgres-data` - PostgreSQL database
- `metabase-data` - Metabase configurations

**View volumes**:
```bash
docker volume ls
```

**Backup volume**:
```bash
docker run --rm -v analytics-data:/data -v $(pwd):/backup alpine tar czf /backup/analytics-data-backup.tar.gz /data
```

## Troubleshooting

### Container won't start
```bash
# Check logs
docker-compose logs analytics-lab

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Port already in use
```bash
# Find process using port
lsof -i :8501

# Change port in docker-compose.yml
ports:
  - "8502:8501"  # Use 8502 on host instead
```

### Out of disk space
```bash
# Clean up Docker
docker system prune -a
docker volume prune
```

## Production Deployment

For production, consider:

1. **Use specific versions** instead of `latest`
2. **Set proper secrets** (not hardcoded passwords)
3. **Use environment files** (`.env`)
4. **Add health checks**
5. **Configure logging**
6. **Use Docker secrets** for sensitive data

Example production `docker-compose.yml`:
```yaml
services:
  analytics-lab:
    image: your-registry/analytics-lab:v1.0.0
    env_file: .env.production
    restart: unless-stopped
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Python Docker Images](https://hub.docker.com/_/python)
