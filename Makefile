# File: Makefile
# Path: my-property/Makefile
# Purpose: Unified deployment automation with safety checks

.PHONY: validate setup up logs health migrate clean renew-certs

# ---- Environment Validation ----
validate:
	@echo "🔍 Validating environment..."
	@test -f .env || (echo "ERROR: Missing .env file"; exit 1)
	@test -f secrets/db_password.txt || (echo "ERROR: Missing DB secret"; exit 1)
	@test -f secrets/redis_password.txt || (echo "ERROR: Missing Redis secret"; exit 1)
	@echo "✅ Environment validation passed"

# ---- Core Workflow ----
setup: validate
	@echo "🔧 Initializing infrastructure..."
	@mkdir -p nginx/ssl postgres/data redis/data
	@echo "🔐 Generating crypto material..."
	@openssl dhparam -out nginx/ssl/dhparam.pem 4096
	@echo "📁 Setting permissions..."
	@sudo chown -R 101:101 nginx/ssl
	@sudo chmod 750 nginx/ssl
	@echo "✅ Setup complete | Run 'make up' to start services"

up:
	@docker compose up -d --build
	@echo "🛡️  Services started | Verify with 'make health'"

logs:
	@docker compose logs -f

health:
	@echo "🩺 Container Status:"
	@docker compose ps
	@echo "\n🌐 Application Health:"
	@curl -sk https://localhost/health

migrate:
	@docker compose exec django-app python manage.py migrate

clean:
	@docker compose down -v --rmi all
	@echo "🧹 Cleaned all containers and volumes"

renew-certs:
	@docker compose run --rm certbot renew
	@docker compose restart nginx-proxy
	@echo "🔄 Certificates renewed and NGINX reloaded"