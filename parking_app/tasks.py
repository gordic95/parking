from datetime import datetime

from celery import shared_task

from .constants import NUMBER_PENALTY
from .models import Parking, CarPenalty, PenaltyOnCar


@shared_task
def auto_in_parking():
    print(Parking.objects.filter(time_in__isnull=False, pay=False))





@shared_task()
def pay_or_not_penalty():
    all_penalty = PenaltyOnCar.objects.all()
    #number_penalty #pay_penalty #time_penalty

    pay_or_not_parking = Parking.objects.filter(pay=False)
    #car_number #time_in #time_out #pay #number_place

    for car in pay_or_not_parking:
        now = datetime.now()    #время сейчас
        fix_time = now - car.time_in     #время с начала парковки и до сейчас
        # Если нам нужно прям каждый час фиксировать, нам нужно время считать от выписки последнего штрафа
        if fix_time.total_seconds() >= 3600:   #если время с начала парковки больше часа
            CarPenalty.objects.create(car=car.car_number, penalty=all_penalty.objects.create(number_penalty=NUMBER_PENALTY + 1))






