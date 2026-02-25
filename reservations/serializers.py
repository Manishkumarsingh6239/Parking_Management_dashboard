from rest_framework import serializers
from .models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.username', read_only=True)
    slot_info = serializers.CharField(source='slot.__str__', read_only=True)

    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ['customer', 'total_amount', 'status']
