#!/bin/sh
if [ "$DJANGO_ENV" = "development" ]; then
    echo "Ambiente de desenvolvimento: instalando dependências..."
    pip install --user --no-cache-dir -r requirements.txt
fi

until nc -z db 5432; do
    echo "Aguardando PostgreSQL..."
    sleep 2
done

until nc -z redis 6379; do
    echo "Aguardando Redis..."
    sleep 2
done

python manage.py migrate
python manage.py collectstatic --noinput
exec gunicorn core.wsgi:application --bind 0.0.0.0:8000 --timeout 120