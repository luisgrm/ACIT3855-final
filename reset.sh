#!/bin/bash

echo "Dropping MySQL tables..."
docker compose exec storage python3 drop_tables.py

echo ""
echo "Removing processing stats file..."
rm -f data/processing/data.json

echo ""
echo "Stopping containers and removing volumes..."
docker compose down -v

echo ""
echo "Reset complete. You can now start fresh with:"
echo "docker compose up --build -d"
