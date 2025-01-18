from django.urls import path
from .views import InParkingViewSet, OutParkingView


urlpatterns = [
    path('in_parking/', InParkingViewSet.as_view(), name='in_parking'),
    path('out_parking/<int:pay>/', OutParkingView.as_view(), name='out_parking'),
    ]

