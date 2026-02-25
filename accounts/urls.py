from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('vehicles/', views.VehicleListView.as_view(), name='vehicle_list'),      # ← add
    path('vehicles/add/', views.AddVehicleView.as_view(), name='add_vehicle'),    # ← add
    path('vehicles/delete/<int:vehicle_id>/', views.DeleteVehicleView.as_view(), name='delete_vehicle')
]
