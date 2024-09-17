from django.urls import path

from .views import (
    UpdateUsernameView,
    UserDataView,
    get_game_summaries,
    get_game_status,
    update_avatar,
    update_status,
)

urlpatterns = [
    path("get_game_summaries/", get_game_summaries, name="get_game_summaries"),
    path("user_data/", UserDataView.as_view(), name="user_data"),
    path("user_data/<int:pk>/", UserDataView.as_view(), name="user_data"),
    path("update_username/", UpdateUsernameView.as_view(), name="update_username"),
    path("update_avatar/", update_avatar, name="update_avatar"),
    path("update_status/", update_status, name="update_status"),
    path("get_game_status/", get_game_status, name="get_game_status"),
]
