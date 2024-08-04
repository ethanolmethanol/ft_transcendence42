import json
import logging
from http import HTTPStatus
from json import JSONDecodeError
from typing import Any, Dict, Union

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from rest_framework.response import Response
from rest_framework.views import APIView
from shared_models.models import CustomUser, Profile
from transcendence_django.dict_keys import USER_ID

from .constants import DEFAULT_COLORS, DEFAULT_SETTINGS

# pylint: disable=no-member

logger = logging.getLogger(__name__)


@method_decorator(csrf_protect, name="dispatch")
class UserDataView(APIView):

    def get_user_id(self, request: Any) -> int:
        return request.session.get("_auth_user_id")

    def find_user_by_id(self, user_id: int) -> CustomUser:
        return get_object_or_404(CustomUser, pk=user_id)

    def get(self, request: Any, pk: int = None) -> Response:
        user_id = pk if pk is not None else self.get_user_id(request)
        if user_id is None:
            return self._respond_with_unauthorized()

        user = self.find_user_by_id(user_id)
        return self._handle_get_request(user, user_id)

    def post(self, request: Any) -> Response:
        result = self.find_user_by_id(request)
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

    def _handle_get_request(self, user: CustomUser, user_id: int) -> Response:
        profile: Profile | None = user.profile
        if profile is None:
            profile = Profile.objects.create(
                color_config=DEFAULT_COLORS,
                game_settings=DEFAULT_SETTINGS,
            )
            user.profile = profile
            user.save()
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
        self, user: CustomUser, color_config: list[str], game_settings: list[int]
    ):
        logger.info("Updating profile for user %s", user)
        profile: Profile | None = user.profile
        if profile is None:
            profile = Profile()
        logger.info("Profile: %s", profile)
        profile.color_config = color_config
        profile.game_settings = game_settings
        profile.save()
        user.profile = profile

    def _handle_post_request(self, user: CustomUser, data: Dict[str, Any]) -> Response:
        new_color_config = self._get_validated_config(
            data, "color_config", DEFAULT_COLORS, str
        )
        new_game_settings = self._get_validated_config(
            data, "game_settings", DEFAULT_SETTINGS, int
        )
        self._update_profile(user, new_color_config, new_game_settings)
        return Response({"status": "success"}, status=HTTPStatus.OK)


@require_http_methods(["POST"])
@csrf_protect
def get_game_summaries(request) -> JsonResponse:
    try:
        data = json.loads(request.body.decode("utf-8"))
        user_id = data.get(USER_ID)
        start_index = data.get("start_index", 0)
        end_index = data.get("end_index", -1)

        if not isinstance(start_index, int) or not isinstance(end_index, int):
            return JsonResponse(
                {"error": "Invalid input types. 'user_id', 'start_index', and 'end_index' must be integers."},
                status=HTTPStatus.BAD_REQUEST
            )

        user = CustomUser.objects.get(pk=user_id)
        history_size = user.history_size
        summaries = list(user.game_summaries.values())

        if start_index < 0 or end_index < 0 or start_index >= end_index:
            return JsonResponse(
                {"error": "Invalid 'start_index' or 'end_index'. Ensure 'start_index' is non-negative and less than 'end_index'."},
                status=HTTPStatus.BAD_REQUEST
            )

        has_more = end_index < history_size

        # Adjust end_index if it exceeds history_size
        if end_index > history_size:
            end_index = history_size

        # Calculate the correct indices for slicing without reversing
        actual_start_index = history_size - end_index
        actual_end_index = history_size - start_index

        sliced_summaries = summaries[actual_start_index:actual_end_index][::-1]

        history = {
            "has_more": has_more,
            "summaries": sliced_summaries
        }
        return JsonResponse(history, safe=False)
    except CustomUser.DoesNotExist:
        return JsonResponse(
            {"error": "User does not exist."},
            status=HTTPStatus.NOT_FOUND
        )
    except (JSONDecodeError, TypeError, ValueError) as e:
        return JsonResponse(
            {"error": "Invalid request data: " + str(e)},
            status=HTTPStatus.BAD_REQUEST
        )