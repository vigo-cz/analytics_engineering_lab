# Fix for Metabase Connection Issue

## Problem
Metabase was failing with: `FATAL: database "metabase" does not exist`

## Solution
Added PostgreSQL initialization script to create the `metabase` database automatically.

## Files Changed
1. `docker-compose.yml` - Added init script mount
2. `infrastructure/docker/init-db.sh` - New database initialization script

## Steps to Fix on Windows

### 1. Pull Latest Changes
```bash
git pull origin main
```

### 2. Stop and Remove Existing Containers
```bash
docker compose down -v
```
**Note**: The `-v` flag removes volumes, which is necessary to reset the database.

### 3. Restart Everything
```bash
docker compose up -d
```

### 4. Check Metabase Logs
```bash
docker compose logs -f metabase
```

Wait for: `Metabase Initialization COMPLETE` (takes 2-5 minutes)

### 5. Access Metabase
Open browser: `http://localhost:3000`

## What the Fix Does

The `init-db.sh` script runs when PostgreSQL starts for the first time and creates:
- `analytics_db` (default, for dbt/Prefect)
- `metabase` (for Metabase application data)

Both databases use the same user (`analytics`) and password (`analytics_password`).

## Troubleshooting

If it still doesn't work:

```bash
# Check if databases were created
docker exec analytics-postgres psql -U analytics -c "\l"

# Should see both:
# - analytics_db
# - metabase
```

If you don't see `metabase`, the init script didn't run. Make sure you used `-v` flag when stopping containers.
