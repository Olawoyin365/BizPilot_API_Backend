"""
Industry Models

Defines the different types of industries/business types supported 
by BizPilot (e.g., Retail, Tailoring, Education).

When a business registers, they select their industry type, which 
determines which features/apps are available to them.
"""
from django.db import models


class Industry(models.Model):
    """
    Industry/Business Type Model
    
    Represents different types of businesses that can use BizPilot.
    Examples: Retail, Tailoring, Education, Restaurant, etc.
    
    Fields:
        name: Industry name (e.g., "Retail", "Tailoring")
        description: Brief description of the industry
        is_active: Whether this industry is currently available for new signups
        created_at: Timestamp when industry was added
        updated_at: Timestamp when industry was last modified
    """
    
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Name of the industry (e.g., Retail, Tailoring, Education)"
    )
    
    description = models.TextField(
        blank=True,
        help_text="Brief description of what this industry does"
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this industry is available for new business registrations"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Industry"
        verbose_name_plural = "Industries"
        ordering = ['name']
    
    def __str__(self):
        """String representation of the industry"""
        return self.name
