# ---- Builder Stage ----
FROM python:3.12-slim-bookworm as builder


# Add build arguments for critical secrets
ARG SECRET_KEY
ARG POSTGRES_PASSWORD

# Set build-time environment variables
ENV SECRET_KEY=$SECRET_KEY \
    POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH="/app:/app/apps:/app/config" \
    DJANGO_SETTINGS_MODULE=config.settings.production

# Build-specific environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH="/app:/app/apps:/app/config" \
    DJANGO_SETTINGS_MODULE=config.settings.production

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev \
    python3-dev \
    gcc \
    curl \
    binutils && \
    rm -rf /var/lib/apt/lists/*

# Create user and directories first
RUN useradd --uid 1001 --create-home --shell /bin/false appuser && \
    mkdir -p /var/log/django && \
    chown -R appuser:appuser /var/log/django && \
    chmod 755 /var/log/django

WORKDIR /app

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
COPY requirements/ .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r base.txt -r prod.txt

# Copy application code
COPY . .

# Set ownership before collectstatic
RUN chown -R appuser:appuser /app

# Run collectstatic as appuser
USER appuser
RUN python manage.py collectstatic --no-input --clear

# ---- Runtime Stage ----
FROM python:3.12-slim-bookworm as runtime

# Unset build-time secrets
ENV SECRET_KEY="" \
    POSTGRES_PASSWORD=""
    
# Runtime environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH="/app:/app/apps:/app/config" \
    PORT=8000 \
    USER=appuser \
    DJANGO_SETTINGS_MODULE=config.settings.production

# Install runtime dependencies (no build tools)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq5 \
    curl && \
    rm -rf /var/lib/apt/lists/*

# User and directory setup
RUN useradd --uid 1001 --create-home --shell /bin/false appuser && \
    mkdir -p /app/staticfiles /var/log/django && \
    chown -R appuser:appuser /app/staticfiles /var/log/django && \
    chmod 755 /app/staticfiles /var/log/django

# Copy certificates
COPY nginx/ssl/rootCA.crt /usr/local/share/ca-certificates/
RUN chmod 644 /usr/local/share/ca-certificates/rootCA.crt && \
    update-ca-certificates

WORKDIR /app

# Copy from builder stage
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
COPY --from=builder /var/log/django /var/log/django

# Set virtual environment path
ENV PATH="/opt/venv/bin:$PATH"

# Final permissions and user
RUN chown -R appuser:appuser /app
USER appuser

# Healthcheck and port
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1
EXPOSE ${PORT}