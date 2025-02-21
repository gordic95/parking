from datetime import datetime, timedelta

from rest_framework import viewsets, generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.status import HTTP_400_BAD_REQUEST

from .constants import ONE_HOUR_COST, MORE_ONE_HOUR_COST, NUMBER_PLACE_BOOL
from .models import Parking, PenaltyOnCar, Car, CarPenalty
from .serializers import ParkingSerializer, CarSerializer, CarPenaltySerializer
from rest_framework.response import Response
from django.utils import timezone


class InParkingViewSet(generics.ListCreateAPIView): #въезд машины
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer

    def create(self, request, *args, **kwargs):
        """Регистрация вьезда авто на парковку"""
        true_keys = [key for key, value in NUMBER_PLACE_BOOL.items() if value is True]  # подсчет занятых мест
        false_keys = [key for key, value in NUMBER_PLACE_BOOL.items() if value is False]  # подсчет свободных мест

        if not false_keys:
            return Response({'message': 'Нет свободных мест'}, status=HTTP_400_BAD_REQUEST)
        number_place = false_keys[0]
        NUMBER_PLACE_BOOL[number_place] = True
        true_keys.append(number_place)
        false_keys.remove(number_place)

        parking_data = {
            'car_number': request.data.get('car_number'),
            'time_in': request.data.get('time_in'),
            # 'time_out': request.data.get('time_out'),   # эти поля нам не нужны на вьезде, поэтому их не заполняем
            # 'pay': request.data.get('pay'),
            'number_place': number_place
        }

        serializer = self.get_serializer(data=parking_data)  #получаем сериалайзер с нашими данными из parking_data
        serializer.is_valid(raise_exception=True)    #проверяем эти данные на верность
        self.perform_create(serializer)      #если все ок, сохраняем их
        headers = self.get_success_headers(serializer.data)

        return Response({'message': 'Машина успешно зарегистрирована на парковке.'}, status=status.HTTP_201_CREATED, headers=headers)


    def perform_create(self, serializer):
        serializer.save()


    def save(self, request, *args, **kwargs):
        """Сохраниние данных в БД."""
        if self.request.method == 'POST':
            self.clean(request, *args, **kwargs)
        return super().save(request, *args, **kwargs)


    def clean(self, request, *args, **kwargs):
        """Метод `clean` в Django используется для выполнения пользовательских проверок данных перед их сохранением."""
        car_number = request.data.get('car_number')
        if Parking.objects.filter(car_number=car_number, time_out__isnull=True).exists():
            raise ValidationError('Машина с таким номером уже на парковке')
        return super().clean(request, *args, **kwargs)


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
        instance = self.get_object()     #получаем обьект с которым будем работать

        if not instance.pay:
            return Response({'message': 'Проезд еще не оплачена'}, status=status.HTTP_400_BAD_REQUEST)

        instance.time_out = timezone.now()  #меняем время выезда на время, которое сейчас
        NUMBER_PLACE_BOOL[instance.number_place] = False   #освобождаем место на парковке нашей  воображаемой БД
        instance.save() #сохраняем
        money = instance.calculate_money()   #применяем метод для расчета оплаты
        return Response({'message': f'Выезд разрешен. Сумма к оплате: {money} руб. Место {instance.number_place} освободилось'}, status=status.HTTP_200_OK)


class OnePayPenalty(generics.RetrieveUpdateAPIView):  #оплата одного штрафа одой машины
    queryset = CarPenalty.objects.all()
    serializer_class = CarPenaltySerializer
    lookup_field = 'pk'


    def get(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        count_penalty = CarPenalty.objects.filter(car=instance.car).count()
        if count_penalty % 10 == 1:
            end : str = ''
        if count_penalty % 10 in [2, 3, 4]:
            end : str = 'а'
        if count_penalty % 10 in [5, 6, 7, 8, 9, 10, 0]:
            end : str = 'оф'
        if count_penalty == 0:
            end : str = 'ов'
        return Response({'message': f'Уважаемый владелец автомобиля {instance.car}. У вас {count_penalty} штраф{end}. Оплатить выбранный штраф.'}, status=status.HTTP_200_OK)


    def put(self, request, *args, **kwargs) -> Response:
            instance: CarPenalty = self.get_object()
            if instance.penalty.pay_penalty:
                return Response({'message': 'Штраф уже оплачен'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                instance.penalty.pay_penalty: bool = True
                instance.penalty.save()
                return Response({'message': f'Штраф № {instance.penalty.number_penalty} оплачен'}, status=status.HTTP_200_OK)


class AllPayPenalty(generics.UpdateAPIView, generics.ListAPIView):  #оплата всех штрафов машины
    queryset = CarPenalty.objects.all()
    serializer_class = CarPenaltySerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs) -> Response:
        queryset: CarPenalty = self.get_queryset()
        count: int = queryset.count()
        if count % 10 == 1:
            end : str = ''
        if count % 10 in [2, 3, 4]:
            end : str = 'а'
        if count % 10 in [5, 6, 7, 8, 9, 10, 0]:
            end : str = 'оф'
        return Response({'message': f'Уважаемый владелец автомобиля {queryset[0].car.number} у вас {count} штраф{end}. Оплатить все штрафы.'}, status=status.HTTP_200_OK)


    def put(self, request, *args, **kwargs) -> Response:
        queryset: CarPenalty = self.get_queryset()
        if queryset.filter(penalty__pay_penalty=True).exists():
            return Response({'message': 'Штрафы уже оплачены'}, status=status.HTTP_400_BAD_REQUEST)
        for instance in queryset:
            instance.penalty.pay_penalty: bool = True
            instance.penalty.save()
        return Response({'message': f'Все штрафы на авто с гос. номером {instance.car.number} оплачены'}, status=status.HTTP_200_OK)












