"""
Retail URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, InventoryHistoryViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'inventory-history', InventoryHistoryViewSet, basename='inventory-history')

urlpatterns = [
    path('', include(router.urls)),
]
