from django.urls import path
from . views import AutoListView, AutoRUDView

app_name = 'auto_app'

urlpatterns = [
    path('auto_list/', AutoListView.as_view(), name='auto_list'),
    path('auto_list/<int:pk>', AutoRUDView.as_view(), name='auto_list')

]