# pylint: disable=no-member
import asyncio
import json
import logging
import random
import threading
from http import HTTPStatus
from typing import Any

from requests import Response as HTTPResponse
from requests import get as http_get
from rest_framework.response import Response
from rest_framework.views import APIView
from transcendence_django.dict_keys import ARENA_ID, CHANNEL_ID, ERROR, USER_ID

from .client import AipiClient

logger = logging.getLogger(__name__)

API_GAME_SOCKET = "wss://back-game"

API_USER_ENDPOINT = "https://back-user/user/user-data"


class AipiView(APIView):

    bots: dict[int, AipiClient] = {}

    def __init__(self) -> None:
        super.__init__()
        self.arena_id: str = ""
        self.wss_address: str = ""
        self.ai_user_id: int = -1

    def get(self, request) -> Response:

        data: dict[str, Any] = json.loads(request.body.decode("utf-8"))

        channel_id: str = data[CHANNEL_ID]

        self.arena_id = data[ARENA_ID]

        logger.info("AIPI got request for channel id %s", channel_id)

        self.wss_address = f"{API_GAME_SOCKET}/ws/game/{channel_id}/"

        self.ai_user_id = self.__new_ai_uid()

        try:
            self.bots[self.ai_user_id] = AipiClient(
                self.wss_address, self.ai_user_id, self.arena_id
            )
            t = threading.Thread(target=self.run_async_loop_in_thread)
            t.daemon = True
            t.start()
            return Response({USER_ID: self.ai_user_id}, status=HTTPStatus.OK)
        except (TypeError, KeyError, ValueError) as e:
            logger.error(e)
            return Response({ERROR: str(e)}, status=HTTPStatus.BAD_REQUEST)

    def run_async_loop_in_thread(self):
        asyncio.run(self.bots[self.ai_user_id].run())

    def __new_ai_uid(self) -> int:
        def __user_id_collision_check(uid: int) -> bool:
            user_response: HTTPResponse = http_get(
                url=f"{API_USER_ENDPOINT}/{uid}/",
                verify=False,  # does not work otherwise
                cert=("/etc/ssl/serv.crt", "/etc/ssl/serv.key"),
                timeout=3,
            )
            status: str = (
                "already taken" if user_response.status_code == 200 else "free to use"
            )
            logger.info("%s: User id is %s", uid, status)
            return user_response.status_code == 404

        uid: int = random.randint(1000, 10000)

        # collisions with ai or real user ids
        while self.bots.get(uid) is not None or not __user_id_collision_check(uid):
            uid = random.randint(1000, 10000)

        return uid
