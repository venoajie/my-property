# ==== Multi-Stage Production Dockerfile ====
# File: Dockerfile
# Purpose: Secure, minimal Django deployment image
# Security: Non-root user, build-time secrets, dependency cleanup

# ---- Builder Stage ----
# Purpose: Install dependencies, build static files
# Security: Contains build tools that are not in final image
FROM python:3.12-slim-bookworm AS builder


# Add build arguments with safe defaults
ARG SECRET_KEY="dummy-secret-for-build"
ARG POSTGRES_PASSWORD="dummy-db-password"
ARG POSTGRES_DB="dummy-db"
ARG POSTGRES_USER="dummy-user"
ARG POSTGRES_HOST="localhost"

# Set build-time environment variables
ENV \
    # Security & Python optimization
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # Application paths
    PYTHONPATH="/app:/app/apps:/app/config" \
    # Django settings
    DJANGO_SETTINGS_MODULE="config.settings.production" \
    # Build flags
    IN_DOCKER_BUILD=1 \
    # Database configuration
    POSTGRES_DB="${POSTGRES_DB}" \
    POSTGRES_USER="${POSTGRES_USER}" \
    POSTGRES_PASSWORD="${POSTGRES_PASSWORD}" \
    POSTGRES_HOST="${POSTGRES_HOST}" \
    POSTGRES_PORT="5432"
    
# Build arguments (Only used during build, not in final image)
# HARDCODED WARNING: Pass these via CI/CD pipeline in production
ARG SECRET_KEY
ARG POSTGRES_PASSWORD

# Build-time environment configuration
ENV \
    # Security & Python optimization
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # Application paths
    PYTHONPATH="/app:/app/apps:/app/config" \
    # Django settings
    DJANGO_SETTINGS_MODULE="config.settings.production" \
    # Build flags
    IN_DOCKER_BUILD=1 \
    # Secrets (Only for collectstatic)
    SECRET_KEY="${SECRET_KEY}" \
    POSTGRES_PASSWORD="${POSTGRES_PASSWORD}"

# System dependencies (Removed in final image)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev python3-dev gcc curl binutils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# User & Directory Setup (Matches runtime stage UID)
RUN useradd --uid 1001 --create-home --shell /bin/false appuser && \
    mkdir -p /app/staticfiles /var/log/django && \
    chown -R appuser:appuser /app /var/log/django && \
    chmod 755 /app /var/log/django

# Virtual Environment (Isolated Python setup)
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app

# Dependency Installation (Layer caching optimization)
COPY requirements/ .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r base.txt -r prod.txt

# Application Code & Static Files
COPY . .
RUN chown -R appuser:appuser /app


# Static File Collection (Run as non-root)
USER appuser
RUN python manage.py collectstatic --no-input --clear --settings=config.settings.build

# ---- Runtime Stage ----
# Purpose: Minimal production image
# Security: No build tools, non-root user
FROM python:3.12-slim-bookworm

# Environment Configuration
ENV \
    # Security & Python optimization
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # Application paths
    PYTHONPATH="/app:/app/apps:/app/config" \
    # Django settings
    DJANGO_SETTINGS_MODULE="config.settings.production" \
    # Network
    PORT=8000 \
    # User
    USER=appuser

# Runtime Dependencies (Only what's needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# User & Directory Setup (Must match builder UID)
RUN useradd --uid 1001 --create-home --shell /bin/false appuser && \
    mkdir -p /app/staticfiles /var/log/django && \
    chown -R appuser:appuser /app /var/log/django && \
    chmod 755 /app /var/log/django

# SSL Certificates (Update CA trust store)
COPY nginx/ssl/rootCA.crt /usr/local/share/ca-certificates/
RUN chmod 644 /usr/local/share/ca-certificates/rootCA.crt && \
    update-ca-certificates

# Application Setup
WORKDIR /app
# Update the COPY command in Dockerfile
COPY --from=builder --chown=appuser:appuser \
    /opt/venv /opt/venv

COPY --from=builder --chown=appuser:appuser \
    /app/ /app/

COPY --from=builder --chown=appuser:appuser \
    /var/log/django /var/log/django

COPY --from=builder --chown=appuser:appuser \
    /app/staticfiles /app/staticfiles

    # Virtual Environment
ENV PATH="/opt/venv/bin:$PATH"

# Healthcheck & Ports
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1
EXPOSE ${PORT}

# Runtime Execution (Non-root user)
USER appuser

# ==== Security Best Practices ====
# 1. Build args should be passed via CI/CD secrets
# 2. Rotate rootCA.crt quarterly
# 3. Use Docker secrets for POSTGRES_PASSWORD in production
# 4. Regular vulnerability scanning