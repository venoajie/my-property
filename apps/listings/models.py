# apps/listings/models.py
"""
Core Data Model: Abstract Listing Base

Security Implementation:
- Provides audit trail through auto-tracked timestamps
- Abstract base prevents direct database table creation
- Serves as foundation for secure inheritance chain

Critical Components:
- created_at: Immutable creation timestamp (auto-set)
- updated_at: Mutation tracking timestamp (auto-updated)
- Meta.abstract: Enforces inheritance-only usage pattern
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

class Listing(models.Model):
    """
    Abstract base model for temporal data tracking
    
    Design Purpose:
    - Standardizes timestamp fields across concrete models
    - Implements DRY principle for audit requirements
    - Enables uniform historical tracking system-wide
    
    Inheritance Protocol:
    1. Extend this class for domain-specific models
    2. Concrete models MUST implement non-abstract Meta
    3. Add domain fields in child classes
    
    Security Constraints:
    - created_at remains immutable after initial save
    - updated_at automatically tracks modifications
    """
    
    # Audit Timeline Fields
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
        """Metaclass enforcing abstract inheritance pattern"""
        abstract = True  # Hardcoded: Critical for base model behavior
        verbose_name = _("Base Listing")
        verbose_name_plural = _("Base Listings")
        
        # HARDCODED PARAMETERS:
        # - abstract=True: Required to prevent direct instantiation
        # - Verbose names: Should match translation requirements