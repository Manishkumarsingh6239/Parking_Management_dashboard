from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_admin():
            messages.error(request, '❌ Access denied! Admins only.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

def owner_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_owner():
            messages.error(request, '❌ Access denied! Parking Owners only.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

def customer_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_customer():
            messages.error(request, '❌ This section is for Customers only.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper