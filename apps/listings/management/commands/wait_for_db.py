# management/commands/wait_for_db.py
import time
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError

class Command(BaseCommand):
    """Wait for database to become available with configurable timeout."""
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--timeout',
            type=int,
            default=30,
            help='Maximum time to wait for database (seconds)'
        )
        parser.add_argument(
            '--interval',
            type=int,
            default=1,
            help='Seconds between connection attempts'
        )

    def handle(self, *args, **options):
        timeout = options['timeout']
        interval = options['interval']
        max_attempts = timeout // interval
        
        self.stdout.write(f"Waiting for database (timeout: {timeout}s, interval: {interval}s)...")
        
        for attempt in range(1, max_attempts + 1):
            try:
                connections['default'].ensure_connection()
                self.stdout.write(self.style.SUCCESS('Database available!'))
                return
            except OperationalError as e:
                self.stdout.write(
                    f"Attempt {attempt}/{max_attempts}: "
                    f"Database unavailable ({str(e)}), retrying in {interval}s..."
                )
                time.sleep(interval)
        
        self.stdout.write(self.style.ERROR(f"Database connection timed out after {timeout} seconds!"))
        raise TimeoutError(f"Could not connect to database after {max_attempts} attempts")