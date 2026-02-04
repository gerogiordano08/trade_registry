#!/bin/sh

echo "Esperando a que PostgreSQL arranque..."

# Intentar conectarse al puerto 5432 de la DB
while ! nc -z db 5432; do
  sleep 0.1
done

echo "PostgreSQL listo. Ejecutando migraciones..."

python manage.py migrate --no-input
python manage.py collectstatic --no-input

exec "$@"