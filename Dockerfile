# ----- Base Image -----
FROM python:3.12-slim-bookworm

# ----- Environment Configuration -----
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH="/app:/app/apps:/app/config" \
    PORT=8000 \
    USER=appuser

# ----- System Setup -----
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev \
    curl \
    binutils  \
    python3-dev \
    gcc && \
    rm -rf /var/lib/apt/lists/*

# ----- User and Directory Setup -----
RUN useradd --uid 1001 --create-home --shell /bin/false appuser && \
    mkdir -p /app/staticfiles /var/log/django && \
    chown -R appuser:appuser /app/staticfiles /var/log/django && \
    chmod 755 /app/staticfiles /var/log/django

# ----- Certificate Authority Setup -----
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

USER ${USER}

# ----- Health Verification -----
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

EXPOSE ${PORT}