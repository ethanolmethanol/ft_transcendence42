from django.urls import path

from .views import is_logged_view, logout_view, signin, signup, oauth2, get_authorize_url, exchange_code_for_user_id, set_username

urlpatterns = [
    path("signin/", signin, name="signin"),
    path("signup/", signup, name="signup"),
    path("logout/", logout_view, name="logout"),
    path("is_logged/", is_logged_view, name="is_logged"),
    path("authorize/", get_authorize_url, name="authorize"),
    path("exchange_code_for_user_id/", exchange_code_for_user_id, name="exchange_code_for_user_id"),
    path("set_username/", set_username, name="set_username"),
    path("o/", oauth2, name="oauth2"),
]
