#!/bin/sh
python manage.py migrate
python manage.py collectstatic --noinput
nohup celery -A core worker -B --loglevel=info
exec "$@"