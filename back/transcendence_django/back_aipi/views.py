# pylint: disable=no-member
from http import HTTPStatus
from typing import Any, Dict, Union
import asyncio
import json
import threading
import random
from datetime import datetime
now = datetime.now

# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_protect
from rest_framework.response import Response
from rest_framework.views import APIView
from .client import AipiClient
import logging

logger = logging.getLogger(__name__)

API_GAME_SOCKET = 'wss://back-game';

# @method_decorator(csrf_protect, name="dispatch")
class AipiView(APIView):

    bots: dict[int: AipiClient] = {}

    def get(self, request) -> Response:

        data: dict[str: Any] = json.loads(request.body.decode("utf-8"))

        channel_id: str = data["channel_id"]

        self.arena_id: str = data["arena_id"]

        logger.info(f"AIPI got request for channel id {channel_id}")

        self.wss_address: str = f"{API_GAME_SOCKET}/ws/game/{channel_id}/"

        self.ai_user_id: int = random.randint(1000, 10000)

        while self.bots.get(self.ai_user_id) is not None: # collisions
            self.ai_user_id: int = random.randint(1000, 10000)

        # check for collisions with user ids 
        try:
            self.bots[self.ai_user_id] = AipiClient(self.wss_address, self.ai_user_id, self.arena_id)
            logger.info(f"Starting thread at {now()}")
            t = threading.Thread(target=self.run_async_loop_in_thread)
            t.setDaemon(True)
            t.start()
            return Response({"user_id": self.ai_user_id}, status=HTTPStatus.OK)
        except (TypeError, KeyError, ValueError) as e:
            logger.error(e)
            return Response({"error": str(e)}, status=HTTPStatus.BAD_REQUEST)

    def run_async_loop_in_thread(self):
        asyncio.run(self.bots[self.ai_user_id].run())
