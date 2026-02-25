import uuid
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Payment
from reservations.models import Reservation
from core.decorators import customer_required

@customer_required
@login_required
def payment_page(request, reservation_id):
    reservation = get_object_or_404(
        Reservation, id=reservation_id, customer=request.user
    )

    # If already paid, go to success directly
    if hasattr(reservation, 'payment') and reservation.payment.status == 'SUCCESS':
        return redirect('payment_success', payment_id=reservation.payment.id)

    if request.method == 'POST':
        transaction_id = 'TXN-' + str(uuid.uuid4())[:8].upper()
        payment = Payment.objects.create(
            reservation=reservation,
            amount=reservation.total_amount,
            status='SUCCESS',
            transaction_id=transaction_id,
            paid_at=timezone.now()
        )
        reservation.status = 'CONFIRMED'
        reservation.save()
        return redirect('payment_success', payment_id=payment.id)

    return render(request, 'payments/payment.html', {'reservation': reservation})

@customer_required
@login_required
def payment_success(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    return render(request, 'payments/success.html', {'payment': payment})