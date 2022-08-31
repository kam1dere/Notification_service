from django.shortcuts import get_object_or_404

from .models import Mailing, Client, Message
from .serializers import MailingSerializer, ClientSerializer, MessageSerializer
from rest_framework import viewsets


class MailingViewSet(viewsets.ModelViewSet):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
