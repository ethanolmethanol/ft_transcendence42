# pylint: disable=no-member
from http import HTTPStatus
from typing import Any, Dict

from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework.response import Response
from rest_framework.views import APIView

from .constants import DEFAULT_COLORS
from .models import Profile


@method_decorator(csrf_protect, name="dispatch")
class UserDataView(APIView):

    def get_user_id(self, request: Any) -> int:
        return request.session.get("_auth_user_id")

    def get(self, request: Any) -> Response:
        user_id = self.get_user_id(request)
        if user_id is None:
            return self._respond_with_unauthorized()

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return self._respond_with_bad_request()

        return self._handle_get_request(user, user_id)

    def post(self, request: Any) -> Response:
        user_id = self.get_user_id(request)
        if user_id is None:
            return self._respond_with_unauthorized()

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return self._respond_with_bad_request()

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
            user=user, defaults={"color_config": DEFAULT_COLORS}
        )
        user_data = {
            "id": user_id,
            "username": user.username,
            "email": user.email,
            "color_config": profile.color_config,
        }
        return Response(user_data, status=HTTPStatus.OK)

    def _handle_post_request(self, user: User, data: Dict[str, Any]) -> Response:
        new_color_config = data.get("color_config")
        profile, _ = Profile.objects.get_or_create(user=user)
        profile.color_config = new_color_config
        profile.save()
        return Response({"status": "success"}, status=HTTPStatus.OK)
