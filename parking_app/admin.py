from django.contrib import admin
from .models import *


class ParkingAdmin(admin.ModelAdmin):
    list_display = ('car_number', 'time_in', 'time_out', 'number_place', 'penalty', 'pay')
    list_filter = ('car_number', 'pay')


class PenaltyOnCarAdmin(admin.ModelAdmin):
    list_display = ('number_penalty', 'pay_penalty', 'time_penalty')
    list_filter = ('number_penalty', 'pay_penalty', 'time_penalty')

admin.site.register(Parking, ParkingAdmin)
admin.site.register(PenaltyOnCar, PenaltyOnCarAdmin)