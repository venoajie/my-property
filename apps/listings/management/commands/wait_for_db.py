# management/commands/wait_for_db.py
import time
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Custom management command to wait for database availability."""
    
    def handle(self, *args, **options):
        """Entry point for command execution."""
        self.stdout.write("Waiting for database connection...")
        
        max_retries = 30  # 30 seconds max wait
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                connections["default"].ensure_connection()
                self.stdout.write(self.style.SUCCESS("Database available!"))
                return
            except OperationalError:
                self.stdout.write(
                    f"Attempt {retry_count + 1}/{max_retries}: "
                    "Database unavailable, retrying in 1s..."
                )
                time.sleep(1)
                retry_count += 1

        self.stdout.write(self.style.ERROR("Database connection timed out!"))
        raise TimeoutError("Could not connect to database after 30 attempts")