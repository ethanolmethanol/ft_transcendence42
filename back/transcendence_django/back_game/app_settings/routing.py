from django.urls import re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/game/(?P<channel_id>\w+)/$", consumers.PlayerConsumer.as_asgi()),
]
