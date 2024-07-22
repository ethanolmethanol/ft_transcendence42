import json
import logging
from http import HTTPStatus
from json import JSONDecodeError

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from transcendence_django.dict_keys import USER_ID
from rest_framework.decorators import api_view
from rest_framework.response import Response
from transcendence_django.models import GameSummary


# Get an instance of a logger
logger = logging.getLogger(__name__)


@api_view(["GET"])
@csrf_protect
def user_data_view(request):
    # pylint: disable=no-member
    try:
        # Extract user ID from session data
        user_id = request.session.get("_auth_user_id")
        if user_id is None:
            return Response(
                {"detail": "User isn't logged in."}, status=HTTPStatus.UNAUTHORIZED
            )
        # Query the User model for the user with the given ID
        user = User.objects.get(pk=user_id)
        # Retrieve the user data
        user_data = {
            "id": user_id,
            "username": user.username,
            "email": user.email,
        }
        return Response(user_data, status=HTTPStatus.OK)
    except User.DoesNotExist:
        return Response({"detail": "User does not exist."}, status=HTTPStatus.NOT_FOUND)

@require_http_methods(["POST"])
@csrf_protect
def get_game_summaries(request) -> JsonResponse:
    logger.info(request.body.decode("utf-8"))
    try:
        data = json.loads(request.body.decode("utf-8"))
        user_id = str(data[USER_ID])
        summaries = GameSummary.objects.filter(players__contains=[{USER_ID: user_id}]).values()
        return JsonResponse(list(summaries), safe=False)
    except (JSONDecodeError, TypeError) as e:
        return JsonResponse({"error": "This user doesn't exist"}, status=HTTPStatus.BAD_REQUEST)
