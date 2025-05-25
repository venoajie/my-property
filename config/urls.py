# config/urls.py
"""
Project URL Configuration

Security Notes:
- Admin path should be changed in production
- API endpoints are versioned for future compatibility
- Rate limiting applied via django-ratelimit
- Health check endpoint exposed without authentication

Flow:
1. Admin interface
2. System monitoring endpoints
3. API endpoints (versioned)
4. Frontend routes (to be handled by frontend server)
"""

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from apps.core.views import health_check, rate_limit_exceeded

# Custom error handlers (configured in settings)
handler429 = rate_limit_exceeded  # type: ignore

@require_GET
def temporary_root(request) -> HttpResponse:
    """Temporary root view until frontend is implemented
    
    Security: Exposed without authentication, replace before production
    """
    return HttpResponse(
        content="Django Application Running\n",
        content_type="text/plain",
        status=200
    )

urlpatterns = [
    # --- Administration ---
    # HARDCODED: Change 'admin/' to unique path in production
    path("admin/", admin.site.urls),
    
    # --- System Endpoints ---
    path("health", health_check, name="system-health-check"),
    path("", temporary_root, name="temporary-root"),
    
    # --- API Endpoints (v1) ---
    path("api/v1/auth/", include("apps.users.urls")),
    path("api/v1/listings/", include("apps.listings.urls")),

    # --- Future Integrations ---
    # Enable when implementing monitoring:
    # path('metrics', include('prometheus.urls')),
]