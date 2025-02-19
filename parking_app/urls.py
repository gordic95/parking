from django.urls import path
from .views import InParkingViewSet, OutParkingView

app_name = 'parking_app'

urlpatterns = [
    path('in_parking/', InParkingViewSet.as_view(), name='in_parking'),
    path('out_parking/<int:pay>/', OutParkingView.as_view(), name='out_parking'),
    # path('penalty/', PenaltyListView.as_view(), name='penalty'),
    # path('penalty/<int:pk>/', PenaltyDetailsView.as_view(), name='penalty'),
    ]

