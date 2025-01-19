from django.contrib import admin
from .models import BaseAuto, AutoBrand, AutoModel


class BaseAutoAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'power', 'color', 'vin')
    search_fields = ('brand', 'model')

class AutoBrandAdmin(admin.ModelAdmin):
    list_display = ('title',)

class AutoModelAdmin(admin.ModelAdmin):
    list_display = ('title',)



admin.site.register(AutoBrand, AutoBrandAdmin)
admin.site.register(AutoModel, AutoModelAdmin)
admin.site.register(BaseAuto, BaseAutoAdmin)


