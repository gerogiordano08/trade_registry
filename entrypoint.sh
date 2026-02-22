#!/bin/sh
touch /usr/src/app/.env
printenv | sed 's/^\([^=]*\)=\(.*\)$/export \1="\2"/' > /usr/src/app/.env
chown appuser:appuser /usr/src/app/.env

echo "Waiting for PostgreSQL to start..."

while ! nc -z db 5432; do
  sleep 0.1
done

service cron start
echo "PostgreSQL ready. Excecuting migrations..."
python manage.py migrate --no-input
python manage.py collectstatic --no-input


exec "$@"