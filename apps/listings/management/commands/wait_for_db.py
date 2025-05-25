# apps/listings/management/commands/wait_for_db.py
"""
Database Connection Readiness Check

Purpose: Ensures database availability before application startup
Security: Contains no sensitive operations, only connection checks
Flow:
1. Parse command-line arguments
2. Attempt database connection with retries
3. Fail gracefully with timeout if unreachable
"""

import time
from typing import Any
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError, InterfaceError

class Command(BaseCommand):
    """Wait for database availability with configurable timeout and retries"""
    
    help = "Ensures database connectivity before application startup"
    
    def add_arguments(self, parser: Any) -> None:
        """Configure command-line parameters"""
        parser.add_argument(
            "--timeout", 
            type=int,
            default=60,  # HARDCODED: Set via DJANGO_DB_WAIT_TIMEOUT in production
            help="Maximum wait time in seconds (default: %(default)s)"
        )
        parser.add_argument(
            "--interval",
            type=int,
            default=3,  # HARDCODED: Set via DJANGO_DB_WAIT_INTERVAL if needed
            help="Retry interval in seconds (default: %(default)s)"
        )
        parser.add_argument(
            "--db-alias",
            type=str,
            default="default",  # HARDCODED: Use for multi-database setups
            help="Database connection alias (default: %(default)s)"
        )

    def handle(self, *args: Any, **options: Any) -> None:
        """Main command execution flow"""
        self._validate_options(options)
        success = self._attempt_connection(
            options["db_alias"],
            options["timeout"],
            options["interval"]
        )
        
        if not success:
            raise TimeoutError(f"Database unavailable after {options['timeout']}s")

    def _validate_options(self, options: dict) -> None:
        """Ensure parameter sanity"""
        if options["timeout"] <= 0:
            raise ValueError("Timeout must be positive integer")
        if options["interval"] <= 0:
            raise ValueError("Interval must be positive integer")

    def _attempt_connection(self, db_alias: str, timeout: int, interval: int) -> bool:
        """Main connection retry logic"""
        max_attempts = timeout // interval
        self.stdout.write(f"Checking database '{db_alias}' availability...")
        
        for attempt in range(1, max_attempts + 1):
            if self._test_connection(db_alias):
                return True
            self._log_attempt(attempt, max_attempts, interval)
            time.sleep(interval)
        
        return False

    def _test_connection(self, db_alias: str) -> bool:
        """Perform actual database connection test"""
        try:
            conn = connections[db_alias]
            conn.ensure_connection()
            if conn.is_usable():
                self.stdout.write(self.style.SUCCESS("Database connection verified"))
                return True
            return False
        except (OperationalError, InterfaceError) as e:
            self.stdout.write(self.style.WARNING(f"Connection error: {str(e)}"))
            return False

    def _log_attempt(self, attempt: int, max_attempts: int, interval: int) -> None:
        """Standardized attempt logging"""
        progress = f"[{attempt}/{max_attempts}]"
        message = f"{progress} Retrying in {interval}s..."
        self.stdout.write(message)