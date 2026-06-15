from email.policy import default

from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Bike(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    photo = models.ImageField(upload_to='vehicles/', null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.brand} {self.name}"
    
from django.db import models

class TestRide(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    address = models.TextField()
    license_number = models.CharField(max_length=50)
    license_expiry = models.DateField()
    preferred_bike = models.CharField(max_length=100)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    message = models.TextField(blank=True, null=True)
    agree_terms = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name
    

class BikeDesign(models.Model):
    """
    Model to store user-created bike designs
    """
    # Design metadata
    name = models.CharField(
        max_length=100,
        help_text="Name of the bike design"
    )
    
    # Canvas data stored as base64 PNG image
    design_data = models.TextField(
        help_text="Canvas drawing data as base64 PNG"
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the design was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When the design was last updated"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Bike Design"
        verbose_name_plural = "Bike Designs"
    
    def __str__(self):
        return f"{self.name}"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'design_data': self.design_data,
            'created_at': self.created_at.isoformat(),
        }