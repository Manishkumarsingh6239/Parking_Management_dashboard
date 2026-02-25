from rest_framework import viewsets, permissions
from .models import ParkingLot, ParkingSlot
from .serializers import ParkingLotSerializer, ParkingSlotSerializer

class ParkingLotViewSet(viewsets.ModelViewSet):
    queryset = ParkingLot.objects.filter(is_active=True)
    serializer_class = ParkingLotSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_fields = ['city', 'is_active']
    search_fields = ['name', 'city']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ParkingSlotViewSet(viewsets.ModelViewSet):
    queryset = ParkingSlot.objects.select_related('lot')
    serializer_class = ParkingSlotSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['slot_type', 'is_active', 'lot']
