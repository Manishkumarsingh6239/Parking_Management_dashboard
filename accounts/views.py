from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views import View
from .forms import RegisterForm
from .models import CustomUser
from .models import Vehicle
from .forms import VehicleForm
from django.contrib.auth.mixins import LoginRequiredMixin


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
        return render(request, 'accounts/register.html', {'form': form})

class LoginView(View):
    def get(self, request):
        return render(request, 'accounts/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid credentials')
        return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

class VehicleListView(LoginRequiredMixin, View):
    def get(self, request):
        vehicles = Vehicle.objects.filter(owner=request.user)
        form = VehicleForm()
        return render(request, 'accounts/vehicles.html', {
            'vehicles': vehicles,
            'form': form
        })

class AddVehicleView(LoginRequiredMixin, View):
    def post(self, request):
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.owner = request.user
            vehicle.save()
            messages.success(request, f'Vehicle {vehicle.plate_number} added!')
            return redirect('vehicle_list')
        vehicles = Vehicle.objects.filter(owner=request.user)
        return render(request, 'accounts/vehicles.html', {
            'vehicles': vehicles,
            'form': form
        })

class DeleteVehicleView(LoginRequiredMixin, View):
    def post(self, request, vehicle_id):
        vehicle = get_object_or_404(Vehicle, id=vehicle_id, owner=request.user)
        vehicle.delete()
        messages.success(request, 'Vehicle removed!')
        return redirect('vehicle_list')
