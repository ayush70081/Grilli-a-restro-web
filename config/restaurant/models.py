from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta

class Reservation(models.Model):
    """
    Stores reservation info. We link to the Django built-in User model
    so that a reservation can belong to the user who created it.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    # email = models.EmailField()
    phone = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveIntegerField()
    special_requests = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} | {self.date} at {self.time}"

# Re-add the MenuItem model for dynamic menu items functionality.
class MenuItem(models.Model):
    CATEGORY_CHOICES = [
         ('starters', 'Starters'),
         ('mains', 'Main Course'),
         ('seafood', 'Seafood'),
         ('desserts', 'Desserts'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.URLField(blank=True, null=True)  # Use ImageField if file uploads are set up
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_formatted_price(self):
        """Return price formatted with ₹ symbol"""
        return f"₹{self.price}"

class MenuItemOption(models.Model):
    """Customization options for menu items (e.g., spice level, cooking preference)"""
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='options')
    name = models.CharField(max_length=100)  # e.g., "Spice Level", "Cooking Preference"
    choices = models.JSONField()  # e.g., ["Mild", "Medium", "Hot"]
    required = models.BooleanField(default=False)
    additional_cost = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.menu_item.name} - {self.name}"

class Order(models.Model):
    """Store customer orders"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready for Pickup'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    special_instructions = models.TextField(blank=True)
    pickup_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    preparing_at = models.DateTimeField(null=True, blank=True)
    ready_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username if self.user else 'Guest'}"

    def get_total_with_tax(self):
        tax_rate = Decimal('0.18')  # 18% GST
        tax_amount = self.total_amount * tax_rate
        return self.total_amount + tax_amount

    def save(self, *args, **kwargs):
        # Ensure pickup_time is timezone-aware
        if self.pickup_time and timezone.is_naive(self.pickup_time):
            self.pickup_time = timezone.make_aware(self.pickup_time)
        
        # Ensure all timestamps are in the correct timezone
        if not self.pickup_time:
            self.pickup_time = timezone.localtime(timezone.now() + timedelta(minutes=30))
        
        # Set confirmed_at when status changes to confirmed
        if self.status == 'confirmed' and not self.confirmed_at:
            self.confirmed_at = timezone.localtime(timezone.now())
        # Set preparing_at when status changes to preparing
        elif self.status == 'preparing' and not self.preparing_at:
            self.preparing_at = timezone.localtime(timezone.now())
        # Set ready_at when status changes to ready
        elif self.status == 'ready' and not self.ready_at:
            self.ready_at = timezone.localtime(timezone.now())
        # Set completed_at when status changes to completed
        elif self.status == 'completed' and not self.completed_at:
            self.completed_at = timezone.localtime(timezone.now())
        
        super().save(*args, **kwargs)

    def update_status(self, new_status):
        """Update order status and corresponding timestamp"""
        self.status = new_status
        
        # Update corresponding timestamp
        if new_status == 'confirmed' and not self.confirmed_at:
            self.confirmed_at = timezone.localtime(timezone.now())
        elif new_status == 'preparing' and not self.preparing_at:
            self.preparing_at = timezone.localtime(timezone.now())
        elif new_status == 'ready' and not self.ready_at:
            self.ready_at = timezone.localtime(timezone.now())
        elif new_status == 'completed' and not self.completed_at:
            self.completed_at = timezone.localtime(timezone.now())
        
        self.save()

class OrderItem(models.Model):
    """Individual items within an order"""
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True)  # Allow null for deleted menu items
    quantity = models.PositiveIntegerField(default=1)
    selected_options = models.JSONField(default=dict)
    item_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        # Handle case where menu_item is None
        item_name = self.menu_item.name if self.menu_item else "Deleted Item"
        return f"{item_name} x{self.quantity}"

    def save(self, *args, **kwargs):
        # Calculate item total, handling deleted menu items
        if self.menu_item:
            self.item_total = self.menu_item.price * self.quantity
        super().save(*args, **kwargs)
