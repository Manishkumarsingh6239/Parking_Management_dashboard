from rest_framework import viewsets, permissions
from .models import Reservation
from .serializers import ReservationSerializer

class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin():
            return Reservation.objects.all().select_related('customer', 'slot')
        return Reservation.objects.filter(customer=user).select_related('slot')

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)
