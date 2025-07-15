#!/bin/sh
python manage.py migrate
python manage.py collectstatic --noinput
celery -A core worker --loglevel=info &
gunicorn core.wsgi:application --bind 0.0.0.0:8000
exec "$@"