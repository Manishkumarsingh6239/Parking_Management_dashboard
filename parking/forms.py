from django import forms
from .models import ParkingLot, ParkingSlot

class ParkingLotForm(forms.ModelForm):
    class Meta:
        model = ParkingLot
        fields = ['name', 'address', 'city', 'total_slots']
        widgets = {'address': forms.Textarea(attrs={'rows': 3})}

class ParkingSlotForm(forms.ModelForm):
    class Meta:
        model = ParkingSlot
        fields = ['slot_number', 'slot_type', 'hourly_rate', 'is_active']
