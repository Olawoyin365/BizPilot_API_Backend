"""
Industry Serializers

Handles serialization/deserialization of Industry data for API responses.
"""
from rest_framework import serializers
from .models import Industry


class IndustrySerializer(serializers.ModelSerializer):
    """
    Serializer for Industry model.
    
    Used for:
    - Listing available industries during business registration
    - Displaying industry details in business responses
    
    Returns read-only data - industries are managed by admins only.
    """
    
    class Meta:
        model = Industry
        fields = ['id', 'name', 'description', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']
