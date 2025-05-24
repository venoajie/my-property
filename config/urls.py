# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from apps.core.views import health_check, rate_limit_exceeded

# Custom error handlers
handler429 = "apps.core.views.rate_limit_exceeded"

def home(request):
    """Temporary root view until frontend is connected"""
    return HttpResponse("Django is running")

urlpatterns = [
    # Admin interface
    path("admin/", admin.site.urls),
    
    # System endpoints
    path("health/", health_check, name="health-check"),
    path("", home, name="home"),
    
    # API endpoints
    path("api/auth/", include("apps.users.urls")),
    path("api/listings/", include("apps.listings.urls")),
]