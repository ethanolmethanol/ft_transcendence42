from django.urls import path

from .views import username_view

urlpatterns = [
    path("username/", username_view, name="username"),
]
