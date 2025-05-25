# my-property/apps/listings/apps.py
from django.apps import AppConfig

class ListingsConfig(AppConfig):
    name = 'listings'  # Must match directory name
    verbose_name = "Property Listings Management"