#!/bin/bash
# Starts the FastAPI backend on http://127.0.0.1:8000
# Seeds the database on first run only (skips if leave_management.db already exists).
cd "$(dirname "$0")/backend" || exit 1

if [ ! -f "leave_management.db" ]; then
    echo "No database found — seeding demo data..."
    python3 seed_data.py
fi

echo "Starting backend at http://127.0.0.1:8000  (docs at /docs)"
uvicorn main:app --reload --port 8000
