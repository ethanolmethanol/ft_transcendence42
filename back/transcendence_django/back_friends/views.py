import json
import logging
from http import HTTPStatus
from typing import Optional

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from rest_framework import status
from shared_models.models import CustomUser
from transcendence_django.dict_keys import (
    FRIENDS_REQUESTS_KEY,
    OFFLINE_KEY,
    ONLINE_KEY,
    PLAYING_KEY,
)

# pylint: disable=no-member

logger = logging.getLogger(__name__)


@method_decorator(
    [require_http_methods(["POST"]), csrf_protect, login_required], name="dispatch"
)
class FriendshipView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user: Optional[CustomUser] = None
        self.friend: Optional[CustomUser] = None

    def dispatch(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            friend_name = data["friendName"]
            self.user = CustomUser.objects.get(pk=request.user.id)
            self.friend = CustomUser.objects.get(username=friend_name)
        except CustomUser.DoesNotExist:
            return JsonResponse(
                {"error": "User does not exist."}, status=HTTPStatus.NOT_FOUND
            )
        except json.JSONDecodeError:
            return JsonResponse(
                {"error": "Invalid JSON data."}, status=HTTPStatus.BAD_REQUEST
            )
        except KeyError:
            return JsonResponse(
                {"error": "Friend name must be provided."},
                status=HTTPStatus.BAD_REQUEST,
            )
        return super().dispatch(request, *args, **kwargs)


class AddView(FriendshipView):
    def post(self, _request, *_args, **_kwargs):  # Unused parameters prefixed with '_'
        assert self.user is not None, "User should have been initialized in dispatch"
        assert (
            self.friend is not None
        ), "Friend should have been initialized in dispatch"
        request_status = self.user.send_friend_request(self.friend)
        return JsonResponse(
            {"status": request_status},
            status=HTTPStatus.OK,
        )


class RemoveView(FriendshipView):
    def post(self, _request, *_args, **_kwargs):
        assert self.user is not None, "User should have been initialized in dispatch"
        assert self.friend is not None, "Friend should have been initialized in dispatch"
        if self.user.remove_friend(self.friend):
            return JsonResponse(
                {"status": f"Successfully removed {self.friend.username} from friends"},
                status=HTTPStatus.OK,
            )
        return JsonResponse(
            {"error": "Friend does not exist."}, status=HTTPStatus.NOT_FOUND
        )


class AcceptView(FriendshipView):
    def post(self, _request, *_args, **_kwargs):
        assert self.user is not None, "User should have been initialized in dispatch"
        assert (
                   self.friend is not None
        ), "Friend should have been initialized in dispatch"
        if self.user.accept_friendship_request(self.friend) is not None:
            return JsonResponse(
                {"status": f"{self.friend.username} is now your friend!"},
                status=HTTPStatus.OK,
            )
        return JsonResponse(
            {"error": "Friend request does not exist."}, status=HTTPStatus.BAD_REQUEST
        )


class DeclineView(FriendshipView):
    def post(self, _request, *_args, **_kwargs):
        assert self.user is not None, "User should have been initialized in dispatch"
        assert (
                self.friend is not None
        ), "Friend should have been initialized in dispatch"
        if self.user.decline_friendship_request(self.friend) is not None:
            return JsonResponse(
                {"status": f"Friendship request from {self.friend.username} declined"},
                status=HTTPStatus.OK,
            )
        return JsonResponse(
            {"error": "Friend request does not exist."}, status=HTTPStatus.BAD_REQUEST
        )


@require_http_methods(["GET"])
@csrf_protect
@login_required
def get_friends_info(request):
    try:
        user = CustomUser.objects.get(pk=request.user.id)
        friend_requests = list(user.get_friend_requests())
        playing_friends = list(user.get_playing_friends())
        online_friends = list(user.get_online_friends())
        offline_friends = list(user.get_offline_friends())
        return JsonResponse(
            {
                FRIENDS_REQUESTS_KEY: friend_requests,
                PLAYING_KEY: playing_friends,
                ONLINE_KEY: online_friends,
                OFFLINE_KEY: offline_friends,
            },
            status=status.HTTP_200_OK,
        )
    except CustomUser.DoesNotExist:
        return JsonResponse(
            {"error": "User does not exist."}, status=HTTPStatus.NOT_FOUND
        )
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON data."}, status=HTTPStatus.BAD_REQUEST
        )
