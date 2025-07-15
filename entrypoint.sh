#!/bin/sh
# Instalar dependências apenas em desenvolvimento (opcional)
if [ "$DJANGO_ENV" = "development" ]; then
    echo "Ambiente de desenvolvimento: instalando dependências..."
    pip install --user --no-cache-dir -r requirements.txt
fi

# Aguardar o PostgreSQL
until nc -z db 5432; do
    echo "Aguardando PostgreSQL..."
    sleep 2
done

# Aguardar o Redis
until nc -z redis 6379; do
    echo "Aguardando Redis..."
    sleep 2
done

# Executar migrações e coletar arquivos estáticos
python manage.py migrate
python manage.py collectstatic --noinput

# Iniciar o Gunicorn
exec gunicorn core.wsgi:application --bind 0.0.0.0:8000