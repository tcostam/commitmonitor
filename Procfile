web: gunicorn commitmonitor.wsgi --limit-request-line 8188 --log-file -
worker: celery worker --app=commitmonitor --loglevel=info
