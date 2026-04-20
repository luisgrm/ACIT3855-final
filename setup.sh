#!/bin/bash

echo "Verifying directories exist..."

# Ensure directories exist
mkdir -p logs data/processing data/health

echo "Setting directory permissions..."

# Allow containers to write logs and stats file
sudo chmod -R 777 logs data config nginx
sudo chmod 777 data/processing data/health

echo "Permissions configured successfully."

echo "Setup complete!"

echo "Starting containers and creating 'receiver' replicas..."
docker compose up --build -d --scale receiver=3

echo "All done!"