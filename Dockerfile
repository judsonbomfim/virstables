# Usar uma imagem base com Python
FROM python:3.12-slim

# Definir variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código do projeto
COPY . .

# Criar diretórios de media ANTES de mudar usuário
RUN mkdir -p /app/media/banners \
    /app/media/cavalos \
    /app/media/leiloes \
    /app/media/fotos_cavalos \
    /app/media/leilao \
    /app/static

# Criar usuário não-root
RUN adduser --disabled-password --gecos '' appuser

# Dar permissões ao appuser
RUN chown -R appuser:appuser /app && \
    chmod -R 755 /app/media /app/static

# Mudar para usuário não-root
USER appuser

# Expor a porta do Gunicorn
EXPOSE 8000

# Comando padrão
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]