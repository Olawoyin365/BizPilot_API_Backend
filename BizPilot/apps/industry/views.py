"""
Industry Views

API endpoints for retrieving available industries.
"""
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Industry
from .serializers import IndustrySerializer


class IndustryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for listing industries.
    
    Endpoints:
        GET /api/industries/ - List all active industries
        GET /api/industries/{id}/ - Get details of a specific industry
    """
    
    queryset = Industry.objects.filter(is_active=True)
    serializer_class = IndustrySerializer
    permission_classes = [AllowAny]
    pagination_class = None
