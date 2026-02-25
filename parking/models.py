from django.db import models
from accounts.models import CustomUser

class ParkingLot(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    total_slots = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return self.name

class ParkingSlot(models.Model):
    SLOT_TYPES = [('CAR', 'Car'), ('BIKE', 'Bike'), ('TRUCK', 'Truck')]
    lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE, related_name='slots')
    slot_number = models.CharField(max_length=20)
    slot_type = models.CharField(max_length=10, choices=SLOT_TYPES, default='CAR')
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['lot', 'slot_number']
        indexes = [models.Index(fields=['lot', 'is_active'])]

    def __str__(self): return f'{self.lot.name} - Slot {self.slot_number}'
