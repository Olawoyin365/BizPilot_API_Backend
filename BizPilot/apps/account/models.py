"""
Account Models

Core authentication models for BizPilot:
- Business: Represents a registered business/tenant
- CustomUser: Extended user model with business relationship
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField


class Business(models.Model):
    """
    Business Model - represents a tenant in the multi-tenant system.
    
    Each business is completely isolated from others. All business data
    (customers, products, etc.) is linked to a Business instance.
    
    Fields:
        store_name: The business/store name
        email: Business contact email
        phone: Business contact phone number
        country: Business location
        industry: Type of business (Retail, Tailoring, etc.)
        owner: The user who created/owns this business
        is_active: Whether the business account is active
        created_at: Registration date
    """
    
    store_name = models.CharField(
        max_length=255,
        help_text="Name of the business/store"
    )
    
    email = models.EmailField(
        unique=True,
        help_text="Business email address"
    )
    
    phone = models.CharField(
        max_length=20,
        help_text="Business phone number"
    )
    
    country = CountryField(
        help_text="Country where the business operates"
    )
    
    industry = models.ForeignKey(
        'industry.Industry',
        on_delete=models.PROTECT,  # Don't allow deleting an industry if businesses use it
        related_name='businesses',
        help_text="Type of business (e.g., Retail, Tailoring)"
    )
    
    owner = models.OneToOneField(
        'account.CustomUser',
        on_delete=models.CASCADE,
        related_name='owned_business',
        null=True,
        blank=True,
        help_text="The user who owns this business"
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this business account is active"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Business"
        verbose_name_plural = "Businesses"
        ordering = ['-created_at']
    
    def __str__(self):
        """String representation of the business"""
        return f"{self.store_name} ({self.industry.name})"


class CustomUser(AbstractUser):
    """
    Custom User Model extending Django's AbstractUser.
    
    Adds business relationship and role information to the standard user model.
    
    Additional Fields:
        email: Required and unique (overriding default)
        phone: User's phone number
        business: Link to the user's business (for multi-tenancy)
        is_business_owner: Whether this user owns their business
        is_staff_member: Whether this user is a staff member of a business
    
    Authentication:
        Users log in with their email (not username)
        Username is still required but can be auto-generated
    """
    
    # Override email to make it required and unique
    email = models.EmailField(
        unique=True,
        help_text="Email address - used for login"
    )
    
    phone = models.CharField(
        max_length=20,
        blank=True,
        help_text="User's phone number"
    )
    
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='users',
        help_text="The business this user belongs to"
    )
    
    is_business_owner = models.BooleanField(
        default=False,
        help_text="Whether this user owns their business"
    )
    
    is_staff_member = models.BooleanField(
        default=False,
        help_text="Whether this user is a staff member (not owner)"
    )
    
    # Use email for authentication instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Required for createsuperuser command
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-date_joined']
    
    def __str__(self):
        """String representation of the user"""
        return f"{self.email} ({self.business.store_name if self.business else 'No Business'})"
    
    def save(self, *args, **kwargs):
        """
        Override save to ensure email is lowercase.
        This prevents duplicate accounts with different case emails.
        """
        if self.email:
            self.email = self.email.lower()
        super().save(*args, **kwargs)
