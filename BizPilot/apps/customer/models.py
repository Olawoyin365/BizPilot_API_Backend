"""
Customer Models

Customer management shared across all industries.
Each customer belongs to a specific business (multi-tenancy).
"""
from django.db import models


class Customer(models.Model):
    """
    Customer Model
    
    Represents customers/clients of a business.
    Shared across all industries - retail customers, tailoring clients, etc.
    
    Multi-tenancy: Each customer belongs to one business and can only
    be seen/managed by that business.
    
    Fields:
        business: The business this customer belongs to (FK)
        name: Customer's full name
        email: Customer's email (optional)
        phone: Customer's phone number
        address: Customer's physical address (optional)
        notes: Additional notes about the customer (optional)
        created_at: When customer was added
        updated_at: Last modification time
    """
    
    business = models.ForeignKey(
        'account.Business',
        on_delete=models.CASCADE,
        related_name='customers',
        help_text="The business this customer belongs to"
    )
    
    name = models.CharField(
        max_length=255,
        help_text="Customer's full name"
    )
    
    email = models.EmailField(
        blank=True,
        null=True,
        help_text="Customer's email address"
    )
    
    phone = models.CharField(
        max_length=20,
        help_text="Customer's phone number"
    )
    
    address = models.TextField(
        blank=True,
        help_text="Customer's physical address"
    )
    
    notes = models.TextField(
        blank=True,
        help_text="Additional notes about the customer"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        ordering = ['-created_at']
        
        # Ensure phone numbers are unique within each business
        # (but different businesses can have customers with same phone)
        unique_together = [['business', 'phone']]
        
        # Add index for faster lookups
        indexes = [
            models.Index(fields=['business', 'phone']),
            models.Index(fields=['business', 'name']),
        ]
    
    def __str__(self):
        """String representation of the customer"""
        return f"{self.name} - {self.phone}"
