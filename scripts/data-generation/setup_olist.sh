#!/bin/bash
# Quick setup script for Olist dataset in DuckDB
# Run this inside the analytics-lab Docker container

set -e

echo "🚀 Olist Dataset Setup for DuckDB"
echo "=================================="
echo ""

# Check if running in Docker
if [ ! -f /.dockerenv ]; then
    echo "⚠️  Warning: Not running in Docker container"
    echo "   Run: docker exec -it analytics-lab bash"
    echo "   Then: ./scripts/data-generation/setup_olist.sh"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Run the Python script
python3 /workspace/scripts/data-generation/load_olist_to_duckdb.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Query the database:"
echo "     duckdb /workspace/data/olist_ecommerce.duckdb"
echo ""
echo "  2. Or use Python:"
echo "     python3"
echo "     >>> import duckdb"
echo "     >>> conn = duckdb.connect('/workspace/data/olist_ecommerce.duckdb')"
echo "     >>> conn.execute('SELECT * FROM raw.orders LIMIT 5').df()"
echo ""
echo "  3. Or use Jupyter Lab:"
echo "     http://localhost:8888"
echo ""
