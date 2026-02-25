from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('PARKING_OWNER', 'Parking Owner'),
        ('CUSTOMER', 'Customer'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CUSTOMER')
    phone = models.CharField(max_length=15, blank=True)

    def is_admin(self): return self.role == 'ADMIN'
    def is_owner(self): return self.role == 'PARKING_OWNER'
    def is_customer(self): return self.role == 'CUSTOMER'

class Vehicle(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    plate_number = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return self.plate_number
