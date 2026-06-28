#!/bin/sh

set -e

# Пытаемся подключиться через Django
until python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'habittracker_pro.settings')
django.setup()
from django.db import connection
connection.ensure_connection()
print('Database connection successful')

" > /dev/null 2>&1; do
  echo "Database is not ready yet... waiting"
  sleep 2
done

echo "Database is ready!"

echo "Applying migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting server..."
gunicorn habittracker_pro.wsgi:application --bind 0.0.0.0:8000