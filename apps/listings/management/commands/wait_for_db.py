# apps/listings/management/commands/wait_for_db.py
import time
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
from typing import Any

class Command(BaseCommand):
    """Wait for database availability before proceeding with application startup.
    
    Features:
    - Configurable timeout and retry interval
    - Clear progress reporting
    - Safe connection handling
    """
    
    help = "Waits for database connection to become available"

    def add_arguments(self, parser: Any) -> None:
        """Configure command-line arguments."""
        parser.add_argument(
            "--timeout",
            type=int,
            default=30,  # HARDCODED DEFAULT: Set via .env if needed
            help="Maximum wait time in seconds (default: %(default)s)"
        )
        parser.add_argument(
            "--interval",
            type=int,
            default=1,  # HARDCODED DEFAULT: Set to balance responsiveness vs load
            help="Seconds between connection attempts (default: %(default)s)"
        )

    def handle(self, *args: Any, **options: Any) -> None:
        """Execute the database connection wait logic."""
        timeout = options["timeout"]
        interval = options["interval"]
        max_attempts = timeout // interval
        db_alias = "default"  # HARDCODED: Change if using multiple databases

        self.stdout.write(f"Database connection check initiated (timeout: {timeout}s, interval: {interval}s)")

        for attempt in range(1, max_attempts + 1):
            try:
                connections[db_alias].ensure_connection()
                self._success()
                return
            except OperationalError as e:
                self._retry(attempt, max_attempts, interval, e)

        self._failure(timeout)
        raise TimeoutError(f"Database connection failed after {timeout} seconds")

    def _success(self) -> None:
        """Handle successful connection."""
        self.stdout.write(self.style.SUCCESS("Database connection established"))
        
    def _retry(self, attempt: int, max_attempts: int, interval: int, error: Exception) -> None:
        """Handle connection retries with progress updates."""
        self.stdout.write(
            f"Attempt {attempt}/{max_attempts}: "
            f"Connection failed ({error}). Retrying in {interval}s..."
        )
        time.sleep(interval)

    def _failure(self, timeout: int) -> None:
        """Handle final connection failure."""
        self.stdout.write(self.style.ERROR(
            f"Critical error: Could not connect to database within {timeout} seconds"
        ))