from django.urls import path
from .views import get_channelID

urlpatterns = [
    path('get_channel_id/', get_channelID, name='get_channelID'),
]
