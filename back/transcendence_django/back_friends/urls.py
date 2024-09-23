from django.urls import path

from .views import (
    AcceptView,
    AddView,
    DeclineView,
    RemoveView,
    get_friends_info,
)

urlpatterns = [
    path("add_friend/", AddView.as_view(), name="add_friend"),
    path("remove_friend/", RemoveView.as_view(), name="remove_friend"),
    path("accept_friendship/", AcceptView.as_view(), name="accept_friendship"),
    path("decline_friendship/", DeclineView.as_view(), name="decline_friendship"),
    path("get_friends_info/", get_friends_info, name="get_friends_info"),
]
