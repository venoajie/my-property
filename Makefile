# File: Makefile
# Path: my-property/Makefile
# Purpose: Safe deployment automation with dependency checks

.PHONY: validate secrets setup up logs health migrate clean renew-certs clean-certs

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
	@(grep -E '^POSTGRES_USER=' .env || echo "POSTGRES_USER=default_user") | cut -d= -f2- > secrets/db_user.txt
	@(grep -E '^POSTGRES_PASSWORD=' .env || echo "POSTGRES_PASSWORD=$$(openssl rand -hex 32)") | cut -d= -f2- > secrets/db_password.txt
	@(grep -E '^REDIS_PASSWORD=' .env || echo "REDIS_PASSWORD=$$(openssl rand -hex 32)") | cut -d= -f2- > secrets/redis_password.txt
	@chmod 600 secrets/*.txt
	@echo "✅ Secrets generated | Never commit these files!"

# ---- Core Workflow ----
setup: secrets validate
	@echo "🔐 Generating crypto material..."
	@mkdir -p nginx/ssl && chmod 700 nginx/ssl
	@if [ ! -f nginx/ssl/rootCA.crt ]; then \
		echo "🛡️ Generating development root CA..."; \
		openssl req -x509 -nodes -newkey rsa:2048 \
			-keyout nginx/ssl/rootCA.key \
			-out nginx/ssl/rootCA.crt \
			-days 365 \
			-subj '/CN=TempCA/O=Development/C=US'; \
		chmod 600 nginx/ssl/*; \
	else \
		echo "🔑 Existing certificates found - skipping generation"; \
	fi
	@openssl dhparam -out nginx/ssl/dhparam.pem 4096
	@echo "✅ Setup complete | Run 'make up' to start services"
    # newkey rsa:2048, change to newkey rsa:4096 in production

certs:
	@echo "🔐 Generating server certificates..."
	@openssl req -newkey rsa:2048 -nodes -keyout nginx/ssl/privkey.pem \
		-subj "/CN=${DOMAIN}" \
		-out nginx/ssl/server.csr
	@openssl x509 -req -in nginx/ssl/server.csr \
		-CA nginx/ssl/rootCA.crt \
		-CAkey nginx/ssl/rootCA.key \
		-CAcreateserial \
		-out nginx/ssl/fullchain.pem \
		-days 365
	@rm nginx/ssl/server.csr
	@echo "✅ Server certificates generated"

# ---- Certificate Cleanup ----
clean-certs:
	@echo "🧹 Removing SSL certificates..."
	@rm -f nginx/ssl/rootCA.key nginx/ssl/rootCA.crt nginx/ssl/dhparam.pem
	@echo "⚠️  Removed all crypto material!"

#Production Certificates:
# Replace self-signed certs with Let's Encrypt
#sudo certbot certonly --nginx -d yourdomain.com
# While 2048-bit is sufficient for development, always use 4096-bit in production:
# Production override
#DH_SIZE=4096 make setup