# ========================================== #
# FILE: Dockerfile                           #
# PATH: my-property/Dockerfile               #
# PURPOSE: Secure Django Production Build    #
# ========================================== #

#Multi-Stage Dockerfile for Django Production Deployment

#Security Architecture:
#1. Builder Stage: Isolated build environment
#2. Runtime Stage: Minimal production image
#3. Non-root user execution
#4. Build-time secret isolation
#5. SSL certificate verification

#Critical Hardcoded Values (Update in Production):
#- POSTGRES_DB="dummy-db"          → Set via CI/CD secrets
#- POSTGRES_USER="dummy-user"       → Set via CI/CD secrets
#- UID 1001                         → Match host user ID

# ===== BUILDER STAGE ===== #
FROM python:3.12-slim-bookworm AS builder

# --------------------------
# Build Configuration
# --------------------------
# Security: Build arguments with safe defaults
ARG SECRET_KEY="dummy-secret-for-build"       # Must be overridden in CI/CD
ARG POSTGRES_PASSWORD="dummy-db-password"     # Must be overridden in CI/CD
ARG POSTGRES_DB="dummy-db"                    # Must be overridden in CI/CD
ARG POSTGRES_USER="dummy-user"                # Must be overridden in CI/CD

# --------------------------
# Environment Setup
# --------------------------
ENV \
    # Security & Optimization
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive \
    # Application Paths
    PYTHONPATH="/app:/app/apps:/app/config" \
    # Django Configuration
    DJANGO_SETTINGS_MODULE="config.settings.production" \
    # Database Credentials
    POSTGRES_DB="${POSTGRES_DB}" \
    POSTGRES_USER="${POSTGRES_USER}" \
    POSTGRES_PASSWORD="${POSTGRES_PASSWORD}" \
    # Build Identification
    IN_DOCKER_BUILD=1

# --------------------------
# System Preparation
# --------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev python3-dev gcc curl binutils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    # Security: Remove risky permissions
    find / -xdev -perm /6000 -type f -exec chmod a-s {} \; || true

# --------------------------
# User & Filesystem Setup
# --------------------------
RUN useradd --uid 1001 --create-home --shell /bin/false appuser && \
    mkdir -p /app/staticfiles /var/log/django && \
    chown -R appuser:appuser /app /var/log/django && \
    chmod 755 /app /var/log/django

# --------------------------
# Python Environment
# --------------------------
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app

# --------------------------
# Dependency Management
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
# Static Assets Collection
# --------------------------
USER appuser
RUN python manage.py check --settings=config.settings.build && \
    python manage.py collectstatic --no-input --clear --settings=config.settings.build

# ===== RUNTIME STAGE ===== #
FROM python:3.12-slim-bookworm

# --------------------------
# Runtime Configuration
# --------------------------
ENV \
    # Security & Optimization
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive \
    # Application Settings
    PYTHONPATH="/app:/app/apps:/app/config" \
    DJANGO_SETTINGS_MODULE="config.settings.production" \
    # Network Configuration
    PORT=8000 \
    # Database Connection
    POSTGRES_HOST="postgres-db" \
    POSTGRES_PORT="5432"

# --------------------------
# System Preparation
# --------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq5 curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    # Security: Remove risky permissions
    find / -xdev -perm /6000 -type f -exec chmod a-s {} \; || true

# --------------------------
# User & Filesystem Setup
# --------------------------
RUN useradd --uid 1001 --create-home --shell /bin/false appuser && \
    mkdir -p /app/staticfiles /var/log/django && \
    chown -R appuser:appuser /app /var/log/django && \
    chmod 755 /app /var/log/django

# --------------------------
# SSL Configuration
# --------------------------
# Security: Certificate verification
RUN test -f nginx/ssl/rootCA.crt || { \
    echo "FATAL: Missing root CA certificate"; \
    echo "Generate with: openssl req -x509 -nodes -newkey rsa:2048 -keyout nginx/ssl/rootCA.key -out nginx/ssl/rootCA.crt -days 365 -subj '/CN=TempCA/O=Development/C=US'"; \
    exit 1; \
}

COPY --chown=appuser:appuser nginx/ssl/rootCA.crt /usr/local/share/ca-certificates/
RUN chmod 644 /usr/local/share/ca-certificates/rootCA.crt && \
    update-ca-certificates

# --------------------------
# Application Deployment
# --------------------------
WORKDIR /app

# Copy Python virtual environment
COPY --from=builder --chown=appuser:appuser /opt/venv /opt/venv

# Copy application code
COPY --from=builder --chown=appuser:appuser /app/ /app/

# Copy log directory structure
COPY --from=builder --chown=appuser:appuser /var/log/django /var/log/django

# Copy collected static files
COPY --from=builder --chown=appuser:appuser /app/staticfiles /app/staticfiles

# Virtual Environment    
ENV PATH="/opt/venv/bin:$PATH"

# --------------------------
# Health Monitoring
# --------------------------
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

EXPOSE ${PORT}

# --------------------------
# Runtime Execution
# --------------------------
USER appuser

# ===== SECURITY CHECKLIST ===== #
#1. Rotate all dummy credentials in production
#2. Replace self-signed SSL certificate
#3. Enable Docker content trust
#. Regular vulnerability scanning:
#   - docker scan <image>
#   - trivy image <image>
#5. Implement CI/CD secret management
