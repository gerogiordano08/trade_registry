FROM python:3.12-slim as builder

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* 

COPY requirements.txt .
RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir --prefix=/install -r requirements.txt


FROM python:3.12-slim

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local

COPY . .

COPY crontab.txt /etc/cron.d/trade-cron

RUN mkdir -p /usr/src/app/data /usr/src/app/staticfiles && \
    adduser --disabled-password appuser && \
    chown -R appuser:appuser /usr/src/app && \
    chmod +x /usr/src/app/entrypoint.sh && \
    chmod 0644 /etc/cron.d/trade-cron && \
    crontab -u appuser /etc/cron.d/trade-cron && \
    chmod u+s /usr/sbin/cron && \
    touch /var/log/cron.log && \
    chown appuser:appuser /var/log/cron.log

RUN usermod -s /bin/bash appuser

USER appuser

EXPOSE 8000

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

CMD [ "gunicorn", "--config", "gunicorn_config.py", "the_trade_registry.wsgi:application" ]