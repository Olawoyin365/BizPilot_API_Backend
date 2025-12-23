"""
Customer Views

API endpoints for customer management (CRUD operations).
All operations are automatically scoped to the authenticated user's business.
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.core.mixins import BusinessQuerySetMixin, BusinessCreateMixin
from .models import Customer
from .serializers import CustomerSerializer, CustomerListSerializer


class CustomerViewSet(BusinessQuerySetMixin, BusinessCreateMixin, viewsets.ModelViewSet):
    """
    API endpoints for Customer management.
    
    Provides complete CRUD operations:
    - GET /api/customers/ - List all customers (paginated, searchable)
    - POST /api/customers/ - Create new customer
    - GET /api/customers/{id}/ - Get customer details
    - PUT /api/customers/{id}/ - Update customer
    - PATCH /api/customers/{id}/ - Partial update
    - DELETE /api/customers/{id}/ - Delete customer
    
    All operations are automatically filtered to show only customers
    belonging to the authenticated user's business.
    
    Features:
    - Search by name, phone, email
    - Ordering by name, created_at
    - Pagination (20 per page by default)
    """
    
    queryset = Customer.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'phone', 'email']
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']  # Default ordering: newest first
    
    def get_serializer_class(self):
        """
        Use lightweight serializer for list view, full serializer for detail views.
        """
        if self.action == 'list':
            return CustomerListSerializer
        return CustomerSerializer
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """
        Custom endpoint to get recently added customers.
        
        GET /api/customers/recent/
        
        Returns the 10 most recently added customers.
        """
        recent_customers = self.get_queryset()[:10]
        serializer = CustomerListSerializer(recent_customers, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search_by_phone(self, request):
        """
        Search for a customer by exact phone number.
        
        GET /api/customers/search_by_phone/?phone=1234567890
        
        Useful for quickly finding a customer when they call or visit.
        """
        phone = request.query_params.get('phone', None)
        
        if not phone:
            return Response(
                {'detail': 'Phone number is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        customer = self.get_queryset().filter(phone=phone).first()
        
        if not customer:
            return Response(
                {'detail': 'Customer not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
