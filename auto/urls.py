from django.contrib import admin
from django.urls import path, include

from auto.settings import DEBUG

app_name = 'auto1'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auto/', include('auto_app.urls')),
    path('parking/', include('parking_app.urls')),
    path('news/', include('news_app.urls')),
]

if DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]

