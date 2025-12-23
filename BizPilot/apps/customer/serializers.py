"""
Customer Serializers

Handles serialization/deserialization of Customer data for API responses.
"""
from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for Customer model.
    
    Used for all CRUD operations on customers.
    The 'business' field is automatically set by BusinessCreateMixin,
    so we don't include it in the input fields.
    """
    
    # Read-only field showing which business the customer belongs to
    business_name = serializers.CharField(source='business.store_name', read_only=True)
    
    class Meta:
        model = Customer
        fields = [
            'id', 'name', 'email', 'phone', 'address', 'notes',
            'business_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'business_name', 'created_at', 'updated_at']
    
    def validate_phone(self, value):
        """
        Validate that phone number is unique within the business.
        
        This check is in addition to the database unique_together constraint.
        """
        # Get the business from the request context
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return value
        
        business = request.user.business
        
        # Check if phone already exists for this business (excluding current instance on update)
        queryset = Customer.objects.filter(business=business, phone=value)
        
        # If updating, exclude the current instance
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise serializers.ValidationError(
                "A customer with this phone number already exists in your business."
            )
        
        return value
    
    def validate_email(self, value):
        """
        Validate email format and normalize it.
        """
        if value:
            value = value.lower().strip()
        return value


class CustomerListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing customers.
    
    Used in list views where we don't need all details.
    Improves performance by reducing data transferred.
    """
    
    class Meta:
        model = Customer
        fields = ['id', 'name', 'phone', 'email', 'created_at']
        read_only_fields = ['id', 'created_at']
