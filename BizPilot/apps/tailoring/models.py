"""
Tailoring App Models

Models for tailoring/fashion design business operations:
- Measurement: Store customer measurements
- Task: Track tailoring tasks/orders
"""
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Measurement(models.Model):
    """
    Measurement Model
    
    Stores body measurements for customers.
    Each measurement record is for a specific garment type.
    
    Fields:
        business: The tailoring business
        customer: The customer being measured
        garment_type: Type of garment (Shirt, Dress, Suit, etc.)
        measurements: JSON field storing all measurements
        notes: Additional notes (fit preferences, special instructions)
        date_taken: When measurements were taken
    """
    
    GARMENT_TYPE_CHOICES = [
        ('MENS_SHIRT', "Men's Shirt"),
        ('MENS_TROUSERS', "Men's Trousers"),
        ('MENS_SUIT', "Men's Suit"),
        ('WOMENS_DRESS', "Women's Dress"),
        ('WOMENS_BLOUSE', "Women's Blouse"),
        ('WOMENS_SKIRT', "Women's Skirt"),
        ('TRADITIONAL', 'Traditional Wear'),
        ('OTHER', 'Other'),
    ]
    
    business = models.ForeignKey(
        'account.Business',
        on_delete=models.CASCADE,
        related_name='measurements',
        help_text="The business this measurement belongs to"
    )
    
    customer = models.ForeignKey(
        'customer.Customer',
        on_delete=models.CASCADE,
        related_name='measurements',
        help_text="The customer these measurements belong to"
    )
    
    garment_type = models.CharField(
        max_length=20,
        choices=GARMENT_TYPE_CHOICES,
        help_text="Type of garment these measurements are for"
    )
    
    # Common measurements (in inches or cm based on business preference)
    neck = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Neck measurement"
    )
    chest = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Chest/Bust measurement"
    )
    waist = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Waist measurement"
    )
    hips = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Hips measurement"
    )
    shoulder = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Shoulder width"
    )
    sleeve_length = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Sleeve length"
    )
    inseam = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Inseam (for trousers)"
    )
    length = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Garment length"
    )
    
    notes = models.TextField(
        blank=True,
        help_text="Additional notes (fit preferences, adjustments, etc.)"
    )
    
    date_taken = models.DateField(
        help_text="Date when measurements were taken"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Measurement"
        verbose_name_plural = "Measurements"
        ordering = ['-date_taken']
        indexes = [
            models.Index(fields=['business', 'customer']),
            models.Index(fields=['business', 'garment_type']),
        ]
    
    def __str__(self):
        return f"{self.customer.name} - {self.get_garment_type_display()} ({self.date_taken})"


class Task(models.Model):
    """
    Task Model
    
    Tracks tailoring tasks/orders from start to completion.
    Helps manage workflow and deadlines.
    
    Statuses:
        - NOT_STARTED: Task created, not begun
        - IN_PROGRESS: Currently being worked on
        - READY_FOR_FITTING: Ready for customer fitting
        - COMPLETED: Task finished
        - DELIVERED: Garment delivered to customer
    """
    
    STATUS_CHOICES = [
        ('NOT_STARTED', 'Not Started'),
        ('IN_PROGRESS', 'In Progress'),
        ('READY_FOR_FITTING', 'Ready for Fitting'),
        ('COMPLETED', 'Completed'),
        ('DELIVERED', 'Delivered'),
    ]
    
    GARMENT_TYPE_CHOICES = Measurement.GARMENT_TYPE_CHOICES
    
    business = models.ForeignKey(
        'account.Business',
        on_delete=models.CASCADE,
        related_name='tailoring_tasks',
        help_text="The business this task belongs to"
    )
    
    customer = models.ForeignKey(
        'customer.Customer',
        on_delete=models.CASCADE,
        related_name='tailoring_tasks',
        help_text="The customer this task is for"
    )
    
    measurement = models.ForeignKey(
        Measurement,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks',
        help_text="Associated measurement (optional)"
    )
    
    garment_type = models.CharField(
        max_length=20,
        choices=GARMENT_TYPE_CHOICES,
        help_text="Type of garment"
    )
    
    description = models.TextField(
        blank=True,
        help_text="Task description (fabric details, style, special requests)"
    )
    
    due_date = models.DateField(
        help_text="When this task should be completed"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='NOT_STARTED',
        help_text="Current status of the task"
    )
    
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Price for this task/order"
    )
    
    paid = models.BooleanField(
        default=False,
        help_text="Whether payment has been received"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ['due_date', '-created_at']
        indexes = [
            models.Index(fields=['business', 'status']),
            models.Index(fields=['business', 'due_date']),
            models.Index(fields=['business', 'customer']),
        ]
    
    def __str__(self):
        return f"{self.customer.name} - {self.get_garment_type_display()} (Due: {self.due_date})"
    
    @property
    def is_overdue(self):
        """Check if task is overdue"""
        from datetime import date
        return self.status not in ['COMPLETED', 'DELIVERED'] and self.due_date < date.today()
    
    @property
    def is_due_soon(self):
        """Check if task is due within 3 days"""
        from datetime import date, timedelta
        return self.due_date <= date.today() + timedelta(days=3)
