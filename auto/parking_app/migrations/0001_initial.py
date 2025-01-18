# Generated by Django 5.1.4 on 2025-01-18 15:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Parking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_number', models.CharField(blank=True, max_length=10, null=True, unique=True, verbose_name='Номер машины')),
                ('time_in', models.DateTimeField(auto_now_add=True, verbose_name='Время въезда')),
                ('time_out', models.DateTimeField(blank=True, null=True, verbose_name='Время выезда')),
                ('pay', models.BooleanField(default=False, verbose_name='Оплата')),
                ('number_place', models.PositiveIntegerField(blank=True, null=True, unique=True, validators=[django.core.validators.MaxValueValidator(500)], verbose_name='Номер места')),
            ],
            options={
                'verbose_name': 'Парковка',
                'verbose_name_plural': 'Парковки',
            },
        ),
    ]
