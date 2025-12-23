"""
Core Mixins for Multi-Tenancy

These mixins ensure automatic business-level data isolation across all apps.
They prevent businesses from seeing or modifying each other's data.

Usage:
    class MyViewSet(BusinessQuerySetMixin, BusinessCreateMixin, viewsets.ModelViewSet):
        queryset = MyModel.objects.all()
        serializer_class = MySerializer
"""
from rest_framework import status
from rest_framework.response import Response


class BusinessQuerySetMixin:
    """
    Automatically filters all querysets to show only data belonging to 
    the authenticated user's business.
    
    This is the PRIMARY security mechanism for multi-tenancy.
    Every list/retrieve operation automatically filters by business.
    """
    
    def get_queryset(self):
        """
        Override get_queryset to filter by the current user's business.
        
        Returns:
            QuerySet: Filtered queryset containing only objects belonging 
                     to the authenticated user's business
        """
        # Get the base queryset from the view
        queryset = super().get_queryset()
        
        # Get the authenticated user
        user = self.request.user
        
        # If user is not authenticated, return empty queryset
        if not user.is_authenticated:
            return queryset.none()
        
        # If user doesn't have a business (shouldn't happen), return empty
        if not hasattr(user, 'business') or user.business is None:
            return queryset.none()
        
        # Filter by the user's business
        return queryset.filter(business=user.business)


class BusinessCreateMixin:
    """
    Automatically sets the business field when creating new objects.
    
    This ensures that all newly created objects are automatically 
    associated with the authenticated user's business.
    """
    
    def perform_create(self, serializer):
        """
        Override perform_create to automatically set the business field.
        
        Args:
            serializer: The serializer instance with validated data
        """
        # Get the authenticated user's business
        business = self.request.user.business
        
        # Save the object with the business automatically set
        serializer.save(business=business)


class BusinessOwnerPermissionMixin:
    """
    Restricts certain actions to business owners only.
    
    Use this mixin for sensitive operations like:
    - Deleting important records
    - Modifying business settings
    - Managing staff accounts
    """
    
    def check_business_owner_permission(self):
        """
        Check if the current user is a business owner.
        
        Returns:
            bool: True if user is business owner, False otherwise
        """
        user = self.request.user
        
        # Check if user is authenticated
        if not user.is_authenticated:
            return False
        
        # Check if user is business owner
        return user.is_business_owner
    
    def destroy(self, request, *args, **kwargs):
        """
        Override destroy to check business owner permission.
        Only business owners can delete records.
        """
        if not self.check_business_owner_permission():
            return Response(
                {"detail": "Only business owners can perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().destroy(request, *args, **kwargs)
