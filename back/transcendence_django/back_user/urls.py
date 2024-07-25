from django.urls import path

from .views import UserDataView
from .views import get_game_summaries

urlpatterns = [
    path("get_game_summaries/", get_game_summaries, name="get_game_summaries"),
    path("user_data/", UserDataView.as_view(), name="user_data"),
]
