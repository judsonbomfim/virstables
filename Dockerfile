# Estágio de build
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Estágio final
FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y netcat-openbsd curl net-tools && rm -rf /var/lib/apt/lists/*
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
RUN chmod +x entrypoint.sh entrypoint-celery.sh
EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]