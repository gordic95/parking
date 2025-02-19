from rest_framework import serializers
from .models import Parking, PenaltyOnCar


class ParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = '__all__'


class PenaltyOnCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = PenaltyOnCar
        fields = '__all__'

    def create(self, validated_data):
        return PenaltyOnCar.objects.create(**validated_data)


    def update(self, instance, validated_data):
        instance.pay_penalty = validated_data.get('pay_penalty', instance.pay_penalty)
        return instance










