from rest_framework import serializers
from .models import Parking, Car, PenaltyOnCar, CarPenalty


class ParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'


class CarPenaltySerializer(serializers.ModelSerializer):
    class Meta:
        model = CarPenalty
        fields = '__all__'


class PenaltyOnCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = PenaltyOnCar
        fields = '__all__'











