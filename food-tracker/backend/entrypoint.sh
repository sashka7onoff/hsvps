#!/bin/sh
set -e

# Wait for DB via Django connection (works for both Postgres and sqlite fallback)
until python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()
from django.db import connection
connection.ensure_connection()
print('Database connection successful')
" > /dev/null 2>&1; do
  echo "Food-tracker DB is not ready yet... waiting"
  sleep 2
done

echo "Food-tracker DB is ready!"

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

# If frontend was built during docker build, copydist to shared volume for nginx
if [ -d "/app/frontend_dist" ]; then
  echo "Publishing frontend dist to shared volume..."
  mkdir -p /usr/share/nginx/food-tracker
  cp -r /app/frontend_dist/* /usr/share/nginx/food-tracker/ 2>/dev/null || true
  echo "Frontend dist published"
fi

echo "Starting food-tracker backend..."
exec gunicorn myproject.wsgi:application --bind 0.0.0.0:8000 --workers 3
