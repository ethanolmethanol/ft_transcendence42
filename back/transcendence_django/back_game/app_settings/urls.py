from django.urls import path
from .views import getChannelID

urlpatterns = [
    path("get_channel_id/", getChannelID, name="getChannelID"),
]
