from django.urls import path

from .views import is_logged_view, logout_view, signin, signup

urlpatterns = [
    path("signin/", signin, name="signin"),
    path("signup/", signup, name="signup"),
    path("logout/", logout_view, name="logout"),
    path("is_logged/", is_logged_view, name="is_logged"),
]
