from django.db import models
from reservations.models import Reservation

class Payment(models.Model):
    STATUS_CHOICES = [('PENDING','Pending'),('SUCCESS','Success'),('FAILED','Failed')]
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    transaction_id = models.CharField(max_length=100, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self): return f'Payment for Reservation #{self.reservation.id}'
