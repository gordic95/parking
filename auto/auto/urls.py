from django.contrib import admin
from django.urls import path, include

app_name = 'auto'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auto/', include('auto_app.urls')),
    path('parking/', include('parking_app.urls')),
]
