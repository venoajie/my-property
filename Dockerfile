# ============================== #
# FILE: Dockerfile               #
# PATH: my-property/Dockerfile   #
# ============================== #



# ===== BUILDER STAGE ===== #
FROM python:3.12-slim-bookworm AS builder

# --------------------------
# Build Arguments & Security
# --------------------------
# WARNING: Pass these via CI/CD secrets in production
ARG SECRET_KEY="dummy-secret-for-build"
ARG POSTGRES_PASSWORD="dummy-db-password"

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
    # Django settings
    DJANGO_SETTINGS_MODULE="config.settings.production" \
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
    # Security: Remove unnecessary setuid/setgid binaries
    find / -xdev -perm /6000 -type f -exec chmod a-s {} \; || true

# --------------------------
# User & Directory Setup
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
# Dependency Installation
# --------------------------
COPY requirements/ .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    -r base.txt \
    -r prod.txt

# --------------------------
# Application Setup
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
# Environment Configuration
# --------------------------
ENV \
    # Security hardening
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive \
    # Application configuration
    PYTHONPATH="/app:/app/apps:/app/config" \
    DJANGO_SETTINGS_MODULE="config.settings.production" \
    PORT=8000

# --------------------------
# System Setup
# --------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq5 curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    # Security: Remove unnecessary setuid/setgid binaries
    find / -xdev -perm /6000 -type f -exec chmod a-s {} \; || true

# --------------------------
# User & Directory Setup
# --------------------------
RUN useradd --uid 1001 --create-home --shell /bin/false appuser && \
    mkdir -p /app/staticfiles /var/log/django && \
    chown -R appuser:appuser /app /var/log/django && \
    chmod 755 /app /var/log/django

# --------------------------
# SSL Configuration
# --------------------------
COPY nginx/ssl/rootCA.crt /usr/local/share/ca-certificates/
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
