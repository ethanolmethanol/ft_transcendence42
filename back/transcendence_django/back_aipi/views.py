# pylint: disable=no-member
from http import HTTPStatus
from typing import Any, Dict, Union

# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_protect
from rest_framework.response import Response
from rest_framework.views import APIView
from .client import client
import logging

logger = logging.getLogger(__name__)

from os import getenv

SERV_IP = getenv("SERV_IP", "")
API_GAME = f'https://{SERV_IP}:8001/game';
API_GAME_SOCKET = f'wss://{SERV_IP}:8001';


# @method_decorator(csrf_protect, name="dispatch")
class AipiView(APIView):

    def get(self, request) -> Response:

        channel_id = request.session.get("channel_id")

        wss_address = f"{API_GAME_SOCKET}/ws/game/{channel_id}/"

        ai_user_id = 0

        # check for collisions with user ids 
        try:
            client(wss_address)
            return Response({"user_id": ai_user_id}, status=HTTPStatus.OK)
        except (TypeError, KeyError, ValueError) as e:
            logger.error(e)
            return Response({"error": str(e)}, status=HTTPStatus.BAD_REQUEST)
