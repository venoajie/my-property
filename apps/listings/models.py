# apps/listings/models.py
"""
Enhanced Property Models with Ecosystem Safety

Maintains:
- Original abstract Listing base class
- Existing timestamp field behavior
- Compatibility with database migrations

Adds:
- Concrete business models
- Validation aligned with PostgreSQL constraints
- Security through ownership tracking
"""

from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

class Listing(models.Model):
    """(Preserves original abstract base implementation)"""
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Creation Timestamp"),
        help_text=_("Immutable record creation timestamp (UTC)")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Last Modified"),
        help_text=_("Tracked modification timestamp (UTC)")
    )

    class Meta:
        abstract = True
        verbose_name = _("Base Listing")
        verbose_name_plural = _("Base Listings")

class Property(Listing):
    """
    Concrete property model extending base
    
    Security Additions:
    - Owner foreign key to existing User model
    - Price validation matching PostgreSQL numeric(14,2)
    - Published state control
    """
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='properties',
        verbose_name=_("Property Owner")
    )
    price = models.DecimalField(
        max_digits=14,  # Matches PostgreSQL numeric(14,2) in compose
        decimal_places=2,
        validators=[MinValueValidator(50000)],  # Minimum $50k property
    )
    # ... (other fields maintain original behavior)