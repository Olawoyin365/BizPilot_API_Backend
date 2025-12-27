"""
Tailoring Admin Configuration
"""
from django.contrib import admin
from .models import Measurement, Task


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    """Admin interface for Measurement model"""
    
    list_display = [
        'customer', 'garment_type', 'business', 'date_taken', 'created_at'
    ]
    list_filter = ['business', 'garment_type', 'date_taken']
    search_fields = ['customer__name', 'customer__phone', 'notes']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('business', 'customer', 'garment_type', 'date_taken')
        }),
        ('Measurements', {
            'fields': (
                'neck', 'chest', 'waist', 'hips',
                'shoulder', 'sleeve_length', 'inseam', 'length'
            )
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Admin interface for Task model"""
    
    list_display = [
        'customer', 'garment_type', 'due_date', 
        'status', 'paid', 'business', 'overdue_status'
    ]
    list_filter = ['business', 'status', 'garment_type', 'paid', 'due_date']
    search_fields = ['customer__name', 'customer__phone', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('business', 'customer', 'garment_type', 'measurement')
        }),
        ('Task Details', {
            'fields': ('description', 'due_date', 'status')
        }),
        ('Payment', {
            'fields': ('price', 'paid')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def overdue_status(self, obj):
        """Display overdue status with color coding"""
        if obj.is_overdue:
            return '🔴 Overdue'
        elif obj.is_due_soon:
            return '🟡 Due Soon'
        return '🟢 On Track'
    overdue_status.short_description = 'Due Status'
