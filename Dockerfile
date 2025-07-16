# Use uma imagem base oficial do Python
FROM python:3.11-slim

# Defina o diretório de trabalho
WORKDIR /app

# Instale dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instale as dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código da aplicação
COPY . .

# Colete arquivos estáticos
RUN python manage.py collectstatic --noinput

# Exponha a porta (se necessário, mas Gunicorn usará um socket)
EXPOSE 8000

# Comando para rodar o Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]