# ========================================== #
# FILE: Dockerfile                           #
# PATH: my-property/Dockerfile               #
# PURPOSE: Secure Django Production Build    #
# ========================================== #

# -------------------------
# Global Build Parameters
# -------------------------

ARG BUILD_UID=1001
ARG SECRET_KEY="dummy-secret-for-build"
ARG POSTGRES_PASSWORD="dummy-db-password"
ARG POSTGRES_DB="dummy-db"
ARG POSTGRES_USER="dummy-user"


# Required for build stage
ARG BUILD_UID

# ===== BUILDER STAGE ===== #
FROM python:${PYTHON_VERSION} AS builder

# -------------------------
# System Hardening
# -------------------------

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev python3-dev gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    find / -xdev -perm /6000 -type f -exec chmod a-s {} \; || true

    # -------------------------
# User & Environment Setup
# -------------------------
RUN useradd --uid ${BUILD_UID} --create-home --shell /bin/false appuser && \
    mkdir -p /app/staticfiles && \
    chown -R appuser:appuser /app
# -------------------------
# Dependency Management
# -------------------------
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app

COPY requirements/ .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r base.txt -r prod.txt

# -------------------------
# Static Asset Compilation
# -------------------------
COPY . .
USER appuser
RUN python manage.py collectstatic --noinput --settings=config.settings.build

# ===== RUNTIME STAGE ===== #
FROM python:${PYTHON_VERSION}

# Re-declare build arguments for this stage
ARG BUILD_UID=1001  # Default if not overridden


# -------------------------
# Runtime Security
# -------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    find / -xdev -perm /6000 -type f -exec chmod a-s {} \; || true

# -------------------------
# Certificate Management
# -------------------------
COPY --chown=appuser:appuser nginx/ssl/rootCA.crt /usr/local/share/ca-certificates/
RUN chmod 644 /usr/local/share/ca-certificates/rootCA.crt && \
    update-ca-certificates

    
# -------------------------
# User & Permissions
# -------------------------
RUN useradd --uid ${BUILD_UID} --create-home --shell /bin/false appuser && \
    mkdir -p /app/staticfiles && \
    chown -R appuser:appuser /app    
    
WORKDIR /app

COPY --from=builder --chown=appuser:appuser /opt/venv /opt/venv
COPY --from=builder --chown=appuser:appuser /app/staticfiles /app/staticfiles
COPY --from=builder --chown=appuser:appuser /app /app

ENV PATH="/opt/venv/bin:$PATH" \
    PORT=8000 \
    POSTGRES_HOST="postgres-db"

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

USER appuser
EXPOSE ${PORT}