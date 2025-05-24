
from django.contrib import admin
from django.urls import path
from apps.core.views import health_check
from django.http import HttpResponse

# Simple view function for temporary landing page
def home(request):
    """Temporary root view for health checks"""
    return HttpResponse("Django is working!")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health_check, name='health-check'),
    path("", home, name="home"),
]



# Note: When creating apps:
# 1. Move views to separate views.py files
# 2. Use include() for app-specific routes
# 3. Add namespace for reverse URL lookups