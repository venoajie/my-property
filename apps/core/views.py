# apps/core/views.py
from django.http import JsonResponse
from django.db import connection
from django.db.utils import OperationalError

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