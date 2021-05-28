#!/bin/bash

set -e

echo "Waiting for postgres..."

while ! nc -z postgres 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

uvicorn src.main:app --reload --workers 1 --host 0.0.0.0 --port 8001
