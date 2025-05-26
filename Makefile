# File: Makefile
# Add these targets to existing file

.PHONY: secrets setup

# ---- Secret Management ----
secrets:
	@echo "🔑 Generating secret files from .env..."
	@mkdir -p secrets && chmod 700 secrets
	@grep -E '^POSTGRES_USER=' .env | cut -d= -f2- > secrets/db_user.txt
	@grep -E '^POSTGRES_PASSWORD=' .env | cut -d= -f2- > secrets/db_password.txt
	@grep -E '^REDIS_PASSWORD=' .env | cut -d= -f2- > secrets/redis_password.txt
	@chmod 600 secrets/*.txt
	@echo "✅ Secrets generated | Never commit these files!"

# ---- Modified Setup Target ----
setup: secrets validate
	@echo "🔐 Generating crypto material..."
	@mkdir -p nginx/ssl
	@openssl dhparam -out nginx/ssl/dhparam.pem 4096
	@echo "✅ Setup complete"