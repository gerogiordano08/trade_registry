# ETAPA 1: Builder (Imagen temporal para compilar)
FROM python:3.12-slim as builder

WORKDIR /usr/src/app

# Evita que Python genere archivos .pyc y permite ver logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalación de dependencias de sistema necesarias para compilar (Postgres, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* 

COPY requirements.txt .
RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir --prefix=/install -r requirements.txt


# ETAPA 2: Final (Imagen ligera de ejecución)
FROM python:3.12-slim

WORKDIR /usr/src/app

# Dependencias de ejecución para Postgres (más ligeras que las de compilación)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    netcat-openbsd \
    cron \
    && rm -rf /var/lib/apt/lists/*

# Copiamos solo las librerías instaladas desde el builder
COPY --from=builder /install /usr/local
COPY --from=builder /install /usr/bin
COPY . .

# Creamos la carpeta de datos y estáticos, y asignamos permisos
RUN mkdir -p /usr/src/app/data /usr/src/app/staticfiles && \
    adduser --disabled-password appuser && \
    chown -R appuser:appuser /usr/src/app && \
    chmod +x /usr/src/app/entrypoint.sh

USER appuser

EXPOSE 8000

# Usamos un entrypoint para manejar las migraciones al arrancar
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

CMD [ "gunicorn", "--config", "gunicorn_config.py", "the_trade_registry.wsgi:application" ]