#!/bin/sh

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting server..."
gunicorn ecommerce.wsgi:application --bind 0.0.0.0:8000 --workers 1 --threads 2 --timeout 60

