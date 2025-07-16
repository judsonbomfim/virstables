#!/bin/sh

# Aguarda a conexão com o banco de dados (local)
until nc -z 127.0.0.1 5432; do
    echo "Aguardando PostgreSQL..."
    sleep 2
done

# Aguarda a conexão com o Redis (local)
until nc -z 127.0.0.1 6379; do
    echo "Aguardando Redis..."
    sleep 2
done


#!/bin/sh

python manage.py migrate
python manage.py collectstatic --noinput
nohup gunicorn core.wsgi:application --bind 0.0.0.0:8000 --log-level=info --timeout 120
# nohup celery -A core worker -B --loglevel=info &
