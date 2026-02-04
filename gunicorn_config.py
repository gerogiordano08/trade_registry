# gunicorn_config.py optimizado para Free Tier (0.1 CPU, 512 MB RAM)

# 1. Concurrencia (Workers)
# Usar solo 1 worker es lo más seguro por la limitación de RAM.
workers = 1 

# 2. Tipo de Worker
# Gevent es ideal para tareas de I/O (esperar peticiones a yfinance)
# porque no bloquea el único worker mientras espera una respuesta.
worker_class = 'gevent' 

# 3. Gevent Worker Connections
# Define cuántas peticiones simultáneas puede manejar el único worker.
# 1000 es un valor estándar para Gevent.
worker_connections = 1000 

# 4. Enlace y Timeout
bind = '0.0.0.0:8000'
timeout = 90