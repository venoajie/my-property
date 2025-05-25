# Dockerfile

# ----- Base Image -----
FROM python:3.12-slim-bookworm

# ----- Environment Configuration -----
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH="/app/apps:/app/config" \
    PORT=8000 \
    USER=appuser

# ----- System Setup -----
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev \
    curl \
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev && \
    rm -rf /var/lib/apt/lists/*

# ----- Certificate Authority Setup -----
# HARDCODED: Replace with organization CA in production
COPY nginx/ssl/rootCA.crt /usr/local/share/ca-certificates/
RUN chmod 644 /usr/local/share/ca-certificates/rootCA.crt && \
    update-ca-certificates

# ----- Application Setup -----
WORKDIR /app

# ----- Dependency Management -----
COPY requirements/ .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    -r base.txt \
    -r prod.txt

# ----- Application Code -----
COPY . .

# ----- Runtime Configuration -----
RUN useradd --uid 1001 --create-home --shell /bin/false appuser && \
    mkdir -p /var/log/django && \
    chown -R appuser:appuser /var/log/django && \
    chmod 755 /var/log/django

USER ${USER}

# ----- Build Tasks -----
#RUN python manage.py collectstatic --no-input --clear # prevent 50 characters secret key problem

# ----- Health Verification -----
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

EXPOSE ${PORT}