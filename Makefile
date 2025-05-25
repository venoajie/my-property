.PHONY: setup up logs health backup renew-certs update

setup:
    @echo "Initializing project structure..."
    mkdir -p nginx/{ssl,logs}
    chmod 700 nginx/ssl
    openssl dhparam -out nginx/ssl/dhparam.pem 2048
    touch nginx/logs/{access,error}.log

up:
    docker compose up -d --build

logs:
    docker compose logs -f

health:
    docker compose ps

backup:
    docker compose exec db pg_dumpall -U ${POSTGRES_USER} > backup_$(date +%F).sql

renew-certs:
    certbot renew --nginx --non-interactive --post-hook "docker compose restart nginx"

update:
    docker compose build --no-cache
    docker compose down
    docker compose up -d

#Note: Replace IP addresses with your domain name when moving to production. 
#For OCI Free Tier, keep instance type as VM.Standard.E2.1.Micro and use Always Free eligible services.