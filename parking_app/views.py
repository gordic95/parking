from rest_framework import viewsets, generics, status
from rest_framework.exceptions import ValidationError

from .constants import ONE_HOUR_COST, MORE_ONE_HOUR_COST
from .models import Parking
from .serializers import ParkingSerializer
from rest_framework.response import Response
from django.utils import timezone



class InParkingViewSet(generics.CreateAPIView): #въезд машины
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer


    def create(self, request, *args, **kwargs):
        """Регистрация автомобилей на парковке"""
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({'message': 'Машина успешно зарегистрирована на парковке'},
                            status=status.HTTP_201_CREATED, headers=headers)
        except ValueError:
            return Response({'message': 'Ошибка регистрации машины'}, status=status.HTTP_400_BAD_REQUEST)


    def clean(self, request, *args, **kwargs):
        """Метод `clean` в Django используется для выполнения пользовательских проверок данных перед их сохранением."""
        car_number = request.data.get('car_number')
        if Parking.objects.filter(car_number=car_number, time_out__isnull=True).exists():
            raise ValidationError('Машина с таким номером уже на парковке')
        return super().clean(request, *args, **kwargs)





#-----------------------------------
    def in_and_out_parking_place(self):
        """Проверка наличия свободных мест."""
        base_count_parking_place = len(Parking.number_place_bool)
        occupied_places = Parking.objects.filter(time_out__isnull=True).count()  # Подсчет занятых мест
        free_place = base_count_parking_place - occupied_places                  # Подсчет свободных мест

        if free_place > 0:
            return f'Свободных мест: {free_place} Занятых мест: {occupied_places}, вы можете проехать на {occupied_places + 1}.'
        elif free_place == 0:
            return f'Все места свободны, проедьте на 1 место.'
        else:
            return 'Свободных мест нет.'


# def in_and_out_parking_place(self):
#     """Проверка наличия свободных мест."""
#     base_count_parking_place = len(Parking.number_place_bool)
#     free_place = 0
#     closed_place = 0
#     if Parking.objects.filter(time_in__isnull=False):
#         free_place = base_count_parking_place - 1
#         closed_place += 1
#         return f'Свободных мест: {free_place} Занятых мест: {closed_place}, вы можете проехать на {closed_place + 1} место'
#
#     if Parking.objects.filter(time_out__isnull=False):
#         free_place += 1
#         closed_place -= 1
#         return f'Свободных мест: {free_place} Занятых мест: {closed_place}'
#
#     if closed_place == base_count_parking_place:
#         return f'Свободных мест нет'


#-----------------------------------

class OutParkingView(generics.RetrieveUpdateDestroyAPIView): #выезд машины
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer
    lookup_field = 'pay'


    def calculate_money(self):
        """Подсчет стоимости пребывания машины на парковке."""
        if not self.time_out:
            raise ValueError("Выезд еще не зафиксирован.")

        time = self.time_out - self.time_in
        hours = int(time.total_seconds() / 3600)

        if hours <= 1:
            money = ONE_HOUR_COST
        else:
            money = MORE_ONE_HOUR_COST * hours

        return money


    def update(self, request, *args, **kwargs):
        """Выезд, проверка, подсчет стоимости и оплата."""
        instance = self.get_object()

        if not instance.pay:
            return Response({'message': 'Проезд еще не оплачена'}, status=status.HTTP_400_BAD_REQUEST)

        instance.time_out = timezone.now()
        instance.save()
        money = instance.calculate_money()
        return Response({'message': f'Выезд разрешен. Сумма к оплате: {money} руб.'}, status=status.HTTP_200_OK)

