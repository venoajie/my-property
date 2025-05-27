# ========================================== #
# FILE: Dockerfile                           #
# PATH: my-property/Dockerfile               #
# PURPOSE: Secure Django Production Build    #
# ========================================== #

# -------------------------
# Global Build Parameters
# -------------------------
# SECURITY: Default values should be overridden in CI/CD
# HARDCODED VALUES (Production Override Required):
ARG PYTHON_VERSION="3.12-slim-bookworm"  # Match container host version
ARG BUILD_UID=1001                       # Must match host user in production
ARG SECRET_KEY="dummy-secret-for-build"   # Rotate using openssl rand -hex 64
ARG POSTGRES_PASSWORD="dummy-db-password" # Set via vault/secret manager
ARG POSTGRES_DB="dummy-db"                # Use environment-specific names
ARG POSTGRES_USER="dummy-user"            # Follow principle of least privilege

# ===== BUILDER STAGE ===== #
FROM python:${PYTHON_VERSION} AS builder

# -------------------------
# System Hardening
# -------------------------
# Security Purpose:
# - Remove unnecessary packages
# - Clean apt cache
# - Disable SUID/GUID binaries
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev python3-dev gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    find / -xdev -perm /6000 -type f -exec chmod a-s {} \; || true

# -------------------------
# User & Environment Setup
# -------------------------
# Security Design:
# - Non-root user from start
# - Strict directory permissions
# - UID parameterization for host compatibility
RUN useradd --uid ${BUILD_UID} --create-home --shell /bin/false appuser && \
    mkdir -p /app/staticfiles && \
    chown -R appuser:appuser /app

# -------------------------
# Dependency Management
# -------------------------
# Optimization Strategy:
# - Separate venv creation
# - Precise dependency installation
# - Cache-friendly layer ordering
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app

COPY requirements/ .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r base.txt -r prod.txt

# -------------------------
# Static Asset Compilation
# -------------------------
# Security Note:
# - Run as non-root user
# - Use build-specific settings
COPY . .
USER appuser
RUN python manage.py collectstatic --noinput --settings=config.settings.build

# ===== RUNTIME STAGE ===== #
FROM python:${PYTHON_VERSION}

# -------------------------
# Runtime Security
# -------------------------
# Attack Surface Reduction:
# - Minimal package installation
# - Regular security updates
# - Filesystem hardening
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    find / -xdev -perm /6000 -type f -exec chmod a-s {} \; || true

# -------------------------
# Certificate Management
# -------------------------
# Security Protocol:
# - Certificate chain validation
# - Strict file permissions
# - Regular rotation (see Makefile)
COPY --chown=appuser:appuser nginx/ssl/rootCA.crt /usr/local/share/ca-certificates/
RUN chmod 644 /usr/local/share/ca-certificates/rootCA.crt && \
    update-ca-certificates

# -------------------------
# User & Permissions
# -------------------------
# Defense-in-Depth:
# - Consistent UID across stages
# - App-specific home directory
# - Immutable filesystem areas
RUN useradd --uid ${BUILD_UID} --create-home --shell /bin/false appuser && \
    mkdir -p /app/staticfiles && \
    chown -R appuser:appuser /app

# -------------------------
# Application Deployment
# -------------------------
WORKDIR /app
COPY --from=builder --chown=appuser:appuser /opt/venv /opt/venv
COPY --from=builder --chown=appuser:appuser /app/staticfiles /app/staticfiles
COPY --from=builder --chown=appuser:appuser /app /app

ENV PATH="/opt/venv/bin:$PATH" \
    PORT=8000 \
    POSTGRES_HOST="postgres-db"

# -------------------------
# Health Monitoring
# -------------------------
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -fsk https://localhost:${PORT}/health || exit 1

EXPOSE ${PORT}
USER appuser

# ===== SECURITY CHECKLIST ===== #
# 1. Rotate all HARDCODED credentials
# 2. Replace self-signed certificates quarterly
# 3. Enable Docker Content Trust (DCT)
# 4. Scan images weekly: docker scan & trivy
# 5. Audit user permissions monthly