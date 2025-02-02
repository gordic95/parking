from celery import shared_task
from . models import Parking


@shared_task
def auto_in_parking():
    print(Parking.objects.filter(time_in__isnull=False, pay=False))
