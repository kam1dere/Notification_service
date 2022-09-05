from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Client, Mailing
from django.db.models import Q
from datetime import datetime
from .tasks import message_for_client


@receiver(post_save, sender=Client)
def new_client(sender, instance):
    now = datetime.now()
    selection = Mailing.objects.filter(Q(date_start_mailing__gt=now) &
                                       Q(date_end_mailing__lt=now) &
                                       Q(tag__exact=instance.tag) &
                                       Q(mobile_operator_code__exact=instance.mobile_operator_code)).values_list(
                                            'message_text', flat=True)
    for message in selection:
        message_for_client(message, instance.phone_number)
    return 'success'
