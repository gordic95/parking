from datetime import datetime, timedelta

from rest_framework import viewsets, generics, status
from rest_framework.status import HTTP_400_BAD_REQUEST

from .constants import ONE_HOUR_COST, MORE_ONE_HOUR_COST, NUMBER_PLACE_BOOL
from .models import Parking, CarPenalty
from .serializers import ParkingSerializer, CarPenaltySerializer
from rest_framework.response import Response
from django.utils import timezone


class InParkingViewSet(generics.ListCreateAPIView): #въезд машины
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer

    def post(self, request, *args, **kwargs) -> Response:
        """Регистрация вьезда авто на парковку"""
        true_keys: list = [key for key, value in NUMBER_PLACE_BOOL.items() if value is True]  # подсчет занятых мест
        false_keys: list = [key for key, value in NUMBER_PLACE_BOOL.items() if value is False]  # подсчет свободных мест

        if not false_keys:
            return Response({'messagge': 'Нет свободных мест'}, status=HTTP_400_BAD_REQUEST)

        else: #если есть свободные места
            number_place = false_keys[0]   #занимаем первое свободное место
            NUMBER_PLACE_BOOL[number_place] = True  #занимаем это место в нашей аля БД
            true_keys.append(number_place)     #добавляем это место в true_keys
            false_keys.remove(number_place)    #удаляем это место из false_keys

            parking_data = {
                'car_number': request.data.get('car_number'),
                'time_in': request.data.get('time_in'),
                'number_place': number_place,
            }


            serializer = self.get_serializer(data=parking_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({'message': 'Машина успешно зарегистрирована на парковке.'}, status=status.HTTP_201_CREATED, headers=headers)


class OutParkingView(generics.RetrieveUpdateDestroyAPIView): #выезд машины
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer
    lookup_field = 'pk'


    def calculate_money(self) -> int:
        """Подсчет стоимости пребывания машины на парковке."""
        instance: Parking = self.get_object()
        time_on_parking: datetime = timezone.now() - instance.time_in
        hours: int = int(time_on_parking.total_seconds() / 3600)
        if hours <= 1:
            money = ONE_HOUR_COST
        else:
            money = MORE_ONE_HOUR_COST * hours
        return money


    def get(self, request, *args, **kwargs)-> Response:
        """Проверка информации о парковочном месте."""
        instance: Parking = self.get_object()
        time_on_parking: datetime = timezone.now() - instance.time_in
        return Response({'message': f'Парковочное место {instance.number_place}. Время парковки составляет: {time_on_parking}. Сумма к оплате: {self.calculate_money()} руб'})


    def pay_parking(self)-> Response:
        """Оплата парковки."""
        instance: Parking = self.get_object()
        instance.pay: bool = True
        instance.save()
        return Response({'message': f'Вы оплатили парковку на сумму {self.calculate_money()} руб.'}, status=status.HTTP_200_OK)


    def put(self, request, *args, **kwargs) -> Response:
        """Выезд и оплата."""
        instance: Parking = self.get_object()
        if instance.pay:
            instance.time_out: datetime = datetime.now()
            instance.pay: bool = True
            NUMBER_PLACE_BOOL[instance.number_place]: bool = False #освобождаем место на парковке нашей воображаемой БД
            instance.save()
            # money = instance.calculate_money()
            return Response({'message': f'Выезд разрешен. Место {instance.number_place} освободилось'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Вы еще не оплатили парковку'}, status=status.HTTP_400_BAD_REQUEST)


class OnePayPenalty(generics.RetrieveUpdateAPIView):  #оплата одного штрафа одой машины
    queryset = CarPenalty.objects.all()
    serializer_class = CarPenaltySerializer
    lookup_field = 'pk'


    def get(self, request, *args, **kwargs) -> Response:
        instance: CarPenalty = self.get_object()
        count_penalty: int = CarPenalty.objects.filter(car=instance.car).count()
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

    def get(self, request, *args, **kwargs):
        # get car pk
        # queryset = CarPenalty.objects.filter(
        queryset = self.get_queryset()
        count = queryset.count()
        if count % 10 == 1:
            end  = ''
        if count % 10 in [2, 3, 4]:
            end  = 'а'
        if count % 10 in [5, 6, 7, 8, 9, 10, 0]:
            end  = 'оф'
        return Response({'message': f'Уважаемый владелец автомобиля {queryset[0].car.number} у вас {count} штраф{end}. Оплатить все штрафы.'}, status=status.HTTP_200_OK)


    def put(self, request, *args, **kwargs) -> Response:
        queryset: CarPenalty = self.get_queryset()
        if queryset.filter(penalty__pay_penalty=True).exists():
            return Response({'message': 'Штрафы уже оплачены'}, status=status.HTTP_400_BAD_REQUEST)
        for instance in queryset:
            instance.penalty.pay_penalty: bool = True
            instance.penalty.save()
        return Response({'message': f'Все штрафы на авто с гос. номером {instance.car.number} оплачены'}, status=status.HTTP_200_OK)












