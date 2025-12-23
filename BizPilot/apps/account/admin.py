"""
Account Admin Configuration

Django admin interface for managing businesses and users.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Business, CustomUser


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    """
    Admin interface for Business model.
    
    Features:
    - List view with key business info
    - Search by store name, email
    - Filter by industry, active status
    - View/edit business details
    """
    
    list_display = ['store_name', 'industry', 'country', 'email', 'is_active', 'created_at']
    list_filter = ['industry', 'is_active', 'country', 'created_at']
    search_fields = ['store_name', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Business Information', {
            'fields': ('store_name', 'email', 'phone', 'country', 'industry')
        }),
        ('Ownership', {
            'fields': ('owner',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin interface for CustomUser model.
    
    Extends Django's default UserAdmin with our custom fields.
    """
    
    list_display = ['email', 'username', 'business', 'is_business_owner', 'is_staff_member', 'is_active']
    list_filter = ['is_business_owner', 'is_staff_member', 'is_active', 'business__industry']
    search_fields = ['email', 'username', 'phone', 'business__store_name']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Business Information', {
            'fields': ('phone', 'business', 'is_business_owner', 'is_staff_member')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('email', 'phone', 'business', 'is_business_owner', 'is_staff_member')
        }),
    )
    
    # Make email the primary identifier in the admin
    ordering = ['email']
