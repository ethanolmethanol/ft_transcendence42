from back_game.app_settings.views import (
    create_lobby,
    is_user_in_lobby,
    join_lobby,
    join_specific_lobby,
    join_tournament,
)
from django.urls import path

urlpatterns = [
    path("create_lobby/", create_lobby, name="create_lobby"),
    path("join_lobby/", join_lobby, name="join_lobby"),
    path("join_specific_lobby/", join_specific_lobby, name="join_specific_lobby"),
    path("join_tournament/", join_tournament, name="join_tournament"),
    path("is_user_in_lobby/", is_user_in_lobby, name="is_user_in_lobby"),
]
