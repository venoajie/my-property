# my-property

folder structure:
.
├── apps
│   ├── core
│   │   ├── __init__.py
│   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   └── test_views.py
│   │   └── views.py
│   ├── __init__.py
│   ├── listings
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── __init__.py
│   │   ├── management
│   │   │   ├── commands
│   │   │   │   ├── __init__.py
│   │   │   │   └── wait_for_db.py
│   │   │   └── __init__.py
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── test_models.py
│   │   │   └── test_views.py
│   │   ├── urls.py
│   │   └── views.py
│   └── users
│       ├── admin.py
│       ├── __init__.py
│       ├── models.py
│       ├── tests
│       │   ├── __init__.py
│       │   └── test_models.py
│       ├── urls.py
│       └── views.py
├── config
│   ├── __init__.py
│   ├── settings
│   │   ├── base.py
│   │   ├── __init__.py
│   │   ├── local.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── README.md
├── real_estate
│   └── __init__.py
└── requirements
    ├── base.txt
    ├── dev.txt
    ├── __init__.py
    └── prod.txt