#!/bin/sh

echo "Waiting for PostgreSQL to start..."

while ! nc -z db 5432; do
  sleep 0.1
done

echo "PostgreSQL ready. Excecuting migrations..."
cron
python manage.py migrate --no-input
python manage.py collectstatic --no-input


python manage.py crontab add

exec "$@"