"""
Account App Configuration
"""
from django.apps import AppConfig


class AccountConfig(AppConfig):
    """Configuration for the account app"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.account'
    verbose_name = 'Authentication & Business Management'
