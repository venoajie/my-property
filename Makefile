# File: Makefile
# Path: my-property/Makefile
# Purpose: Safe deployment automation with dependency checks

.PHONY: validate init up logs health migrate clean

# ---- Environment Validation ----
validate:
	@test -f .env || (echo "ERROR: Missing .env file"; exit 1)
	@test -f secrets/db_password.txt || (echo "ERROR: Missing DB secret"; exit 1)
	@test -f secrets/redis_password.txt || (echo "ERROR: Missing Redis secret"; exit 1)

# ---- Core Workflow ----
init: validate
	@echo "🔐 Generating crypto material..."
	@mkdir -p nginx/ssl
	@openssl dhparam -out nginx/ssl/dhparam.pem 4096
	@echo "✅ Initialization complete"

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