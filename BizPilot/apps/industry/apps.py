"""
Industry App Configuration
"""
from django.apps import AppConfig


class IndustryConfig(AppConfig):
    """Configuration for the industry app"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.industry'
    verbose_name = 'Industries'
