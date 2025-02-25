from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

app_name = 'auto1'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auto/', include('auto_app.urls')),
    path('parking/', include('parking_app.urls')),
    path('news/', include('news_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

