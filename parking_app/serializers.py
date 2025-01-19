from rest_framework import serializers
from .models import Parking




class ParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = '__all__'


    def save(self, request, *args, **kwargs):
        """Сохраниние данных в БД."""
        if self.request.method == 'POST':
            self.clean(request, *args, **kwargs)
        return super().save(request, *args, **kwargs)