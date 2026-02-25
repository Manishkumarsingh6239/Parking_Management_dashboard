from django import forms
from django.utils import timezone
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['slot', 'vehicle', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time:

            # ✅ Check 1 — end time must be after start time
            if end_time <= start_time:
                raise forms.ValidationError(
                    '❌ Exit time must be after entry time!'
                )

            # ✅ Check 2 — booking must be at least 30 minutes
            duration_minutes = (end_time - start_time).total_seconds() / 60
            if duration_minutes < 30:
                raise forms.ValidationError(
                    '❌ Minimum booking duration is 30 minutes!'
                )

            # ✅ Check 3 — cannot book in the past
            if start_time < timezone.now():
                raise forms.ValidationError(
                    '❌ Entry time cannot be in the past!'
                )

        return cleaned_data