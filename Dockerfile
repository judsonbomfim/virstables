# Usar uma imagem base com Python
FROM python:3.12-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar requirements.txt e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código do projeto
COPY . .

# Expor a porta do Gunicorn (opcional, para documentação)
EXPOSE 8000

# Comando padrão será sobrescrito no docker-compose.yml
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]