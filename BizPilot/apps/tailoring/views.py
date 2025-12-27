"""
Tailoring Views

API endpoints for tailoring business operations.
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import date, timedelta
from apps.core.mixins import BusinessQuerySetMixin, BusinessCreateMixin
from .models import Measurement, Task
from .serializers import (
    MeasurementSerializer,
    TaskSerializer,
    TaskListSerializer
)


class MeasurementViewSet(BusinessQuerySetMixin, BusinessCreateMixin, viewsets.ModelViewSet):
    """
    API endpoints for customer measurements.
    
    Endpoints:
    - GET /api/tailoring/measurements/ - List measurements
    - POST /api/tailoring/measurements/ - Create new measurement
    - GET /api/tailoring/measurements/{id}/ - Get measurement details
    - PUT/PATCH /api/tailoring/measurements/{id}/ - Update measurement
    - DELETE /api/tailoring/measurements/{id}/ - Delete measurement
    - GET /api/tailoring/measurements/by_customer/{customer_id}/ - Customer's measurements
    """
    
    queryset = Measurement.objects.select_related('business', 'customer')
    serializer_class = MeasurementSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['customer__name', 'customer__phone', 'notes']
    ordering_fields = ['date_taken', 'created_at']
    ordering = ['-date_taken']
    
    def get_queryset(self):
        """Add filtering by garment type and customer"""
        queryset = super().get_queryset()
        
        # Filter by garment type
        garment_type = self.request.query_params.get('garment_type', None)
        if garment_type:
            queryset = queryset.filter(garment_type=garment_type)
        
        # Filter by customer
        customer_id = self.request.query_params.get('customer', None)
        if customer_id:
            queryset = queryset.filter(customer_id=customer_id)
        
        return queryset
    
    @action(detail=False, methods=['get'], url_path='by_customer/(?P<customer_id>[^/.]+)')
    def by_customer(self, request, customer_id=None):
        """
        Get all measurements for a specific customer.
        
        GET /api/tailoring/measurements/by_customer/{customer_id}/
        """
        measurements = self.get_queryset().filter(customer_id=customer_id)
        serializer = self.get_serializer(measurements, many=True)
        return Response(serializer.data)


class TaskViewSet(BusinessQuerySetMixin, BusinessCreateMixin, viewsets.ModelViewSet):
    """
    API endpoints for tailoring tasks/orders.
    
    Main Endpoints:
    - GET /api/tailoring/tasks/ - List tasks (with filters)
    - POST /api/tailoring/tasks/ - Create new task
    - GET /api/tailoring/tasks/{id}/ - Get task details
    - PUT/PATCH /api/tailoring/tasks/{id}/ - Update task
    - DELETE /api/tailoring/tasks/{id}/ - Delete task
    
    Additional Endpoints:
    - GET /api/tailoring/tasks/today/ - Tasks due today
    - GET /api/tailoring/tasks/overdue/ - Overdue tasks
    - GET /api/tailoring/tasks/upcoming/ - Tasks due within 7 days
    - POST /api/tailoring/tasks/{id}/update_status/ - Update task status
    """
    
    queryset = Task.objects.select_related('business', 'customer', 'measurement')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['customer__name', 'customer__phone', 'description']
    ordering_fields = ['due_date', 'status', 'created_at']
    ordering = ['due_date']
    
    def get_serializer_class(self):
        """Use lightweight serializer for list view"""
        if self.action == 'list':
            return TaskListSerializer
        return TaskSerializer
    
    def get_queryset(self):
        """Add filtering options"""
        queryset = super().get_queryset()
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by garment type
        garment_type = self.request.query_params.get('garment_type', None)
        if garment_type:
            queryset = queryset.filter(garment_type=garment_type)
        
        # Filter by customer
        customer_id = self.request.query_params.get('customer', None)
        if customer_id:
            queryset = queryset.filter(customer_id=customer_id)
        
        # Filter by payment status
        paid = self.request.query_params.get('paid', None)
        if paid is not None:
            queryset = queryset.filter(paid=(paid.lower() == 'true'))
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """
        Get tasks due today.
        
        GET /api/tailoring/tasks/today/
        """
        today_tasks = self.get_queryset().filter(
            due_date=date.today()
        ).exclude(
            status__in=['COMPLETED', 'DELIVERED']
        )
        
        serializer = TaskListSerializer(today_tasks, many=True)
        return Response({
            'count': today_tasks.count(),
            'tasks': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """
        Get overdue tasks.
        
        GET /api/tailoring/tasks/overdue/
        """
        overdue_tasks = self.get_queryset().filter(
            due_date__lt=date.today()
        ).exclude(
            status__in=['COMPLETED', 'DELIVERED']
        )
        
        serializer = TaskListSerializer(overdue_tasks, many=True)
        return Response({
            'count': overdue_tasks.count(),
            'tasks': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """
        Get tasks due within the next 7 days.
        
        GET /api/tailoring/tasks/upcoming/
        """
        upcoming_date = date.today() + timedelta(days=7)
        upcoming_tasks = self.get_queryset().filter(
            due_date__range=[date.today(), upcoming_date]
        ).exclude(
            status__in=['COMPLETED', 'DELIVERED']
        )
        
        serializer = TaskListSerializer(upcoming_tasks, many=True)
        return Response({
            'count': upcoming_tasks.count(),
            'tasks': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """
        Update task status.
        
        POST /api/tailoring/tasks/{id}/update_status/
        
        Body:
        {
            "status": "IN_PROGRESS|READY_FOR_FITTING|COMPLETED|DELIVERED"
        }
        """
        task = self.get_object()
        new_status = request.data.get('status')
        
        if not new_status:
            return Response(
                {'detail': 'Status is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate status
        valid_statuses = [choice[0] for choice in Task.STATUS_CHOICES]
        if new_status not in valid_statuses:
            return Response(
                {'detail': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        task.status = new_status
        task.save()
        
        serializer = self.get_serializer(task)
        return Response({
            'message': 'Status updated successfully',
            'task': serializer.data
        })
