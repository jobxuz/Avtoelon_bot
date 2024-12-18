from celery import shared_task
from datetime import datetime
from apps.bot.utils.bs4data import data_id_funcsion, car_data


@shared_task
def hello_world():
    """
    Har daqiqada 'Salom dunyo' xabarini chiqaradi
    """
    vaqt = datetime.now().strftime('%H:%M:%S')
    xabar = f"Salom dunyo! Hozirgi vaqt: {vaqt}"
    print(xabar)
    return xabar



@shared_task
def add_cars():

    for i in data_id_funcsion():
        car_data(i)

    return "Barchasi qushildi!!!"




#      celery -A core worker --loglevel=info --pool=solo
#      celery -A core worker --beat --loglevel=info --pool=solo


