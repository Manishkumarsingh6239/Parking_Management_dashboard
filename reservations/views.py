from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.views import View
from .models import Reservation
from .forms import ReservationForm
from parking.models import ParkingSlot
from core.decorators import customer_required
from django.utils.decorators import method_decorator

@method_decorator(customer_required, name='dispatch')
class BookSlotView(View):
    def get(self, request, slot_id):
        slot = get_object_or_404(ParkingSlot, id=slot_id)
        form = ReservationForm(initial={'slot': slot})
        return render(request, 'reservations/book.html', {'form': form, 'slot': slot})

    @transaction.atomic
    def post(self, request, slot_id):
        slot = get_object_or_404(ParkingSlot, id=slot_id)
        form = ReservationForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_time']
            end = form.cleaned_data['end_time']
            # Check overlapping
            overlap = Reservation.objects.filter(
                slot=slot, status__in=['PENDING', 'CONFIRMED'],
                start_time__lt=end, end_time__gt=start
            ).exists()
            if overlap:
                messages.error(request, 'This slot is already booked for that time!')
                return render(request, 'reservations/book.html', {'form': form, 'slot': slot})
            reservation = form.save(commit=False)
            reservation.customer = request.user
            reservation.total_amount = reservation.calculate_amount()
            reservation.save()
            return redirect('payment', reservation_id=reservation.id)
        return render(request, 'reservations/book.html', {'form': form, 'slot': slot})
