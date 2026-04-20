#!/bin/sh
set -e

echo "Storage startup: creating database tables..."
python3 create_tables.py

echo "Storage startup: starting app..."
exec python3 app.py