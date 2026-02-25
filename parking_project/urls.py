from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from parking.api_views import ParkingLotViewSet, ParkingSlotViewSet
from reservations.api_views import ReservationViewSet

router = DefaultRouter()
router.register(r'parking-lots', ParkingLotViewSet)
router.register(r'parking-slots', ParkingSlotViewSet)
router.register(r'reservations', ReservationViewSet, basename='reservation')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('parking/', include('parking.urls')),
    path('reservations/', include('reservations.urls')),
    path('payments/', include('payments.urls')),
    path('api/', include(router.urls)),
]
