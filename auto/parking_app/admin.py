from django.contrib import admin
from .models import *


class ParkingAdmin(admin.ModelAdmin):
    list_display = ('car_number', 'time_in', 'time_out')
    list_filter = ('car_number', 'pay')

admin.site.register(Parking, ParkingAdmin)