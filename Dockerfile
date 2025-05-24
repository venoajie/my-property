# syntax=docker/dockerfile:1
FROM python:3.12-bookworm

# Environment optimization
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/apps:/app/config \
    PORT=8000
# System dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Application setup
WORKDIR /app
COPY requirements /app/requirements

# Dependency installation
RUN pip install --no-cache-dir \
    -r requirements/base.txt \
    -r requirements/prod.txt

# Application code
COPY . .
COPY .env* /app/

# Runtime configuration
EXPOSE $PORT
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:$PORT/health/ || exit 1

# Development note: For production, consider:
# - Multi-stage builds
# - Separate user account
# - gunicorn startup command