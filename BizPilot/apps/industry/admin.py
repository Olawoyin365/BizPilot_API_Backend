"""
Industry Admin Configuration
"""
from django.contrib import admin
from .models import Industry


@admin.register(Industry)
class CustomerAdmin(admin.ModelAdmin):
    """
    Admin interface for Industry model.
    """
    
    list_display = ['id', 'name']


