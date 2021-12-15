from rest_framework import serializers
from parking.models import Parking_Space, Bookings

class ParkingSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking_Space
        fields = '__all__'
        read_only_fields = ['id']
    
class BookingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = '__all__'
        read_only_fields = ['id']

class UpdateBookingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = '__all__'
        read_only_fields = ['id','owner','ticket','parking_space']
