from django.core.validators import MaxValueValidator
from django.db import models

class AutoBrand(models.Model):
    title = models.CharField(max_length=100, verbose_name='Марка авто')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Марка авто'
        verbose_name_plural = 'Марки авто'


class AutoModel(models.Model):
    title = models.CharField(max_length=100, verbose_name='Модель авто')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Модель авто'
        verbose_name_plural = 'Модели авто'

class BaseAuto(models.Model):
    power = models.PositiveIntegerField(validators=[MaxValueValidator(1000)], verbose_name='Мощность')
    color = models.CharField(max_length=20, verbose_name='Цвет')
    vin = models.CharField(max_length=20, unique=True, verbose_name='VIN')
    brand = models.ForeignKey(AutoBrand, on_delete=models.CASCADE, verbose_name='Марка авто')
    model = models.ForeignKey(AutoModel, on_delete=models.CASCADE, verbose_name='Модель авто')

    def __str__(self):
        return f'{self.brand} {self.model}'


    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'