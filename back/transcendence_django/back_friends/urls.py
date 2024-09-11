from django.urls import path

from .views import (
    accept_friendship,
    add_friend,
    decline_friendship,
    get_friends_info,
    remove_friend,
)

urlpatterns = [
    path("add_friend/", add_friend, name="add_friend"),
    path("remove_friend/", remove_friend, name="remove_friend"),
    path("accept_friendship/", accept_friendship, name="accept_friendship"),
    path("decline_friendship/", decline_friendship, name="decline_friendship"),
    path("get_friends_info/", get_friends_info, name="get_friends_info"),
]
