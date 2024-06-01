from back_game.app_settings.views import get_channel_id
from django.urls import path

urlpatterns = [
    path("get_channel_id/", get_channel_id, name="get_channel_id"),
]
