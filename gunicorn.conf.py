# Gunicorn configuration file for LMS
# Run with: gunicorn -c gunicorn.conf.py lms_project.wsgi:application

# Server socket
bind = "127.0.0.1:8001"
backlog = 2048

# Worker processes
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers after this many requests, to prevent memory leaks
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "/var/log/gunicorn/lms-access.log"
errorlog = "/var/log/gunicorn/lms-error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "lms_gunicorn"

# Server mechanics
daemon = False
pidfile = "/var/run/gunicorn/lms.pid"
user = "www-data"
group = "www-data"
tmp_upload_dir = None

# SSL (if needed)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"

# Preload app for better performance
preload_app = True

# Environment variables
raw_env = [
    'DJANGO_SETTINGS_MODULE=lms_project.settings',
]

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Performance tuning
worker_tmp_dir = "/dev/shm"
