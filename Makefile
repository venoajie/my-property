# File: Makefile
# Path: my-property/Makefile
# Purpose: Secure Deployment Automation

.PHONY: validate secrets setup build clean

# ---- Environment Variables ----
DOCKER_IMAGE ?= realestate-app
BUILD_ARGS ?= --build-arg BUILD_UID=$(shell id -u) \
              --build-arg SECRET_KEY=$(shell cat secrets/db_password.txt) \
              --build-arg POSTGRES_PASSWORD=$(shell cat secrets/db_password.txt)

# ---- Core Workflow ----
all: validate setup build

validate:
    @echo "🔍 Validating environment..."
    @test -f .env || (echo "ERROR: Missing .env file"; exit 1)
    @test -d nginx/ssl || (echo "ERROR: Missing SSL directory"; exit 1)

secrets:
    @echo "🔑 Generating secrets..."
    @mkdir -p secrets nginx/ssl
    @test -f secrets/db_password.txt || openssl rand -hex 32 > secrets/db_password.txt
    @chmod 600 secrets/*

setup: secrets
    @echo "🔐 Generating crypto material..."
    @test -f nginx/ssl/rootCA.crt || openssl req -x509 -nodes -newkey rsa:2048 \
        -keyout nginx/ssl/rootCA.key \
        -out nginx/ssl/rootCA.crt \
        -days 365 -subj '/CN=TempCA/O=Development/C=US'
    @openssl dhparam -out nginx/ssl/dhparam.pem 2048
    @chmod 600 nginx/ssl/*

build: validate setup
    @echo "🏗️  Building Docker image..."
    @docker build $(BUILD_ARGS) -t $(DOCKER_IMAGE) .

clean:
    @echo "🧹 Cleaning artifacts..."
    @docker rmi -f $(DOCKER_IMAGE) 2>/dev/null || true
    @rm -rf secrets/*.txt nginx/ssl/*.pem

# ---- Security Checks ----
scan:
    @docker scan $(DOCKER_IMAGE)
    @trivy image $(DOCKER_IMAGE)