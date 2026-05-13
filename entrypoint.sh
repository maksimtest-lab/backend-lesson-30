#!/bin/sh
set -e

echo "📌 Waiting for PostgreSQL..."

until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  echo "⏳ PostgreSQL is starting..."
  sleep 1
done

echo "✅ PostgreSQL is available"

echo "📌 Applying migrations..."
python manage.py migrate --noinput

echo "📌 Collecting static files..."
python manage.py collectstatic --noinput

echo "🚀 Starting Gunicorn..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8111 \
    --workers 4 \
    --timeout 120
