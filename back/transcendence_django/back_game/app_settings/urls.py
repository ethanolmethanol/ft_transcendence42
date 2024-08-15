from back_game.app_settings.views import (
    create_channel,
    is_user_in_channel,
    join_channel,
    join_specific_channel,
    join_tournament,
)
from django.urls import path

urlpatterns = [
    path("create_channel/", create_channel, name="create_channel"),
    path("join_channel/", join_channel, name="join_channel"),
    path("join_specific_channel/", join_specific_channel, name="join_specific_channel"),
    path("join_tournament/", join_tournament, name="join_tournament"),
    path("is_user_in_channel/", is_user_in_channel, name="is_user_in_channel"),
]
