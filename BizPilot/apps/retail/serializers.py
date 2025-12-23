"""
Retail Serializers
"""
from rest_framework import serializers
from .models import Category, Product, InventoryHistory


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""
    
    product_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'product_count', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_product_count(self, obj):
        """Get count of products in this category"""
        return obj.products.count()
    
    def validate_name(self, value):
        """Ensure category name is unique within the business"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return value
        
        business = request.user.business
        queryset = Category.objects.filter(business=business, name__iexact=value)
        
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise serializers.ValidationError(
                "A category with this name already exists."
            )
        
        return value


class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for product listings"""
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    is_out_of_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category_name', 'price', 'stock_quantity',
            'is_low_stock', 'is_out_of_stock', 'created_at'
        ]


class ProductSerializer(serializers.ModelSerializer):
    """Full serializer for Product model"""
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    is_out_of_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'category', 'category_name',
            'price', 'stock_quantity', 'low_stock_threshold', 'sku',
            'image', 'is_low_stock', 'is_out_of_stock',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_category(self, value):
        """Ensure category belongs to the same business"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return value
        
        if value and value.business != request.user.business:
            raise serializers.ValidationError(
                "Category does not belong to your business."
            )
        
        return value


class InventoryUpdateSerializer(serializers.Serializer):
    """Serializer for updating inventory quantities"""
    
    change_type = serializers.ChoiceField(
        choices=InventoryHistory.CHANGE_TYPE_CHOICES,
        help_text="Type of inventory change"
    )
    quantity = serializers.IntegerField(
        min_value=1,
        help_text="Quantity to add or subtract"
    )
    notes = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Optional notes about the change"
    )


class InventoryHistorySerializer(serializers.ModelSerializer):
    """Serializer for Inventory History"""
    
    product_name = serializers.CharField(source='product.name', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = InventoryHistory
        fields = [
            'id', 'product_name', 'user_name', 'change_type',
            'quantity_change', 'previous_quantity', 'new_quantity',
            'notes', 'created_at'
        ]
