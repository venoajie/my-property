from django.db import models

class Listing(models.Model):
    """Base model placeholder"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True