from rest_framework import serializers
from .models import ParkingLot, ParkingSlot

class ParkingSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSlot
        fields = '__all__'

class ParkingLotSerializer(serializers.ModelSerializer):
    slots = ParkingSlotSerializer(many=True, read_only=True)
    owner_name = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = ParkingLot
        fields = '__all__'
