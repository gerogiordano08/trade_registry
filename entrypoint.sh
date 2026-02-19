#!/bin/sh

echo "Esperando a que PostgreSQL arranque..."

while ! nc -z db 5432; do
  sleep 0.1
done

echo "PostgreSQL listo. Ejecutando migraciones..."
cron
python manage.py migrate --no-input
python manage.py collectstatic --no-input


python manage.py crontab add

exec "$@"