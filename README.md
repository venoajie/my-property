# File: README.md
# Purpose: Secure Deployment Guide for Real Estate Platform
# Security Level: Production (with development safeguards)

![Architecture Diagram](docs/architecture.png)  
*Production-ready microservice architecture with defense-in-depth security*

---

## Table of Contents
1. [Infrastructure Philosophy](#1-infrastructure-philosophy)  
2. [Security First Principles](#2-security-first-principles)  
3. [Deployment Workflow](#3-deployment-workflow)  
4. [Environment Configuration](#4-environment-configuration)  
5. [Monitoring & Maintenance](#5-monitoring--maintenance)  
6. [Troubleshooting](#6-troubleshooting)  

---

## 1. Infrastructure Philosophy

### Core Components
```text
.
├── .env                    # Environment secrets (NEVER commit this)
├── docker-compose.yml      # Production service definitions
├── config/
│   └── settings/
│       ├── base.py         # Shared configurations
│       └── production.py   # Security-hardened settings
└── nginx/
    ├── nginx.conf         # TLS 1.3 + Security headers
    └── ssl/               # Certificate storage (700 permissions)
```

**Design Rationale**:  
- **Isolation**: Services run in discrete containers  
- **Layered Security**: Multiple defense mechanisms at each architecture tier  
- **Auditability**: Clear separation of development vs production configurations
- **Automation**: Makefile-driven security setup

---

## 2. Security First Principles

### Critical Security Controls
```bash
#  Initialize security infrastructure 
make setup
```

| Control                  | Implementation Example               | Purpose                          |
|--------------------------|------------------------------------- |----------------------------------|
| Secret Rotation          | 	make secrets                      | Prevent credential compromise    |
| TLS Configuration        | make setup (Auto-generates DH params)| Perfect forward secrecy          |
| Container Hardening      | Non-root users in Dockerfiles        | Reduce attack surface            |
| Audit Trails             | Centralized Prometheus metrics       | Forensic readiness               |

Key Size	Estimated Time	Security Level	Use Case
2048-bit	2-5 minutes	Good	Development/Testing
4096-bit	30-90+ minutes	Excellent	Production

For Development (Speed Over Security):

bash
# Ctrl+C to cancel current operation
make clean-certs
sed -i 's/dhparam.pem 4096/dhparam.pem 2048/' Makefile
make setup

---

## 3. Deployment Workflow
#  Quick Start 
git clone https://github.com/yourusername/real-estate-platform.git  
cd real-estate-platform  

# Generate secrets and initialize infrastructure  
make setup 

# Full clean rebuild
make clean-certs
make setup


# Verify deployment  
make health  


---
---

## 4. Environment Configuration

### Critical Variables
| Variable                 | Example Value               | Security Consideration                    |
|--------------------------|-----------------------------|-------------------------------------------|
| `POSTGRES_PASSWORD`      | `$(openssl rand -hex 32)`   | 256-bit entropy, rotated monthly          |
| `AWS_ACCESS_KEY_ID`      | `AKIAXXXXXXXXXXXXXXXX`      | Use IAM roles where possible              |
| `TLS_CERTIFICATES        | `nginx/ssl/`                | Automated renewal via make renew-certs    |
| `REDIS_PASSWORD`         | `$(openssl rand -hex 32)`   | Separate from DB credentials              |

---

## 5. Monitoring & Maintenance
### Maintenance Procedures
# Renew SSL certificates  
make renew-certs  

### Monitoring Stack
| Service       | Access URL                  | Purpose                          |
|---------------|-----------------------------|----------------------------------|
| Prometheus    | `https://DOMAIN:9090`       | Metrics collection               |
| Grafana       | `https://DOMAIN:3000`       | Dashboard visualization          |
| Healthchecks  | Built-in `/api/health/`     | Service liveness verification    |

Component	Access Method	Maintenance Command
Database	PostgreSQL 16	make backup
Application	Django 4.2	make update
Monitoring	Prometheus + Grafana	make logs

6. Troubleshooting
Common Issues
Symptom	Solution	Verification Command
Certificate errors	make clean-certs && make setup	openssl verify nginx/ssl/*
Database connection fails	make migrate	make health
Permission denied	sudo chown -R 101:101 nginx/ssl	ls -l nginx/ssl/
Security Checklist
Run make setup after cloning repository

Set DEBUG=0 in production environments

Rotate secrets quarterly via make secrets

Replace development CA with production certificates




---
