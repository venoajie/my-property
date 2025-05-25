# Real Estate Platform Deployment Guide

## Prerequisites
- Docker 20.10+
- Docker Compose 2.20+
- OpenSSL (for certificate generation)
- Git 2.25+

## First-Time Setup

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/real-estate-platform.git
cd real-estate-platform

Initialize Project Structure
make setup  # Creates required directories and generates DH parameters

Environment Configuration
cp .env.example .env
nano .env  # Edit with your values

Minimum Required Variables:
# Database
POSTGRES_DB=real_estate
POSTGRES_USER=app_user
POSTGRES_PASSWORD=strong_password

# Django
SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
DEBUG=0
ALLOWED_HOSTS=130.61.246.120,localhost

# AWS (for media storage)
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_STORAGE_BUCKET_NAME=your-bucket

Generate SSL Certificates (Development)
make generate-ssl

Security Essentials
SSL Certificates (Production):
certbot certonly --standalone -d yourdomain.com

File Permissions:
chmod 600 nginx/ssl/*
chown -R 101:101 nginx/logs  # For Docker Nginx user

Firewall Rules:
sudo ufw allow 443/tcp
sudo ufw deny 80/tcp

Building & Running

# Start all services
make up

# View logs
make logs

# Check system health
make health

First-Time Deployment
Apply database migrations:

bash
docker compose exec web python manage.py migrate
Create superuser:

bash
docker compose exec web python manage.py createsuperuser
Verify services:

bash
curl https://130.61.246.120/health
Maintenance
Daily Operations
bash
# Backup database
make backup

# Renew certificates (production)
make renew-certs

# Update dependencies
make update
Troubleshooting
Issue	Solution
Docker permission denied	sudo usermod -aG docker $USER
Missing environment variables	make env && source .env
Nginx SSL errors	make generate-ssl
Database connection issues	make reset-db
Production Readiness Checklist
Replace self-signed certificates with Let's Encrypt

Implement monitoring (Prometheus/Grafana)

Set up daily database backups

Configure AWS S3 for media storage

Enable Cloudflare/CDN protection

folder structure:
.
├── my-property
│   ├── apps
│   │   ├── core
│   │   │   ├── __init__.py
│   │   │   ├── tests
│   │   │   │   ├── __init__.py
│   │   │   │   └── test_views.py
│   │   │   └── views.py
│   │   ├── __init__.py
│   │   ├── listings
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── __init__.py
│   │   │   ├── management
│   │   │   │   ├── commands
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── wait_for_db.py
│   │   │   │   └── __init__.py
│   │   │   ├── migrations
│   │   │   │   └── __init__.py
│   │   │   ├── models.py
│   │   │   ├── tests
│   │   │   │   ├── __init__.py
│   │   │   │   ├── test_models.py
│   │   │   │   └── test_views.py
│   │   │   ├── urls.py
│   │   │   └── views.py
│   │   └── users
│   │       ├── admin.py
│   │       ├── __init__.py
│   │       ├── models.py
│   │       ├── tests
│   │       │   ├── __init__.py
│   │       │   └── test_models.py
│   │       ├── urls.py
│   │       └── views.py
│   ├── config
│   │   ├── __init__.py
│   │   ├── settings
│   │   │   ├── base.py
│   │   │   ├── __init__.py
│   │   │   ├── local.py
│   │   │   └── production.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── manage.py
│   ├── monitoring
│   │   └── prometheus.yml
│   ├── nginx
│   │   ├── nginx.conf
│   │   └── ssl
│   │       ├── fullchain.pem
│   │       ├── privkey.pem
│   │       ├── rootCA.crt
│   │       ├── rootCA.key
│   │       ├── rootCA.srl
│   │       ├── server.crt
│   │       ├── server.csr
│   │       ├── server.ext
│   │       └── server.key
│   ├── README.md
│   ├── real_estate
│   │   └── __init__.py
│   ├── requirements
│   │   ├── base.txt
│   │   ├── dev.txt
│   │   ├── __init__.py
│   │   └── prod.txt
│   ├── ssl
│   └── staticfiles
└── real-estate
    ├── API_DOCS.md
    ├── compose
    │   ├── local.yml
    │   └── production.yml
    ├── config
    │   ├── gunicorn.conf.py
    │   └── pytest.ini
    ├── CONTRIBUTING.md
    ├── deployment
    │   ├── build.sh
    │   ├── deploy-prod.sh
    │   └── deploy-staging.sh
    ├── DEPLOYMENT.md
    ├── docker-compose.yml
    ├── docker-entrypoint.sh
    ├── Dockerfile
    ├── get-docker.sh
    ├── Makefile
    ├── manage.py
    ├── monitoring
    │   ├── grafana
    │   │   └── dashboards
    │   │       └── django.json
    │   ├── healthchecks
    │   │   └── healthz.sh
    │   └── prometheus
    │       └── prometheus.yml
    ├── pyproject.toml
    ├── README.md
    ├── requirements
    │   ├── base.txt
    │   ├── dev.txt
    │   └── prod.txt
    ├── scripts
    │   ├── backup.sh
    │   ├── migrate.sh
    │   └── setup_db.sh
    ├── src
    │   ├── apps
    │   │   ├── chat
    │   │   │   ├── __init__.py
    │   │   │   └── tests
    │   │   │       ├── __init__.py
    │   │   │       ├── stream_chat.py
    │   │   │       └── test_api.py
    │   │   ├── __init__.py
    │   │   ├── listings
    │   │   │   ├── apps.py
    │   │   │   ├── __init__.py
    │   │   │   ├── models.py
    │   │   │   └── tests
    │   │   │       ├── __init__.py
    │   │   │       ├── integration
    │   │   │       │   ├── __init__.py
    │   │   │       │   └── test_search.py
    │   │   │       ├── test_models.py
    │   │   │       └── test_views.py
    │   │   ├── manage
    │   │   │   ├── __init__.py
    │   │   │   └── tests
    │   │   │       └── __init__.py
    │   │   ├── offers
    │   │   │   ├── __init__.py
    │   │   │   └── tests
    │   │   │       ├── __init__.py
    │   │   │       └── test_workflows.py
    │   │   ├── requirements
    │   │   │   ├── base.txt
    │   │   │   ├── dev.txt
    │   │   │   ├── __init__.py
    │   │   │   ├── prod.txt
    │   │   │   ├── tests
    │   │   │   │   └── __init__.py
    │   │   │   └── test.txt
    │   │   ├── static
    │   │   │   ├── __init__.py
    │   │   │   └── tests
    │   │   │       └── __init__.py
    │   │   ├── templates
    │   │   │   ├── __init__.py
    │   │   │   └── tests
    │   │   │       └── __init__.py
    │   │   └── users
    │   │       ├── __init__.py
    │   │       └── tests
    │   │           ├── __init__.py
    │   │           ├── test_forms.py
    │   │           ├── test_models.py
    │   │           └── test_views.py
    │   ├── core
    │   │   ├── __init__.py
    │   │   ├── settings.py
    │   │   ├── settings_test.py
    │   │   ├── tests
    │   │   │   ├── __init__.py
    │   │   │   ├── test_settings.py
    │   │   │   └── test_utils.py
    │   │   └── views.py
    │   ├── __init__.py
    │   ├── manage.py
    │   ├── pytest.ini
    │   ├── real_estate
    │   │   ├── __init__.py
    │   │   ├── settings
    │   │   │   ├── base.py
    │   │   │   ├── development.py
    │   │   │   ├── __init__.py
    │   │   │   └── production.py
    │   │   ├── urls.py
    │   │   └── wsgi.py
    │   ├── requirements
    │   │   ├── base.txt
    │   │   ├── dev.txt
    │   │   └── prod.txt
    │   ├── setup.py
    │   └── tests
    │       ├── conftest.py
    │       ├── __init__.py
    │       ├── test_integration
    │       │   └── test_auth_flow.py
    │       └── test_selenium
    │           ├── conftest.py
    │           ├── __init__.py
    │           └── test_login.py
    ├── urls.py
    └── wait-for-db.sh