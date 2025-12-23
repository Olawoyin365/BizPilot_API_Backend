"""
Retail App Models

E-commerce and inventory management models for retail businesses.

Models:
- Category: Product categories
- Product: Products in inventory
- InventoryHistory: Tracks all inventory changes
"""
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Category(models.Model):
    """
    Product Category Model
    
    Organizes products into categories (e.g., Electronics, Clothing, Food).
    Each category belongs to a specific business (multi-tenancy).
    
    Fields:
        business: The business this category belongs to
        name: Category name
        description: Category description
        created_at: When category was created
    """
    
    business = models.ForeignKey(
        'account.Business',
        on_delete=models.CASCADE,
        related_name='categories',
        help_text="The business this category belongs to"
    )
    
    name = models.CharField(
        max_length=100,
        help_text="Category name (e.g., Electronics, Clothing)"
    )
    
    description = models.TextField(
        blank=True,
        help_text="Description of this category"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']
        unique_together = [['business', 'name']]  # Category names unique per business
        indexes = [
            models.Index(fields=['business', 'name']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.business.store_name})"


class Product(models.Model):
    """
    Product Model
    
    Represents products in a retail business's inventory.
    
    Fields:
        business: The business this product belongs to
        category: Product category
        name: Product name
        description: Product description
        price: Product price
        stock_quantity: Current stock level
        low_stock_threshold: Alert when stock falls below this
        sku: Stock Keeping Unit (optional)
        image: Product image
        created_at: When product was added
        updated_at: Last modification time
    """
    
    business = models.ForeignKey(
        'account.Business',
        on_delete=models.CASCADE,
        related_name='products',
        help_text="The business this product belongs to"
    )
    
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products',
        help_text="Product category"
    )
    
    name = models.CharField(
        max_length=255,
        help_text="Product name"
    )
    
    description = models.TextField(
        blank=True,
        help_text="Product description"
    )
    
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Product price"
    )
    
    stock_quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Current stock quantity"
    )
    
    low_stock_threshold = models.IntegerField(
        default=10,
        validators=[MinValueValidator(0)],
        help_text="Alert when stock falls below this level"
    )
    
    sku = models.CharField(
        max_length=100,
        blank=True,
        help_text="Stock Keeping Unit (SKU)"
    )
    
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        help_text="Product image"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['business', 'name']),
            models.Index(fields=['business', 'category']),
            models.Index(fields=['business', 'sku']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.business.store_name}"
    
    @property
    def is_low_stock(self):
        """Check if product stock is below threshold"""
        return self.stock_quantity <= self.low_stock_threshold
    
    @property
    def is_out_of_stock(self):
        """Check if product is out of stock"""
        return self.stock_quantity == 0


class InventoryHistory(models.Model):
    """
    Inventory History Model
    
    Tracks all changes to product inventory (additions, sales, adjustments).
    Provides an audit trail for inventory management.
    
    Change Types:
        - RESTOCK: Adding new stock
        - SALE: Reducing stock due to sale
        - ADJUSTMENT: Manual correction (damage, loss, found items, etc.)
        - RETURN: Customer returned an item
    """
    
    CHANGE_TYPE_CHOICES = [
        ('RESTOCK', 'Restock'),
        ('SALE', 'Sale'),
        ('ADJUSTMENT', 'Adjustment'),
        ('RETURN', 'Return'),
    ]
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='inventory_history',
        help_text="The product that was changed"
    )
    
    user = models.ForeignKey(
        'account.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        help_text="User who made the change"
    )
    
    change_type = models.CharField(
        max_length=20,
        choices=CHANGE_TYPE_CHOICES,
        help_text="Type of inventory change"
    )
    
    quantity_change = models.IntegerField(
        help_text="Change in quantity (positive for additions, negative for reductions)"
    )
    
    previous_quantity = models.IntegerField(
        help_text="Stock quantity before change"
    )
    
    new_quantity = models.IntegerField(
        help_text="Stock quantity after change"
    )
    
    notes = models.TextField(
        blank=True,
        help_text="Additional notes about the change"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Inventory History"
        verbose_name_plural = "Inventory Histories"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.product.name} - {self.change_type} ({self.quantity_change})"
