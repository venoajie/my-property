# File: Makefile
# Purpose: Infrastructure automation for secure real estate platform deployment
# Security Level: Production (with development safeguards)

# --------------------------
# 1. Environment Configuration
# --------------------------
DOMAIN ?= localhost# Override with production domain
COMPOSE := docker compose# Docker Compose command abstraction
DB_SERVICE := db# Database service name
WEB_SERVICE := web# Django service name
NGINX_SERVICE := nginx# Web server service name
SSL_DIR := nginx/ssl# Certificate storage
LOG_DIR := nginx/logs# Access/error logs
DB_DIR := postgres/data# Database volume

.PHONY: setup up logs health backup renew-certs update migrate security-check

# --------------------------
# 2. Core Workflow Targets
# --------------------------

## Initialize project structure with secure permissions
setup:@echo "🔧 Building secure directory structure..."
	sudo mkdir -p "${SSL_DIR}" "${LOG_DIR}" "${DB_DIR}"
	sudo chown -R $$(whoami):$$(whoami) "${SSL_DIR}" "${LOG_DIR}" "${DB_DIR}"
	sudo chmod 755 "${SSL_DIR}" "${LOG_DIR}" "${DB_DIR}"  # Base permissions

	@echo "🔐 Applying cryptographic protections..."
	sudo openssl dhparam -out "${SSL_DIR}/dhparam.pem" 2048

	@echo "📁 Configuring service-specific permissions..."
	# Prepare logs for NGINX (UID 101)
	sudo chown -R 101:101 "${LOG_DIR}"
	sudo chmod 755 "${LOG_DIR}"
	sudo chcon -Rt httpd_log_t "${LOG_DIR}"  # SELinux

	# Secure SSL directory
	sudo chmod 700 "${SSL_DIR}"
	sudo chown -R root:root "${SSL_DIR}"

	# Configure DB directory for PostgreSQL (UID 999)
	sudo chown -R 999:999 "${DB_DIR}"
	sudo chmod 750 "${DB_DIR}"

## Start all services in production mode
up:
	${COMPOSE} up -d --build
	@echo "✅ Services started. Verify with 'make health'"

## Follow container logs in real-time
logs:
	${COMPOSE} logs -f

## Check system health status
health:
	@echo "🩺 Container status:"
	${COMPOSE} ps
	@echo "\n🌐 Testing API endpoint..."
	curl -k "https://${DOMAIN}/api/health/"

# --------------------------
# 3. Database Management
# --------------------------

## Create database backup snapshot
backup:
	@echo "💾 Backing up database..."
	${COMPOSE} exec ${DB_SERVICE} pg_dump -U $${POSTGRES_USER} $${POSTGRES_DB} > backup_$(date +%F).sql
	@echo "🔒 Backup stored as backup_$(date +%F).sql"

## Apply Django database migrations
migrate:
	${COMPOSE} exec ${WEB_SERVICE} python manage.py migrate
	@echo "🗄️ Database schema updated"

# --------------------------
# 4. Security Maintenance
# --------------------------

## Renew SSL certificates (Production Only)
renew-certs:
	certbot renew --nginx --non-interactive --post-hook "${COMPOSE} restart ${NGINX_SERVICE}"
	@echo "🔄 Certificates renewed. NGINX restarted."

## Full system rebuild with security updates
update:
	@echo "🛠️  Rebuilding containers..."
	${COMPOSE} build --no-cache
	${COMPOSE} down
	${COMPOSE} up -d
	@echo "⚠️ Warning: Rebuilding containers may cause temporary service interruption"

# --------------------------
# 5. Deployment Notes
# --------------------------
# Production Checklist:
# 1. Replace ${DOMAIN} with actual production domain
# 2. Set DEBUG=0 in .env file
# 3. Rotate all secrets (POSTGRES_PASSWORD, SECRET_KEY, etc)
#
# OCI Free Tier Requirements:
# - Instance Type: VM.Standard.E2.1.Micro
# - Use Always Free eligible services
# - Monitor resource usage thresholds