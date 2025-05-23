FROM python:3.12-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy all requirements files
COPY requirements /app/requirements

# Install base and production requirements
RUN pip install --no-cache-dir \
    -r requirements/base.txt \
    -r requirements/prod.txt

COPY . .

COPY .env /app/

EXPOSE 8000