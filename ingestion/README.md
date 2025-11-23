# Data Ingestion

This folder contains all data extraction and loading scripts (the "EL" in ELT).

## Structure

- **`apis/`** - API data extractors
  - REST API clients
  - GraphQL clients
  - Webhook handlers
  
- **`databases/`** - Database extractors
  - PostgreSQL extractors
  - MySQL extractors
  - MongoDB extractors
  - Other database sources

- **`files/`** - File-based extractors
  - CSV/Excel parsers
  - JSON/XML parsers
  - Parquet readers
  - S3/Cloud storage readers

## Philosophy

This folder focuses on **extraction and loading** only. Transformations happen in dbt.

### What Goes Here
✅ Extracting data from APIs  
✅ Reading from source databases  
✅ Loading raw data into warehouse  
✅ Data validation at ingestion  

### What Doesn't Go Here
❌ Data transformations (use dbt)  
❌ Business logic (use dbt)  
❌ Orchestration (use Prefect)  

## Example: API Extractor

```python
import requests
from typing import Dict, List

class APIExtractor:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
    
    def extract(self, endpoint: str) -> List[Dict]:
        """Extract data from API endpoint"""
        response = requests.get(
            f"{self.base_url}/{endpoint}",
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        response.raise_for_status()
        return response.json()
    
    def load_to_warehouse(self, data: List[Dict], table: str):
        """Load data to warehouse (raw/staging schema)"""
        # Your loading logic here
        pass
```

## Best Practices

1. **Idempotency** - Make extractions idempotent (safe to re-run)
2. **Incremental Loading** - Use timestamps/watermarks for incremental loads
3. **Error Handling** - Handle API rate limits, timeouts, retries
4. **Logging** - Log extraction metrics (rows extracted, duration, etc.)
5. **Schema Validation** - Validate data structure before loading
6. **Raw Storage** - Store raw data before any transformations

## Orchestration

All ingestion scripts should be orchestrated via Prefect flows in the `prefect/` folder.
