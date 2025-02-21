from django.contrib import admin
from .models import *


class ParkingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'car_number', 'time_in', 'time_out', 'number_place', 'pay')
    list_filter = ('car_number', 'pay')


class PenaltyOnCarAdmin(admin.ModelAdmin):
    list_display = ('pk', 'number_penalty', 'pay_penalty', 'time_penalty')
    list_filter = ('number_penalty', 'pay_penalty', 'time_penalty')


class CarAdmin(admin.ModelAdmin):
    list_display = ('pk', 'number',)


class CarPenaltyAdmin(admin.ModelAdmin):
    list_display = ('pk', 'car',)


admin.site.register(CarPenalty, CarPenaltyAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Parking, ParkingAdmin)
admin.site.register(PenaltyOnCar, PenaltyOnCarAdmin)