from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from parking.models import ParkingLot, ParkingSlot
from reservations.models import Reservation
from payments.models import Payment
from accounts.models import CustomUser
from .decorators import admin_required, owner_required, customer_required

def landing(request):
    return render(request, 'core/landing.html')

@login_required
def dashboard(request):
    user = request.user
    if user.is_admin():
        return redirect('admin_dashboard')
    elif user.is_owner():
        return redirect('owner_dashboard')
    else:
        return redirect('customer_dashboard')

@admin_required
def admin_dashboard(request):
    context = {
        'total_users': CustomUser.objects.count(),
        'total_lots': ParkingLot.objects.count(),
        'total_reservations': Reservation.objects.count(),
        'total_revenue': Payment.objects.filter(
            status='SUCCESS'
        ).aggregate(total=Sum('amount'))['total'] or 0,
        'recent_reservations': Reservation.objects.select_related(
            'customer', 'slot__lot'
        ).order_by('-created_at')[:10],
        'recent_payments': Payment.objects.select_related(
            'reservation__customer'
        ).order_by('-paid_at')[:10],
    }
    return render(request, 'core/admin_dashboard.html', context)

@owner_required
def owner_dashboard(request):
    lots = ParkingLot.objects.filter(
        owner=request.user
    ).prefetch_related('slots')

    owner_reservations = Reservation.objects.filter(
        slot__lot__owner=request.user
    ).select_related(
        'customer', 'slot', 'slot__lot'
    ).order_by('-created_at')

    # Calculate total earned from confirmed reservations
    total_earned = owner_reservations.filter(
        status='CONFIRMED'
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    context = {
        'lots': lots,
        'owner_reservations': owner_reservations,
        'total_earned': total_earned,
    }
    return render(request, 'core/owner_dashboard.html', context)

@customer_required
def customer_dashboard(request):
    reservations = Reservation.objects.filter(
        customer=request.user
    ).select_related('slot__lot', 'vehicle', 'payment')
    return render(request, 'core/customer_dashboard.html', {
        'reservations': reservations
    })