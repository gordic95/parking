from django.http import HttpResponse

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination

from . models import BaseAuto
from . serializers import AutoSerializer


class AutoListView(ListCreateAPIView):
    queryset = BaseAuto.objects.all()
    serializer_class = AutoSerializer
    pagination_class = PageNumberPagination

class AutoRUDView(RetrieveUpdateDestroyAPIView):
    queryset = BaseAuto.objects.all()
    serializer_class = AutoSerializer
    lookup_field = 'pk'

