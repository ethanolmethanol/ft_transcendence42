from back_game.app_settings import consumers, tournament_consumers
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r"ws/game/classic/(?P<channel_id>\w+)/$", consumers.ClassicConsumer.as_asgi()),
    re_path(r"ws/game/tournament/(?P<channel_id>\w+)/$", tournament_consumers.TournamentConsumer.as_asgi()),
]
