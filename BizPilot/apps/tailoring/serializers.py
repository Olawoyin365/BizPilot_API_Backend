"""
Tailoring Serializers
"""
from rest_framework import serializers
from datetime import date
from .models import Measurement, Task


class MeasurementSerializer(serializers.ModelSerializer):
    """Serializer for Measurement model"""
    
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    customer_phone = serializers.CharField(source='customer.phone', read_only=True)
    garment_type_display = serializers.CharField(source='get_garment_type_display', read_only=True)
    
    class Meta:
        model = Measurement
        fields = [
            'id', 'customer', 'customer_name', 'customer_phone',
            'garment_type', 'garment_type_display',
            'neck', 'chest', 'waist', 'hips', 'shoulder',
            'sleeve_length', 'inseam', 'length',
            'notes', 'date_taken', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_customer(self, value):
        """Ensure customer belongs to the same business"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return value
        
        if value.business != request.user.business:
            raise serializers.ValidationError(
                "Customer does not belong to your business."
            )
        
        return value
    
    def validate_date_taken(self, value):
        """Ensure date is not in the future"""
        if value > date.today():
            raise serializers.ValidationError(
                "Measurement date cannot be in the future."
            )
        return value


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model"""
    
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    customer_phone = serializers.CharField(source='customer.phone', read_only=True)
    garment_type_display = serializers.CharField(source='get_garment_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    is_due_soon = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'customer', 'customer_name', 'customer_phone',
            'measurement', 'garment_type', 'garment_type_display',
            'description', 'due_date', 'status', 'status_display',
            'price', 'paid', 'is_overdue', 'is_due_soon',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_customer(self, value):
        """Ensure customer belongs to the same business"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return value
        
        if value.business != request.user.business:
            raise serializers.ValidationError(
                "Customer does not belong to your business."
            )
        
        return value
    
    def validate_measurement(self, value):
        """Ensure measurement belongs to the same business and customer"""
        if value:
            request = self.context.get('request')
            if not request or not request.user.is_authenticated:
                return value
            
            if value.business != request.user.business:
                raise serializers.ValidationError(
                    "Measurement does not belong to your business."
                )
        
        return value
    
    def validate(self, attrs):
        """Cross-field validation"""
        # If measurement is provided, ensure it's for the same customer
        measurement = attrs.get('measurement')
        customer = attrs.get('customer')
        
        if measurement and customer and measurement.customer != customer:
            raise serializers.ValidationError({
                "measurement": "Measurement must belong to the selected customer."
            })
        
        return attrs


class TaskListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for task listings"""
    
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    garment_type_display = serializers.CharField(source='get_garment_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'customer_name', 'garment_type_display',
            'due_date', 'status_display', 'is_overdue', 'paid'
        ]
