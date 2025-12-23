"""
Core App Configuration

This app contains shared utilities, mixins, and base classes 
used across all other apps in the BizPilot platform.
"""
from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Configuration for the core app"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
    verbose_name = 'Core Utilities'
