# apps/listings/management/commands/wait_for_db.py
import time
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError

class Command(BaseCommand):
    """Wait for database availability before application startup"""
    
    help = "Waits for database connection"
    
    def add_arguments(self, parser):
        parser.add_argument(
            "--timeout", 
            type=int,
            default=60,  # HARDCODED: Set via .env if needed
            help="Maximum wait seconds (default: %(default)s)"
        )
        parser.add_argument(
            "--interval",
            type=int,
            default=3,
            help="Retry interval in seconds (default: %(default)s)"
        )

    def handle(self, *args, **options):
        """Main command logic"""
        max_attempts = options["timeout"] // options["interval"]
        db_alias = "default"  # HARDCODED: Change for multiple DBs
        
        for attempt in range(1, max_attempts + 1):
            if self._try_connection(db_alias):
                return
            self._wait(attempt, max_attempts, options["interval"])
        
        raise TimeoutError(f"Database unavailable after {options['timeout']}s")

    def _try_connection(self, db_alias: str) -> bool:
        """Attempt database connection"""
        try:
            connections[db_alias].ensure_connection()
            self.stdout.write(self.style.SUCCESS("Database connected"))
            return True
        except OperationalError:
            return False

    def _wait(self, attempt: int, max_attempts: int, interval: int):
        """Handle wait between attempts"""
        self.stdout.write(f"Attempt {attempt}/{max_attempts}: Waiting {interval}s...")
        time.sleep(interval)