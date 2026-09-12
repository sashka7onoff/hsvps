#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."
python -c "
import psycopg2, time, os
while True:
    try:
        psycopg2.connect(
            host=os.environ.get('DB_HOST', 'db'),
            port=os.environ.get('DB_PORT', '5432'),
            user=os.environ.get('DB_USER', 'postgres'),
            password=os.environ.get('DB_PASSWORD', ''),
            dbname=os.environ.get('DB_NAME', 'get_blank'),
        )
        break
    except psycopg2.OperationalError:
        time.sleep(1)
"
echo "PostgreSQL is ready."

python manage.py migrate --noinput

exec gunicorn getblank.wsgi:application --bind 0.0.0.0:8000 --workers 4
