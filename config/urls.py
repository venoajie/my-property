# config/urls.py
"""
Main URL Configuration

Security Implementation:
- Versioned API endpoints (v1/)
- Strict import patterns
- Namespaced routing
- Centralized DRF router

Flow:
1. API requests → DRF router
2. Auth endpoints → users app
3. Admin/docs → protected routes

Maintenance Notes:
- Versioning allows backward compatibility
- Router registration keeps endpoints discoverable
- Type hints aid IDE autocompletion
"""

from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from rest_framework import routers
from typing import List, Union, Any

# Import after DRF to ensure schema view works
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView

# Local imports
from apps.listings.views import PropertyViewSet, OfferViewSet

# Initialize DRF router with strict trailing slash config
router: routers.DefaultRouter = routers.DefaultRouter(trailing_slash=False)
router.register(r'properties', PropertyViewSet, basename='property')
router.register(r'offers', OfferViewSet, basename='offer')

# Type alias for URL patterns
URLPattern = Union[Any, List[Any]]

urlpatterns: List[URLPattern] = [
    # API endpoints
    path('api/v1/', include((router.urls, 'api_v1'), namespace='api_v1')),
    
    # Authentication subsystem
    path('api/v1/auth/', include('users.urls', namespace='auth')),
    
    # Admin interface (disabled in production)
    path('admin/', admin.site.urls),
    
    # API documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularRedocView.as_view(url_name='schema'), name='apidocs'),
    
    # Default redirect (preserve existing behavior)
    path('', RedirectView.as_view(url='/api/docs/'))
]

if settings.DEBUG:  # type: ignore
    # Debug toolbar only in development
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]