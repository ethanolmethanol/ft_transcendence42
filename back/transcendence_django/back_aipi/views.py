# pylint: disable=no-member
from http import HTTPStatus
from typing import Any, Dict, Union
import asyncio
import json
import threading
import random
from requests import get as http_get, Response, JSONDecodeError

from rest_framework.response import Response
from rest_framework.views import APIView
from .client import AipiClient
import logging
from transcendence_django.dict_keys import ( CHANNEL_ID, ARENA_ID, USER_ID, ERROR )

logger = logging.getLogger(__name__)

API_GAME_SOCKET = 'wss://back-game';

API_USER_ENDPOINT = 'https://back-user/user/user-data';

class AipiView(APIView):

    bots: dict[int: AipiClient] = {}

    def get(self, request) -> Response:

        data: dict[str: Any] = json.loads(request.body.decode("utf-8"))

        channel_id: str = data[CHANNEL_ID]

        self.arena_id: str = data[ARENA_ID]

        logger.info(f"AIPI got request for channel id {channel_id}")

        self.wss_address: str = f"{API_GAME_SOCKET}/ws/game/{channel_id}/"

        self.ai_user_id: int = self.__new_ai_uid()

        try:
            self.bots[self.ai_user_id] = AipiClient(self.wss_address, self.ai_user_id, self.arena_id)
            t = threading.Thread(target=self.run_async_loop_in_thread)
            t.setDaemon(True)
            t.start()
            return Response({USER_ID: self.ai_user_id}, status=HTTPStatus.OK)
        except (TypeError, KeyError, ValueError) as e:
            logger.error(e)
            return Response({ERROR: str(e)}, status=HTTPStatus.BAD_REQUEST)

    def run_async_loop_in_thread(self):
        asyncio.run(self.bots[self.ai_user_id].run())

    def __new_ai_uid(self) -> int:
        def __user_id_collision_check(uid: int) -> bool:
            user_response: Response = http_get(
                url = f"{API_USER_ENDPOINT}/{uid}/",
                verify = False, # does not work otherwise
                cert = ('/etc/ssl/serv.crt', '/etc/ssl/serv.key')
            )
            logger.info(f"{uid}: User id is {"already taken" if user_response.status_code == 200 else "free to use"}")
            return user_response.status_code == 404
        uid: int = random.randint(1000, 10000)

        # collisions with ai or real user ids
        while self.bots.get(uid) is not None or not __user_id_collision_check(uid):
            uid: int = random.randint(1000, 10000)

        return uid
