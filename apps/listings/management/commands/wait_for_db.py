# management/commands/wait_for_db.py
import time
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError

class Command(BaseCommand):
    """Custom management command to wait for database availability."""
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--timeout',
            type=int,
            default=30,
            help='Maximum time to wait for database (in seconds)'
        )
        parser.add_argument(
            '--interval',
            type=int,
            default=1,
            help='Interval between retries (in seconds)'
        )

    def handle(self, *args, **options):
        """Entry point for command execution."""
        timeout = options['timeout']
        interval = options['interval']
        max_retries = timeout // interval
        
        self.stdout.write(f"Waiting for database connection (timeout: {timeout}s, interval: {interval}s)...")
        
        for attempt in range(1, max_retries + 1):
            try:
                connections["default"].ensure_connection()
                self.stdout.write(self.style.SUCCESS("Database available!"))
                return
            except OperationalError as e:
                self.stdout.write(
                    f"Attempt {attempt}/{max_retries}: "
                    f"Database unavailable ({str(e)}), retrying in {interval}s..."
                )
                time.sleep(interval)

        self.stdout.write(self.style.ERROR(f"Database connection timed out after {timeout} seconds!"))
        raise TimeoutError(f"Could not connect to database after {max_retries} attempts")