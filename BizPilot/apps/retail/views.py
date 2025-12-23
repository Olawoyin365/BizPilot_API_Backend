"""
Retail Views

API endpoints for retail/e-commerce functionality.
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from apps.core.mixins import BusinessQuerySetMixin, BusinessCreateMixin
from .models import Category, Product, InventoryHistory
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductListSerializer,
    InventoryUpdateSerializer,
    InventoryHistorySerializer
)


class CategoryViewSet(BusinessQuerySetMixin, BusinessCreateMixin, viewsets.ModelViewSet):
    """
    API endpoints for product categories.
    
    Endpoints:
    - GET /api/retail/categories/ - List categories
    - POST /api/retail/categories/ - Create category
    - GET /api/retail/categories/{id}/ - Get category details
    - PUT/PATCH /api/retail/categories/{id}/ - Update category
    - DELETE /api/retail/categories/{id}/ - Delete category
    """
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class ProductViewSet(BusinessQuerySetMixin, BusinessCreateMixin, viewsets.ModelViewSet):
    """
    API endpoints for products and inventory management.
    
    Main Endpoints:
    - GET /api/retail/products/ - List products (with search, filter, pagination)
    - POST /api/retail/products/ - Create product
    - GET /api/retail/products/{id}/ - Get product details
    - PUT/PATCH /api/retail/products/{id}/ - Update product
    - DELETE /api/retail/products/{id}/ - Delete product
    
    Additional Endpoints:
    - GET /api/retail/products/low_stock/ - Products below threshold
    - GET /api/retail/products/out_of_stock/ - Out of stock products
    - POST /api/retail/products/{id}/update_inventory/ - Update stock
    - GET /api/retail/products/search/ - Advanced search
    """
    
    queryset = Product.objects.select_related('category', 'business')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'sku', 'category__name']
    ordering_fields = ['name', 'price', 'stock_quantity', 'created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Use lightweight serializer for list view"""
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer
    
    def get_queryset(self):
        """
        Override to add filtering options via query parameters.
        
        Query params:
        - category: Filter by category ID
        - min_price: Minimum price
        - max_price: Maximum price
        - in_stock: true/false - filter by stock availability
        """
        queryset = super().get_queryset()
        
        # Filter by category
        category_id = self.request.query_params.get('category', None)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price', None)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        
        max_price = self.request.query_params.get('max_price', None)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Filter by stock availability
        in_stock = self.request.query_params.get('in_stock', None)
        if in_stock is not None:
            if in_stock.lower() == 'true':
                queryset = queryset.filter(stock_quantity__gt=0)
            elif in_stock.lower() == 'false':
                queryset = queryset.filter(stock_quantity=0)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """
        Get products with low stock (below threshold).
        
        GET /api/retail/products/low_stock/
        """
        from django.db.models import F
        
        low_stock_products = self.get_queryset().filter(
            stock_quantity__lte=F('low_stock_threshold')
        )
        
        serializer = ProductListSerializer(low_stock_products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def out_of_stock(self, request):
        """
        Get products that are out of stock.
        
        GET /api/retail/products/out_of_stock/
        """
        out_of_stock_products = self.get_queryset().filter(stock_quantity=0)
        
        serializer = ProductListSerializer(out_of_stock_products, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    @transaction.atomic
    def update_inventory(self, request, pk=None):
        """
        Update product inventory and create history record.
        
        POST /api/retail/products/{id}/update_inventory/
        
        Body:
        {
            "change_type": "RESTOCK|SALE|ADJUSTMENT|RETURN",
            "quantity": 10,
            "notes": "Optional notes"
        }
        """
        product = self.get_object()
        serializer = InventoryUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        change_type = serializer.validated_data['change_type']
        quantity = serializer.validated_data['quantity']
        notes = serializer.validated_data.get('notes', '')
        
        # Calculate quantity change based on type
        if change_type in ['RESTOCK', 'RETURN']:
            quantity_change = quantity
        else:  # SALE or ADJUSTMENT
            quantity_change = -quantity
        
        # Store previous quantity
        previous_quantity = product.stock_quantity
        new_quantity = previous_quantity + quantity_change
        
        # Validate new quantity
        if new_quantity < 0:
            return Response(
                {'detail': 'Insufficient stock for this operation.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update product stock
        product.stock_quantity = new_quantity
        product.save()
        
        # Create history record
        InventoryHistory.objects.create(
            product=product,
            user=request.user,
            change_type=change_type,
            quantity_change=quantity_change,
            previous_quantity=previous_quantity,
            new_quantity=new_quantity,
            notes=notes
        )
        
        return Response({
            'message': 'Inventory updated successfully',
            'previous_quantity': previous_quantity,
            'new_quantity': new_quantity,
            'is_low_stock': product.is_low_stock
        })


class InventoryHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoints for viewing inventory history.
    
    Endpoints:
    - GET /api/retail/inventory-history/ - List all changes
    - GET /api/retail/inventory-history/{id}/ - Get specific change details
    - GET /api/retail/inventory-history/by_product/{product_id}/ - History for specific product
    """
    
    serializer_class = InventoryHistorySerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Filter history to only show records for products in the user's business.
        """
        user = self.request.user
        if not user.is_authenticated or not user.business:
            return InventoryHistory.objects.none()
        
        return InventoryHistory.objects.filter(
            product__business=user.business
        ).select_related('product', 'user')
    
    @action(detail=False, methods=['get'], url_path='by_product/(?P<product_id>[^/.]+)')
    def by_product(self, request, product_id=None):
        """
        Get inventory history for a specific product.
        
        GET /api/retail/inventory-history/by_product/{product_id}/
        """
        history = self.get_queryset().filter(product_id=product_id)
        
        page = self.paginate_queryset(history)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(history, many=True)
        return Response(serializer.data)
