# pylint: disable=no-member
from http import HTTPStatus
from typing import Any, Dict

from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework.response import Response
from rest_framework.views import APIView
from typing import Union

from .constants import DEFAULT_COLORS, DEFAULT_SETTINGS
from .models import Profile


@method_decorator(csrf_protect, name="dispatch")
class UserDataView(APIView):

    def get_user_id(self, request: Any) -> int:
        return request.session.get("_auth_user_id")

    def findUserById(self, request: Any) -> Union[Response, User]:
        user_id = self.get_user_id(request)
        if user_id is None:
            return self._respond_with_unauthorized()

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return self._respond_with_bad_request()

        return user

    def get(self, request: Any) -> Response:
        result = self.findUserById(request)

        if isinstance(result, Response):
            return result
        
        user, user_id = result, self.get_user_id(request)

        return self._handle_get_request(user, user_id)

    def post(self, request: Any) -> Response:
        result = self.findUserById(request)

        if isinstance(result, Response):
            return result
        
        user = result
        return self._handle_post_request(user, request.data)

    def _respond_with_unauthorized(self) -> Response:
        return Response(
            {"detail": "User isn't logged in."}, status=HTTPStatus.UNAUTHORIZED
        )

    def _respond_with_bad_request(self) -> Response:
        return Response(
            {"detail": "User does not exist."}, status=HTTPStatus.BAD_REQUEST
        )

    def _handle_get_request(self, user: User, user_id: int) -> Response:
        profile, _ = Profile.objects.get_or_create(
            user=user,
            defaults={
                "color_config": DEFAULT_COLORS,
                "game_settings": DEFAULT_SETTINGS,
            },
        )
        user_data = {
            "id": user_id,
            "username": user.username,
            "email": user.email,
            "color_config": profile.color_config,
            "game_settings": profile.game_settings,
        }
        return Response(user_data, status=HTTPStatus.OK)

    def _validate_list_of_type(self, lst, item_type):
        return isinstance(lst, list) and all(
            isinstance(item, item_type) for item in lst
        )

    def _get_validated_config(self, data, key, default, item_type):
        raw_config = data.get(key)
        if self._validate_list_of_type(raw_config, item_type):
            return raw_config
        return default

    def _update_profile(
        self, user: User, color_config: list[str], game_settings: list[int]
    ):
        profile, _ = Profile.objects.get_or_create(user=user)
        profile.color_config = color_config
        profile.game_settings = game_settings
        profile.save()

    def _handle_post_request(self, user: User, data: Dict[str, Any]) -> Response:
        new_color_config = self._get_validated_config(
            data, "color_config", DEFAULT_COLORS, str
        )
        new_game_settings = self._get_validated_config(
            data, "game_settings", DEFAULT_SETTINGS, int
        )
        self._update_profile(user, new_color_config, new_game_settings)
        return Response({"status": "success"}, status=HTTPStatus.OK)
