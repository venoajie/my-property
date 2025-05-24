# Dockerfile
# syntax=docker/dockerfile:1

# Base Python image
FROM python:3.12-bookworm

# Environment configuration
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH="/app/apps:/app/config" \
    PORT=8000

# System dependencies
RUN apt-get update && \
    apt-get install -y libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# SSL certificate setup
COPY nginx/ssl/rootCA.crt /usr/local/share/ca-certificates/
RUN chmod 644 /usr/local/share/ca-certificates/rootCA.crt && \
    update-ca-certificates

# Application setup
WORKDIR /app

# Install Python dependencies
COPY requirements/ /app/requirements/
RUN pip install --no-cache-dir \
    -r requirements/base.txt \
    -r requirements/prod.txt \
    check  # Verify all dependencies

# Copy application code
COPY . .

# Collect static files
RUN python manage.py collectstatic --no-input

# Runtime configuration
EXPOSE $PORT
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl --fail "http://localhost:$PORT/health/" || exit 1