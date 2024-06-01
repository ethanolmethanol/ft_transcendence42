from django.urls import path

from .views import user_data_view

urlpatterns = [
    path("user_data/", user_data_view, name="user_data_view"),
]
