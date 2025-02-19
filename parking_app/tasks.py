from datetime import datetime

from celery import shared_task
from . models import Parking, PenaltyOnCar


@shared_task
def auto_in_parking():
    print(Parking.objects.filter(time_in__isnull=False, pay=False))


# @shared_task()
# def penalty_of_the_hour():
#     dont_pay_parking = Parking.objects.filter(pay=False)
#     for parking in dont_pay_parking:
#         now = datetime.now()
#         fix_time = now - parking.time_in
#
#         if fix_time.total_seconds() >= 3600:
#             try:
#                 PenaltyOnCar.objects.create()



