# my-property

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