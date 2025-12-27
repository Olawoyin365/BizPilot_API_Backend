"""
BizPilot URL Configuration

This file routes all API endpoints to their respective apps.
All API endpoints are prefixed with /api/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/account/', include('apps.account.urls')),      # Authentication & Business
    path('api/industries/', include('apps.industry.urls')),  # Industry types
    path('api/customers/', include('apps.customer.urls')),   # Customer management
    path('api/retail/', include('apps.retail.urls')),        # Retail features
    path('api/tailoring/', include('apps.tailoring.urls')), # Tailoring features
    
    # JWT token refresh endpoint (common endpoint)
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
