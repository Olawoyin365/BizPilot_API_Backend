"""
Account URL Configuration

Routes for authentication and account management endpoints.
"""
from django.urls import path
from .views import (
    BusinessRegistrationView,
    login_view,
    UserProfileView,
    business_details_view
)

urlpatterns = [
    # Business registration (public)
    path('register/', BusinessRegistrationView.as_view(), name='register'),
    
    # User login (public)
    path('login/', login_view, name='login'),
    
    # User profile (authenticated)
    path('profile/', UserProfileView.as_view(), name='profile'),
    
    # Business details (authenticated)
    path('business/', business_details_view, name='business-details'),
]
