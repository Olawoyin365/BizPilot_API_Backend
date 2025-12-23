"""
Customer App Configuration
"""
from django.apps import AppConfig


class CustomerConfig(AppConfig):
    """Configuration for the customer app"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.customer'
    verbose_name = 'Customer Management'
