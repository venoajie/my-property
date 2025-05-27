# apps/listings/apps.py  
"""  
Listing Application Registry  

Security Purpose:  
- Ensures proper model registration  
- Maintains app namespace isolation  
- Required for database migrations  

Design Rationale:  
- Explicit app_label declaration prevents Django registry conflicts  
- Full dotted path ensures consistent app discovery  
- Ready() method kept simple for auditability  
"""  

from django.apps import AppConfig  
from django.utils.translation import gettext_lazy as _  

class ListingsConfig(AppConfig):  
    # Critical security setting - must match project structure  
    name = 'apps.listings'  # HARDCODED: Do not change without migrations  
    verbose_name = _("Property Listings Management")  

    def ready(self):  
        """Security Note: Disabled until signal implementation"""  
        # Reserved for future signal registration  
        pass  