from django.urls import path
from . import consumers
from django.conf import settings

websocket_urlpatterns = [
    path(settings.B_WS_NAME, consumers.RobotConsumer.as_asgi())
]

