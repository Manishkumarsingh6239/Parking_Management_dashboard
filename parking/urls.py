from django.urls import path
from . import views

urlpatterns = [
    path('', views.ParkingLotListView.as_view(), name='parking_list'),
    path('create/', views.ParkingLotCreateView.as_view(), name='parking_create'),
    path('<int:lot_id>/add-slot/', views.ParkingSlotCreateView.as_view(), name='add_slot'),
    path('slot/<int:slot_id>/toggle/', views.ToggleSlotView.as_view(), name='toggle_slot'),  # ← add this
]