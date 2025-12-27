"""
Tailoring App Configuration
"""
from django.apps import AppConfig


class TailoringConfig(AppConfig):
    """Configuration for the tailoring app"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.tailoring'
    verbose_name = 'Tailoring & Fashion Design'
