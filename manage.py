#!/usr/bin/env python
import os
import sys
from django.core.management import execute_from_command_line

# Set default to production, override locally via environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

if __name__ == "__main__":
    try:
        execute_from_command_line(sys.argv)
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Make sure:"
            "\n1. You're in a virtual environment"
            "\n2. Django is installed (pip install django)"
        ) from exc

# Development Note: For local development, use:
# export DJANGO_SETTINGS_MODULE=config.settings.development