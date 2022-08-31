from celery import shared_task
from .models import Mailing, Client, Message
from datetime import datetime


@shared_task
def hi():
    return 'Hello'

@shared_task
def mes_client():
    return Client.objects.get(id=1)

'''
TaskResult.objects.count()

'''
@shared_task
def mailing():
    mailing_pk = Mailing.objects.get(pk=1)
    now = datetime.now().strftime('%H:%M:%S')

    if mailing_pk.time_start_mailing.strftime('%H:%M:%S') <= now <= mailing_pk.time_end_mailing.strftime('%H:%M:%S'):
        return mailing_pk

