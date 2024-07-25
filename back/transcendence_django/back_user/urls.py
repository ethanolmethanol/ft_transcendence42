from django.urls import path

from .views import UserDataView

urlpatterns = [
    path("user_data/", UserDataView.as_view(), name="user_data"),
]
