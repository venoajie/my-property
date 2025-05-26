# apps/core/views.py
"""
System Status Endpoints

Security Considerations:
- Exposed without authentication (by design for health checks)
- Limited to GET requests only
- No sensitive data exposure in responses
- Rate limited via django-ratelimit

Key Functions:
1. rate_limit_exceeded: Custom handler for 429 responses
2. health_check: Comprehensive system status verification
"""

from django.http import HttpRequest, JsonResponse, HttpResponse
from django.db import connection
from django.db.utils import OperationalError
from django.views.decorators.http import require_GET
from django.core.cache import cache
from typing import Any

@require_GET
def rate_limit_exceeded(request: HttpRequest, exception: Exception) -> JsonResponse:
    """
    Custom handler for rate-limited requests
    
    Args:
        request: Incoming HTTP request
        exception: Ratelimit exception (not used but required by Django)
        
    Returns:
        JsonResponse: Standardized error response with 429 status
    """
    return JsonResponse(
        {
            "error": "rate_limit_exceeded",
            "message": "Too many requests. Please try again later.",
        },
        status=429,
    )

@require_GET
def health_check(request: HttpRequest) -> JsonResponse:
    """
    Comprehensive system health verification
    
    Flow:
    1. Database connection test
    2. Cache service verification
    3. Response construction with status codes
    
    Security:
    - No authentication required (essential for load balancers)
    - Limited to GET requests only
    
    Returns:
        JsonResponse: System status with appropriate HTTP status code
    """
    # Database Connectivity Check
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_status = "connected"
    except OperationalError as e:
        db_status = f"database_error: {str(e)}"
    
    # Cache Service Check
    try:
        # Test read/write capability
        cache.set("healthcheck", "ok", timeout=1)
        cached_value = cache.get("healthcheck")
        cache_status = "connected" if cached_value == "ok" else "unresponsive"
    except Exception as e:  # pylint: disable=broad-except
        cache_status = f"cache_error: {str(e)}"
    
    # Determine overall system status
    overall_status = 200 if db_status == "connected" else 503
    
    return JsonResponse(
        {
            "status": "ok" if overall_status == 200 else "degraded",
            "services": {
                "database": db_status,
                "cache": cache_status
            }
        },
        status=overall_status
    )