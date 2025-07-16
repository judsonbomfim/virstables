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

# Executa migrações e coleta arquivos estáticos (apenas no serviço web)
if [ "$1" = "web" ]; then
    # python manage.py migrate --noinput
    python manage.py collectstatic --noinput
fi

# Inicia o Gunicorn ou Celery conforme o serviço
if [ "$1" = "web" ]; then
    exec gunicorn --bind 0.0.0.0:8000 core.wsgi:application --timeout 120
elif [ "$1" = "celery_worker" ]; then
    exec celery -A core worker -l info
else
    echo "Serviço não reconhecido. Use 'web' ou 'celery_worker'."
    exit 1
fi