"""
Retail Admin Configuration
"""
from django.contrib import admin
from .models import Category, Product, InventoryHistory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for Category model"""
    
    list_display = ['name', 'business', 'product_count', 'created_at']
    list_filter = ['business', 'created_at']
    search_fields = ['name', 'business__store_name']
    readonly_fields = ['created_at', 'updated_at']
    
    def product_count(self, obj):
        """Display product count in list view"""
        return obj.products.count()
    product_count.short_description = 'Products'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin interface for Product model"""
    
    list_display = [
        'name', 'business', 'category', 'price', 
        'stock_quantity', 'low_stock_status', 'created_at'
    ]
    list_filter = ['business', 'category', 'created_at']
    search_fields = ['name', 'sku', 'business__store_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Product Information', {
            'fields': ('business', 'category', 'name', 'description', 'sku')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock_quantity', 'low_stock_threshold')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def low_stock_status(self, obj):
        """Display stock status with color coding"""
        if obj.is_out_of_stock:
            return '🔴 Out of Stock'
        elif obj.is_low_stock:
            return '🟡 Low Stock'
        return '🟢 In Stock'
    low_stock_status.short_description = 'Stock Status'


@admin.register(InventoryHistory)
class InventoryHistoryAdmin(admin.ModelAdmin):
    """Admin interface for Inventory History"""
    
    list_display = [
        'product', 'change_type', 'quantity_change', 
        'new_quantity', 'user', 'created_at'
    ]
    list_filter = ['change_type', 'created_at', 'product__business']
    search_fields = ['product__name', 'user__username', 'notes']
    readonly_fields = [
        'product', 'user', 'change_type', 'quantity_change',
        'previous_quantity', 'new_quantity', 'notes', 'created_at'
    ]
    
    # Make all fields read-only (history shouldn't be edited)
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
