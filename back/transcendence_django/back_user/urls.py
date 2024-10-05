from django.urls import path

from .views import (
    UpdateUsernameView,
    UserDataView,
    get_game_summaries,
    get_username,
    is_user_playing,
    update_avatar,
    update_playing_status,
)

urlpatterns = [
    path("get_game_summaries/", get_game_summaries, name="get_game_summaries"),
    path("get_username/", get_username, name="get_username"),
    path("user_data/", UserDataView.as_view(), name="user_data"),
    path("user_data/<int:pk>/", UserDataView.as_view(), name="user_data"),
    path("update_username/", UpdateUsernameView.as_view(), name="update_username"),
    path("update_avatar/", update_avatar, name="update_avatar"),
    path("is_user_playing/", is_user_playing, name="is_user_playing"),
    path("update_playing_status/", update_playing_status, name="update_playing_status"),
]
