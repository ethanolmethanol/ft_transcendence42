from django.urls import path

from .views import (
    exchange_code_for_user_id,
    get_authorize_url,
    is_logged_view,
    logout_view,
    set_username_42,
    signin,
    signup,
)

urlpatterns = [
    path("signin/", signin, name="signin"),
    path("signup/", signup, name="signup"),
    path("logout/", logout_view, name="logout"),
    path("is_logged/", is_logged_view, name="is_logged"),
    path("authorize/", get_authorize_url, name="authorize"),
    path(
        "exchange_code_for_user_id/",
        exchange_code_for_user_id,
        name="exchange_code_for_user_id"
    ),
    path("set_username_42/", set_username_42, name="set_username_42"),
]
