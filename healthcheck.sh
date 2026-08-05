#!/bin/bash

echo "=== Healthcheck: Travel Journal Application ==="

# Check Backend API Health
BACKEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/)
if [ "$BACKEND_STATUS" -eq 200 ]; then
    echo "[OK] Backend API is running on http://localhost:8000"
else
    echo "[FAIL] Backend API responded with status: $BACKEND_STATUS"
fi

# Check Frontend Nginx Health
FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:80/)
if [ "$FRONTEND_STATUS" -eq 200 ]; then
    echo "[OK] Frontend App is running on http://localhost:80"
else
    echo "[FAIL] Frontend App responded with status: $FRONTEND_STATUS"
fi
