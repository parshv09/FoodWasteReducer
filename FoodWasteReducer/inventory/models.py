from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

def default_expiry_date():
    return timezone.now().date() + timezone.timedelta(days=7)

class FoodItem(models.Model):
    CATEGORY_CHOICES = [
        ('FRUIT', 'Fruits'),
        ('VEG', 'Vegetables'),
        ('DAIRY', 'Dairy'),
        ('MEAT', 'Meat'),
        ('GRAIN', 'Grains'),
        ('OTHER', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)  # Changed from CharField
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='OTHER')
    expiry_date = models.DateField(default=default_expiry_date)  # Using named function
    added_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.quantity})"
    
    def is_expiring_soon(self):
        return (self.expiry_date - timezone.now().date()).days <= 3