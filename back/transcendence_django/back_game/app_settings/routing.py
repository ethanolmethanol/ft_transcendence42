from back_game.app_settings import consumers
from django.urls import re_path

websocket_urlpatterns = [
    re_path(
        r"ws/game/classic/(?P<lobby_id>\w+)/$", consumers.ClassicConsumer.as_asgi()
    ),
    re_path(
        r"ws/game/tournament/(?P<lobby_id>\w+)/$",
        consumers.TournamentConsumer.as_asgi(),
    ),
]
