# apps/core/views.py
from django.http import JsonResponse
from django.db import connection
from django.db.utils import OperationalError
from django.views.decorators.http import require_GET

@require_GET
def rate_limit_exceeded(request, exception):
    return JsonResponse(
        {
            "error": "rate_limit_exceeded",
            "message": "Too many requests. Please try again later.",
        },
        status=429,
    )
def health_check(request):
    """Enhanced health check with DB verification"""
    try:
        # Simple DB query to verify connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_status = "connected"
    except OperationalError as e:
        db_status = f"error: {str(e)}"
    
    return JsonResponse({
        "status": "ok",
        "services": {
            "database": db_status,
            "cache": "enabled"  # Add Redis/memcached check later
        }
    }, status=200 if db_status == "connected" else 503)