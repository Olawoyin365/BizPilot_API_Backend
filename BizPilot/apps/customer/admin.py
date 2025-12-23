"""
Customer Admin Configuration
"""
from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """
    Admin interface for Customer model.
    """
    
    list_display = ['name', 'phone', 'email', 'business', 'created_at']
    list_filter = ['business', 'created_at']
    search_fields = ['name', 'phone', 'email', 'business__store_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('business', 'name', 'phone', 'email', 'address')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
