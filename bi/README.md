# Business Intelligence Tools

This folder contains configurations, dashboards, and assets for BI tools.

## Structure

- **`metabase/`** - Metabase configurations
  - Dashboard exports (JSON)
  - Question exports
  - Collection organization
  - Embedding configurations

- **`lightdash/`** - Lightdash (dbt-native BI)
  - Custom metrics
  - Dashboard configurations
  - Chart definitions

## Metabase

### Setup
```bash
# Run Metabase with Docker
docker run -d -p 3000:3000 --name metabase metabase/metabase
```

### Best Practices
1. **Use dbt models** - Query dbt models, not raw tables
2. **Collections** - Organize dashboards by team/domain
3. **Version Control** - Export dashboards as JSON and commit them
4. **Permissions** - Set up proper data permissions
5. **Caching** - Configure caching for better performance

### Exporting Dashboards
```bash
# Export dashboard as JSON (via Metabase API)
curl -X GET \
  -H "X-Metabase-Session: YOUR_SESSION_TOKEN" \
  http://localhost:3000/api/dashboard/1 > metabase/dashboards/sales_dashboard.json
```

## Lightdash

Lightdash is a dbt-native BI tool that reads directly from your dbt project.

### Setup
```bash
# Install Lightdash CLI
npm install -g @lightdash/cli

# Connect to your dbt project
lightdash dbt run
lightdash start-preview
```

### Benefits
- **dbt-native** - Uses your dbt metrics and dimensions
- **Version controlled** - Everything in YAML alongside dbt
- **Self-service** - Non-technical users can explore dbt models

## Choosing a BI Tool

| Tool | Best For | Pros | Cons |
|------|----------|------|------|
| **Metabase** | General purpose BI | Easy to use, great UI | Not dbt-native |
| **Lightdash** | dbt-first teams | dbt integration, version control | Newer tool |

## Resources

- [Metabase Documentation](https://www.metabase.com/docs/)
- [Lightdash Documentation](https://docs.lightdash.com/)
