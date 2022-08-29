from backports import zoneinfo
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Mailing(models.Model):
    date_start_mailing = models.DateTimeField(verbose_name='Дата запуска рассылки')
    date_end_mailing = models.DateTimeField(verbose_name='Дата окончания рассылки')
    time_start_mailing = models.TimeField(verbose_name='Время запуска рассылки')
    time_end_mailing = models.TimeField(verbose_name='Время окончания рассылки')
    message_text = models.TextField(verbose_name='Текст сообщения для доставки клиенту')
    tag = models.CharField(max_length=100, verbose_name='Тэг', blank=True)
    mobile_operator_code = models.CharField(verbose_name='Код мобильного оператора',
                                            max_length=3, blank=True)

    def __str__(self):
        return f'Рассылка {self.pk} начиная с: {self.date_start_mailing}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


'''
Так как я предпологаю такой сценарий:
Неделю идет рассылка с какой-нибудь информацией в определенный период времения
то:
необходимо разделять поля времени и даты
с такого-то по такое-то число с такого-то по такое-то время

'''


class Client(models.Model):
    TIMEZONE_CHOICES = ((x, x) for x in sorted(zoneinfo.available_timezones(), key=str.lower))

    phone_number = PhoneNumberField()
    mobile_operator_code = models.CharField(verbose_name='Код мобильного оператора', max_length=3, editable=False)
    tag = models.CharField(verbose_name='Тэг', max_length=100, blank=True)
    timezone = models.CharField(choices=TIMEZONE_CHOICES, max_length=250, verbose_name='Часовой пояс')

    def save(self, *args, **kwargs):
        self.mobile_operator_code = str(self.phone_number)[2:5]
        return super(Client, self).save(*args, **kwargs)

    def __str__(self):
        return f'Клиент {self.pk} номер телефона: {self.phone_number}'


class Message(models.Model):
    SENT = 'Отправлена'
    NO_SENT = 'Не отправлена'

    STATUS_CHOICES = [
        (SENT, 'Отправлена'),
        (NO_SENT, 'Не отправлена'),
    ]

    time_create = models.DateTimeField(verbose_name='Дата и время создания (отправки)', auto_now_add=True)
    sending_status = models.CharField(verbose_name='Статус отправки', max_length=15, choices=STATUS_CHOICES)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='messages')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return f'Сообщение {self.pk} с текстом {self.mailing} для {self.client}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'