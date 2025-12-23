"""
Custom Permission Classes

These permissions provide fine-grained access control beyond 
Django's built-in IsAuthenticated permission.
"""
from rest_framework import permissions


class IsBusinessOwner(permissions.BasePermission):
    """
    Permission check: Only business owners can access this view.
    
    This is for sensitive operations like:
    - Business settings management
    - Staff account creation/deletion
    - Subscription management
    """
    
    def has_permission(self, request, view):
        """
        Check if user is authenticated and is a business owner.
        
        Args:
            request: The request object
            view: The view being accessed
            
        Returns:
            bool: True if user is business owner, False otherwise
        """
        return (
            request.user.is_authenticated and 
            hasattr(request.user, 'is_business_owner') and
            request.user.is_business_owner
        )


class IsBusinessOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission check: Business owners get full access, 
    staff members get read-only access.
    
    Use this for views where:
    - Staff can view data (GET, HEAD, OPTIONS)
    - Only owners can modify data (POST, PUT, PATCH, DELETE)
    """
    
    def has_permission(self, request, view):
        """
        Check permissions based on request method and user role.
        
        Args:
            request: The request object
            view: The view being accessed
            
        Returns:
            bool: True if user has permission, False otherwise
        """
        # Ensure user is authenticated
        if not request.user.is_authenticated:
            return False
        
        # Read permissions for any authenticated user with a business
        if request.method in permissions.SAFE_METHODS:
            return hasattr(request.user, 'business') and request.user.business is not None
        
        # Write permissions only for business owners
        return (
            hasattr(request.user, 'is_business_owner') and
            request.user.is_business_owner
        )


class BelongsToSameBusiness(permissions.BasePermission):
    """
    Object-level permission: Check if the object belongs to 
    the user's business.
    
    This provides an additional layer of security at the object level,
    though the queryset filtering should prevent most unauthorized access.
    """
    
    def has_object_permission(self, request, view, obj):
        """
        Check if the object belongs to the requesting user's business.
        
        Args:
            request: The request object
            view: The view being accessed
            obj: The object being accessed
            
        Returns:
            bool: True if object belongs to user's business, False otherwise
        """
        # Ensure user is authenticated
        if not request.user.is_authenticated:
            return False
        
        # Check if object has a business attribute
        if not hasattr(obj, 'business'):
            return False
        
        # Check if the object's business matches the user's business
        return obj.business == request.user.business
