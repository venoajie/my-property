# File: Makefile
# Add these targets to existing file

# File: Makefile
# Path: my-property/Makefile
# Purpose: Safe deployment automation with dependency checks

.PHONY: validate secrets setup up logs health migrate clean renew-certs

# ---- Environment Validation ----
validate:
	@echo "🔍 Validating environment..."
	@test -f .env || (echo "ERROR: Missing .env file"; exit 1)
	@test -f secrets/db_user.txt || (echo "ERROR: Missing DB user secret"; exit 1)
	@test -f secrets/db_password.txt || (echo "ERROR: Missing DB password secret"; exit 1)
	@test -f secrets/redis_password.txt || (echo "ERROR: Missing Redis secret"; exit 1)
	@echo "✅ Environment validation passed"

# ---- Secret Management ----
secrets:
	@echo "🔑 Generating secret files from .env..."
	@mkdir -p secrets && chmod 700 secrets
	@grep -E '^POSTGRES_USER=' .env | cut -d= -f2- > secrets/db_user.txt
	@grep -E '^POSTGRES_PASSWORD=' .env | cut -d= -f2- > secrets/db_password.txt
	@grep -E '^REDIS_PASSWORD=' .env | cut -d= -f2- > secrets/redis_password.txt
	@chmod 600 secrets/*.txt
	@echo "✅ Secrets generated | Never commit these files!"

# ---- Core Workflow ----
setup: secrets validate
	@echo "🔐 Generating crypto material..."
	@mkdir -p nginx/ssl
	@openssl dhparam -out nginx/ssl/dhparam.pem 4096
	@echo "✅ Setup complete | Run 'make up' to start services"

up:
	@docker compose up -d --build
	@echo "🛡️  Services started | Verify with 'make health'"
    
    