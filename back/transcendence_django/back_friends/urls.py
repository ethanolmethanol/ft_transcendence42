from django.urls import path

from .views import (
    AcceptFriendshipView,
    AddFriendView,
    DeclineFriendshipView,
    RemoveFriendView,
    get_friends_info,
)

urlpatterns = [
    path("add_friend/", AddFriendView.as_view(), name="add_friend"),
    path("remove_friend/", RemoveFriendView.as_view(), name="remove_friend"),
    path("accept_friendship/", AcceptFriendshipView.as_view(), name="accept_friendship"),
    path("decline_friendship/", DeclineFriendshipView.as_view(), name="decline_friendship"),
    path("get_friends_info/", get_friends_info, name="get_friends_info"),
]
