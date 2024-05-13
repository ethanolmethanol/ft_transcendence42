from django.urls import path
from .views import get_channel_id

urlpatterns = [
    path("get_channel_id/", get_channel_id, name="get_channel_id"),
]
