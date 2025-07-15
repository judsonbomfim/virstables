#!/bin/sh
# Instalar dependências apenas em desenvolvimento (opcional)
if [ "$DJANGO_ENV" = "development" ]; then
    echo "Ambiente de desenvolvimento: instalando dependências..."
    pip install --user --no-cache-dir -r requirements.txt
fi

# Aguardar o Redis
until nc -z redis 6379; do
    echo "Aguardando Redis..."
    sleep 2
done

# Iniciar o Celery
exec celery -A core worker --loglevel=info