from . models import *
from rest_framework import serializers

class AutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseAuto
        fields = '__all__'