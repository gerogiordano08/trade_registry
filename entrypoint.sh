#!/bin/sh

# cron template configuration
envsubst '${CRON_PRICE_UPDATE_TIME} ${CRON_NEWS_SCRAPE_TIME} ${CRON_NEWS_CLEAN_TIME} ${CRON_NEWS_SCRAPE_PRICE_UPDATE_LOG_TRUNCATE_TIME} ${CRON_NEWS_CLEAN_LOG_TRUNCATE_TIME}' < /usr/src/app/crontab.template > /usr/src/app/crontab.txt
cp /usr/src/app/crontab.txt /etc/cron.d/trade-cron
chmod 0644 /etc/cron.d/trade-cron
# Ensure the file ends with a newline (cron requirement)
echo "" >> /etc/cron.d/trade-cron

# config envs for cron
touch /usr/src/app/.env
printenv | sed 's/^\([^=]*\)=\(.*\)$/export \1="\2"/' > /usr/src/app/.env
chown appuser:appuser /usr/src/app/.env

echo "Waiting for PostgreSQL to start..."

while ! nc -z db 5432; do
  sleep 0.1
done

service cron start
echo "PostgreSQL ready. Excecuting migrations..."
gosu appuser python manage.py migrate --no-input
gosu appuser python manage.py collectstatic --no-input


exec gosu appuser "$@"