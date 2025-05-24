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
        retry_delay = 1  # 1 second between retries

        for attempt in range(1, max_retries + 1):
            try:
                connections["default"].ensure_connection()
                self.stdout.write(self.style.SUCCESS("Database available!"))
                return
            except OperationalError as e:
                self.stdout.write(
                    f"Attempt {attempt}/{max_retries}: "
                    f"Database unavailable ({str(e)}), retrying in {retry_delay}s..."
                )
                time.sleep(retry_delay)

        self.stdout.write(self.style.ERROR("Database connection timed out!"))
        raise TimeoutError(f"Could not connect to database after {max_retries} attempts")