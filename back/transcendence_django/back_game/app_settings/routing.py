from back_game.app_settings import consumers
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r"ws/game/(?P<channel_id>\w+)/$", consumers.PlayerConsumer.as_asgi()),
]
