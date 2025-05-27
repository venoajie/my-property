# ========================================== #
# FILE: Dockerfile                           #
# PATH: my-property/Dockerfile               #
# PURPOSE: Secure Django Production Build    #
# ========================================== #

# Multi-Stage Dockerfile for Django Production Deployment
# Security Architecture:
# 1. Isolated builder environment
# 2. Minimal runtime image
# 3. Non-root execution
# 4. Build-time secret isolation
# 5. Certificate verification

# --------------------------
# Build Arguments (Override in CI/CD)
# --------------------------
# SECURITY: These defaults should be overridden in production
# HARDCODED VALUES:
ARG SECRET_KEY="dummy-secret-for-build"        # Rotate in production
ARG POSTGRES_PASSWORD="dummy-db-password"      # Use vault secrets
ARG POSTGRES_DB="dummy-db"                     # Set via environment
ARG POSTGRES_USER="dummy-user"                 # Set via environment

# ===== BUILDER STAGE ===== #
FROM python:3.12-slim-bookworm AS builder

# --------------------------
# Environment Configuration
# --------------------------
ENV \
    # Security hardening
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive \
    # Application paths
    PYTHONPATH="/app:/app/apps:/app/config" \
    # Build identification
    IN_DOCKER_BUILD=1

# --------------------------
# System Setup
# --------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev python3-dev gcc curl binutils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    # Remove risky permissions
    find / -xdev -perm /6000 -type f -exec chmod a-s {} \; || true

# --------------------------
# User & Filesystem Setup
# --------------------------
RUN useradd --uid 1001 --create-home --shell /bin/false appuser && \
    mkdir -p /app/staticfiles /var/log/django && \
    chown -R appuser:appuser /app /var/log/django

# --------------------------
# Python Environment
# --------------------------
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app

# --------------------------
# Dependency Installation
# --------------------------
COPY requirements/ .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    -r base.txt \
    -r prod.txt

# --------------------------
# Application Deployment
# --------------------------
COPY . .
RUN chown -R appuser:appuser /app

# --------------------------
# Asset Compilation
# --------------------------
USER appuser
RUN python manage.py check --settings=config.settings.build && \
    python manage.py collectstatic --no-input --clear --settings=config.settings.build

# ===== RUNTIME STAGE ===== #
FROM python:3.12-slim-bookworm

# --------------------------
# Runtime Environment
# --------------------------
ENV \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive \
    PORT=8000 \
    POSTGRES_HOST="postgres-db" \
    POSTGRES_PORT="5432"

# --------------------------
# System Configuration
# --------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq5 curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    find / -xdev -perm /6000 -type f -exec chmod a-s {} \; || true

# --------------------------
# User & Permissions
# --------------------------
RUN useradd --uid 1001 --create-home --shell /bin/false appuser && \
    mkdir -p /app/staticfiles /var/log/django && \
    chown -R appuser:appuser /app /var/log/django && \
    chmod 755 /app /var/log/django

# --------------------------
# Certificate Setup
# --------------------------
COPY --chown=appuser:appuser nginx/ssl/rootCA.crt /usr/local/share/ca-certificates/
RUN test -f /usr/local/share/ca-certificates/rootCA.crt || { \
    echo "FATAL: Missing root CA certificate in container"; exit 1; \
} && \
    chmod 644 /usr/local/share/ca-certificates/rootCA.crt && \
    update-ca-certificates

# --------------------------
# Application Deployment
# --------------------------
WORKDIR /app
COPY --from=builder --chown=appuser:appuser /opt/venv /opt/venv
COPY --from=builder --chown=appuser:appuser /app/ /app/
COPY --from=builder --chown=appuser:appuser /var/log/django /var/log/django
COPY --from=builder --chown=appuser:appuser /app/staticfiles /app/staticfiles

ENV PATH="/opt/venv/bin:$PATH"

# --------------------------
# Health & Runtime
# --------------------------
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

EXPOSE ${PORT}
USER appuser

# ===== SECURITY CHECKLIST ===== #
# 1. Rotate all dummy credentials
# 2. Replace self-signed certificates
# 3. Enable Docker content trust
# 4. Implement vulnerability scanning
# 5. Use secret management system