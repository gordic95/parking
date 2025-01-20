from django.core.validators import MaxValueValidator
from django.db import models
from rest_framework.exceptions import ValidationError

from . constants import ONE_HOUR_COST, MORE_ONE_HOUR_COST


class Parking(models.Model):
    car_number = models.CharField(max_length=10, unique=True, verbose_name='Номер машины', null=True, blank=True)
    time_in = models.DateTimeField(auto_now_add=True, verbose_name='Время въезда')
    time_out = models.DateTimeField(null=True, blank=True, verbose_name='Время выезда')
    pay = models.BooleanField(default=False, verbose_name='Оплата')
    number_place = models.PositiveIntegerField(null=True, blank=True, unique=True,validators=[MaxValueValidator(500)], verbose_name='Номер места')





    def __str__(self):
        return f'Номер машины: {self.car_number} Время въезда: {self.time_in} Время выезда: {self.time_out} Оплата: {self.pay} Номер места: {self.number_place}'

    class Meta:
        verbose_name = 'Парковка'
        verbose_name_plural = 'Парковки'





    # def save(self, *args, **kwargs):
    #     self.full_clean()
    #     return super().save(*args, **kwargs)