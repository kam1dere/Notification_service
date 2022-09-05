from celery import shared_task
from django.db.models import Q

from .models import Mailing, Client
from datetime import datetime


@shared_task
def mailing():
    mailing_pk = Mailing.objects.get(pk=1)
    now = datetime.now().strftime('%H:%M:%S')

    if mailing_pk.time_start_mailing.strftime('%H:%M:%S') <= now <= mailing_pk.time_end_mailing.strftime('%H:%M:%S'):
        selection = Client.objects.filter(Q(tag__exact=mailing_pk.tag) &
                                          Q(mobile_operator_code__exact=mailing_pk.mobile_operator_code)).values_list(
                                            'phone_number', flat=True)
        for client in selection:
            print(message_for_client(mailing_pk.message_text, client))
        return 'success'


@shared_task
def message_for_client(message_text, phone_number):
    return f'Сообщение: {message_text} для {phone_number}'
