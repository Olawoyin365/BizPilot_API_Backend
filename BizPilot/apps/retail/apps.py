"""
Retail App Configuration
"""
from django.apps import AppConfig


class RetailConfig(AppConfig):
    """Configuration for the retail app"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.retail'
    verbose_name = 'Retail & Inventory Management'
