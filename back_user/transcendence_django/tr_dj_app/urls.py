from django.urls import path

from .views import is_logged_view, username_view

urlpatterns = [
    path("is_logged/", is_logged_view, name="is_logged"),
    path("username/", username_view, name="username"),
]
