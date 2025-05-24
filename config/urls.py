
from django.contrib import admin
from django.urls import path
from apps.core.views import health_check,rate_limit_exceeded
from django.http import HttpResponse

handler429 = "apps.core.views.rate_limit_exceeded"

# Simple view function for temporary landing page
def home(request):
    """Temporary root view for health checks"""
    return HttpResponse("Django is working!")


urlpatterns = [
    # Core functionality
    path("admin/", admin.site.urls),
    path("health/", health_check, name="health-check"),
    
    # App routes
    path("api/auth/", include("apps.users.urls")),
    path("api/listings/", include("apps.listings.urls")),
    
    # Temporary landing
    path("", home, name="home"),
]


# Note: When creating apps:
# 1. Move views to separate views.py files
# 2. Use include() for app-specific routes
# 3. Add namespace for reverse URL lookups