from django.urls import path
from .views import InParkingViewSet, OutParkingView, AllPayPenalty, OnePayPenalty

app_name = 'parking_app'

urlpatterns = [
    path('in_parking/', InParkingViewSet.as_view(), name='in_parking'),
    path('out_parking/<int:pay>/', OutParkingView.as_view(), name='out_parking'),
    path('all_pay_penalty/', AllPayPenalty.as_view(), name='all_pay_penalty'),
    path('one_pay_penalty/<int:pk>/', OnePayPenalty.as_view(), name='one_pay_penalty')
    ]

