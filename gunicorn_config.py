import os

workers = int(os.getenv('GUNICORN_WORKERS', '1'))

worker_class = os.getenv('GUNICORN_WORKER_CLASS', 'gevent')

# Defines simultaneous worker connections
worker_connections = int(os.getenv('GUNICORN_WORKER_CONNECTIONS', '1000'))

bind = os.getenv('GUNICORN_BIND', '0.0.0.0:8000')
timeout = int(os.getenv('GUNICORN_TIMEOUT', '90'))