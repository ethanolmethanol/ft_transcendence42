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
from .constants import (
    API_GAME_SOCKET,
    API_USER_ENDPOINT,
    UID_RNG_BEGIN,
    UID_RNG_END,
    UID_RNG_STEP,
)

logger = logging.getLogger(__name__)


class AipiView(APIView):

    bots: dict[int, AipiClient] = {}
    coli_rng_offset: int = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
                cert=("/etc/ssl/public.crt", "/etc/ssl/private.key"),
                timeout=3,
            )
            status: str = (
                "already taken"
                if user_response.status_code == HTTPStatus.OK
                else "free to use"
            )
            logger.info("%s: User id is %s", uid, status)
            return user_response.status_code == HTTPStatus.NOT_FOUND

        uid: int = random.randint(UID_RNG_BEGIN, UID_RNG_END)

        # collisions with ai or real user ids
        while self.bots.get(uid) is not None or not __user_id_collision_check(uid):
            uid = random.randint(
                UID_RNG_BEGIN + self.coli_rng_offset, UID_RNG_END + self.coli_rng_offset
            )
            self.coli_rng_offset += UID_RNG_STEP

        return uid
