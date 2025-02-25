from django.core.validators import MaxValueValidator
from django.db import models
from rest_framework.exceptions import ValidationError


class Car(models.Model):
    number = models.CharField(max_length=10, unique=True, verbose_name='Номер машины', null=True, blank=True)



    def __str__(self) -> str:
        return self.number

    class Meta():
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'


class Parking(models.Model):
    car_number = models.OneToOneField('Car', on_delete=models.CASCADE, null=True, blank=True, related_name='car_number')
    time_in = models.DateTimeField(auto_now_add=True, verbose_name='Время въезда')
    time_out = models.DateTimeField(null=True, blank=True, verbose_name='Время выезда')
    pay = models.BooleanField(default=False, verbose_name='Оплата')
    number_place = models.PositiveIntegerField(null=True, blank=True, unique=True,validators=[MaxValueValidator(500)], verbose_name='Номер места')


    def __str__(self):
        return f'Номер машины: {self.car_number} Время въезда: {self.time_in} Время выезда: {self.time_out} Оплата: {self.pay} Номер места: {self.number_place}'

    class Meta:
        verbose_name = 'Парковка'
        verbose_name_plural = 'Парковки'


class PenaltyOnCar(models.Model):
    number_penalty = models.PositiveIntegerField(null=True, blank=True, unique=True, validators=[MaxValueValidator(500)], verbose_name='Номер штрафа')
    pay_penalty = models.BooleanField(default=False, verbose_name='Оплата штрафа')
    time_penalty = models.DateTimeField(auto_now_add=True, verbose_name='Время получения штрафа')

    def __str__(self):
        return f'Номер штрафа: {self.number_penalty}'

    class Meta:
        verbose_name = 'Штраф'
        verbose_name_plural = 'Штрафы'


class CarPenalty(models.Model):
    car = models.ForeignKey('Car', on_delete=models.CASCADE, null=True, blank=True, related_name='car_penalty')
    penalty = models.ForeignKey('PenaltyOnCar', on_delete=models.CASCADE, null=True, blank=True, related_name='penalty_car')

    def __str__(self):
        return f'Номер машины: {self.car} Номер штрафа: {self.penalty}'

    class Meta:
        verbose_name = 'Штраф на машину'
        verbose_name_plural = 'Штрафы на машины'



