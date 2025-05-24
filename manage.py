# manage.py
import os
import sys
from django.core.management import execute_from_command_line

def main():
    """Entry point for Django management commands."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
    
    try:
        execute_from_command_line(sys.argv)
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Make sure:\n"
            "1. You're in a virtual environment\n"
            "2. Django is installed (pip install django)"
        ) from exc

if __name__ == "__main__":
    main()
    
# Development Note: For local development, use:
# export DJANGO_SETTINGS_MODULE=config.settings.development