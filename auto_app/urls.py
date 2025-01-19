from django.urls import path
from . views import AutoListView, index, AutoRUDView

app_name = 'auto_app'

urlpatterns = [
    path('', index, name='index'),
    path('auto_list/', AutoListView.as_view(), name='auto_list'),
    path('auto_list/<int:pk>', AutoRUDView.as_view(), name='auto_list')

]