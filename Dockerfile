# Dockerfile
# Use lighter base image
FROM python:3.12-slim-bookworm

# Environment configuration
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH="/app/apps:/app/config" \
    PORT=8000

# System dependencies + curl for healthchecks
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# SSL certificate setup
COPY nginx/ssl/rootCA.crt /usr/local/share/ca-certificates/
RUN chmod 644 /usr/local/share/ca-certificates/rootCA.crt && \
    update-ca-certificates

# Application setup
WORKDIR /app

# Install dependencies first for caching
COPY ./requirements /app/requirements/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    -r requirements/base.txt \
    -r requirements/prod.txt

# Copy application
COPY . .

# Collect static during build
RUN mkdir -p /var/log/django && \
    touch /var/log/django/app.log && \
    chown -R www-data:www-data /var/log/django && \
    python manage.py collectstatic --no-input --clear

# Healthcheck with installed curl
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:$PORT/health/ || exit 1

EXPOSE $PORT