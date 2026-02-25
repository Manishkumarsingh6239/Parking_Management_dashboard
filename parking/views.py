from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from .models import ParkingLot, ParkingSlot
from .forms import ParkingLotForm, ParkingSlotForm
from django.http import JsonResponse
from core.decorators import owner_required
from django.utils.decorators import method_decorator


class ParkingLotListView(View):
    def get(self, request):
        lots = ParkingLot.objects.filter(is_active=True).prefetch_related('slots')
        return render(request, 'parking/lot_list.html', {'lots': lots})

@method_decorator(owner_required, name='dispatch')
class ParkingLotCreateView(View):
    def get(self, request):
        return render(request, 'parking/lot_form.html', {'form': ParkingLotForm()})

    def post(self, request):
        form = ParkingLotForm(request.POST)
        if form.is_valid():
            lot = form.save(commit=False)
            lot.owner = request.user
            lot.save()
            messages.success(request, 'Parking lot created!')
            return redirect('owner_dashboard')
        return render(request, 'parking/lot_form.html', {'form': form})
    
@method_decorator(owner_required, name='dispatch')
class ParkingSlotCreateView(View):
    def get(self, request, lot_id):
        lot = get_object_or_404(ParkingLot, id=lot_id, owner=request.user)
        form = ParkingSlotForm()
        return render(request, 'parking/slot_form.html', {'form': form, 'lot': lot})

    def post(self, request, lot_id):
        lot = get_object_or_404(ParkingLot, id=lot_id, owner=request.user)
        form = ParkingSlotForm(request.POST)

        current_slot_count = lot.slots.count()
        if current_slot_count >= lot.total_slots:
            messages.error(request, f'Cannot add more slots! This lot only allows {lot.total_slots} slot(s). You already have {current_slot_count}.')
            return render(request, 'parking/slot_form.html', {'form': form, 'lot': lot})
        
        if form.is_valid():
            slot = form.save(commit=False)
            slot.lot = lot        # ← this is the key line
            slot.save()
            messages.success(request, 'Slot added successfully!')
            return redirect('owner_dashboard')
        return render(request, 'parking/slot_form.html', {'form': form, 'lot': lot})
    

@method_decorator(owner_required, name='dispatch')
class ToggleSlotView(View):
    def post(self, request, slot_id):
        slot = get_object_or_404(ParkingSlot, id=slot_id, lot__owner=request.user)
        slot.is_active = not slot.is_active  # flip True→False or False→True
        slot.save()
        status = "activated" if slot.is_active else "deactivated"
        messages.success(request, f'Slot {slot.slot_number} has been {status}!')
        return redirect('owner_dashboard')
