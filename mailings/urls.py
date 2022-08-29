from django.urls import path
from rest_framework import routers
from .views import MailingViewSet, ClientViewSet, MessageViewSet


router = routers.SimpleRouter()
router.register(r'api', MailingViewSet)
router.register(r'api', ClientViewSet)
router.register(r'api', MessageViewSet)

urlpatterns = [

]

urlpatterns += router.urls