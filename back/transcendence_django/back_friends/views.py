import json
import logging
from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
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


@require_http_methods(["POST"])
@csrf_protect
@login_required
def add_friend(request):
    try:
        data = json.loads(request.body)
        friend_name = data.get("friendName")
        if friend_name == "":
            return JsonResponse(
                {"status": "Please enter a friend name."}, status=HTTPStatus.BAD_REQUEST
            )
        user = CustomUser.objects.get(pk=request.user.id)
        friend = CustomUser.objects.get(username=friend_name)
        request_status = user.send_friend_request(friend)
        return JsonResponse({"status": request_status}, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return JsonResponse(
            {"error": "User does not exist."}, status=HTTPStatus.NOT_FOUND
        )
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON data."}, status=HTTPStatus.BAD_REQUEST
        )


@require_http_methods(["POST"])
@csrf_protect
@login_required
def remove_friend(request):
    try:
        data = json.loads(request.body)
        friend_name = data.get("friendName")
        user = CustomUser.objects.get(pk=request.user.id)
        friend = CustomUser.objects.get(username=friend_name)
        if user.remove_friend(friend):
            return JsonResponse(
                {"status": "Successfully removed %s from friends" % friend.username},
                status=status.HTTP_200_OK,
            )
        else:
            return JsonResponse(
                {"error": "Friend does not exist."}, status=HTTPStatus.NOT_FOUND,
            )
    except CustomUser.DoesNotExist:
        return JsonResponse(
            {"error": "User does not exist."},
            status=HTTPStatus.NOT_FOUND,
        )
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON data."}, status=HTTPStatus.BAD_REQUEST
        )


@require_http_methods(["POST"])
@csrf_protect
@login_required
def accept_friendship(request):
    try:
        data = json.loads(request.body)
        friend_name = data.get("friendName")
        user = CustomUser.objects.get(pk=request.user.id)
        friend = CustomUser.objects.get(username=friend_name)
        if user.accept_friendship_request(friend) is not None:
            return JsonResponse(
                {"status": "%s is now your friend!" % friend.username},
                status=status.HTTP_200_OK,
            )
        else:
            return JsonResponse(
                {"error": "Friend request does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except CustomUser.DoesNotExist:
        return JsonResponse(
            {"error": "User does not exist."}, status=HTTPStatus.NOT_FOUND
        )
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON data."}, status=HTTPStatus.BAD_REQUEST
        )


@require_http_methods(["POST"])
@csrf_protect
@login_required
def decline_friendship(request):
    try:
        data = json.loads(request.body)
        friend_name = data.get("friendName")
        user = CustomUser.objects.get(pk=request.user.id)
        friend = CustomUser.objects.get(username=friend_name)
        if user.decline_friendship_request(friend) is not None:
            return JsonResponse(
                {"status": "Friendship request from %s declined" % friend.username},
                status=status.HTTP_200_OK,
            )
        else:
            return JsonResponse(
                {"error": "Friend request does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except CustomUser.DoesNotExist:
        return JsonResponse(
            {"error": "User does not exist."}, status=HTTPStatus.NOT_FOUND
        )
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON data."}, status=HTTPStatus.BAD_REQUEST
        )


@require_http_methods(["GET"])
@csrf_protect
@login_required
def get_friends_info(request):
    #  send this request every 5 s (if user on the friend page)
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
                OFFLINE_KEY: offline_friends
            },
            status=status.HTTP_200_OK),
    except CustomUser.DoesNotExist:
        return JsonResponse(
            {"error": "User does not exist."}, status=HTTPStatus.NOT_FOUND
        )
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON data."}, status=HTTPStatus.BAD_REQUEST
        )
