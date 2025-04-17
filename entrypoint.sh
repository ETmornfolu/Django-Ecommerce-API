#!/bin/sh

set -e  # Exit on any error

echo "🚀 Running Django migrations..."
python manage.py migrate --noinput

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Entrypoint tasks complete. Starting server..."
exec "$@"



