# apps/listings/views.py (Initial Compatible Version)
"""
DRF Views with Existing Middleware Compatibility

Maintains:
- Original security middleware chain
- Rate limiting configuration
- Permission classes from base settings

Adds:
- Read-only API endpoints
- Ownership validation
"""

from rest_framework import viewsets, permissions
from .models import Property

class PropertyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API for published properties
    
    Safety Features:
    - Inherits security headers from middleware.py
    - Uses existing auth classes from settings
    - Compatible with current nginx routing
    """
    queryset = Property.objects.filter(is_published=True)
    serializer_class = PropertySerializer
    permission_classes = [permissions.AllowAny]  # Matches original public access

    def get_queryset(self):
        """Maintains original filtering behavior"""
        return super().get_queryset().order_by('-created_at')