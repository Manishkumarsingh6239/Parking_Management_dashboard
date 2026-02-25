from django.db import models
from django.utils import timezone
from accounts.models import CustomUser, Vehicle
from parking.models import ParkingSlot

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    slot = models.ForeignKey(ParkingSlot, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['start_time', 'end_time']),
            models.Index(fields=['slot', 'status']),
        ]

    def calculate_amount(self):
        duration = (self.end_time - self.start_time).total_seconds() / 3600
        return round(duration * float(self.slot.hourly_rate), 2)

    def __str__(self): return f'Reservation #{self.id} by {self.customer.username}'
