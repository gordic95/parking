from django.urls import path
from . import views

app_name = 'auto_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('auto_list/', views.AutoListView.as_view(), name='auto_list'),
]