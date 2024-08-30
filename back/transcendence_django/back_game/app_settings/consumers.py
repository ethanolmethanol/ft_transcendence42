from back_game.app_settings.base_consumer import BaseConsumer
from back_game.app_settings.game_logic_interface import GameLogicInterface
from transcendence_django.dict_keys import ASSIGNATIONS
from typing import Any
import logging

logger = logging.getLogger(__name__)

class ClassicConsumer(BaseConsumer):

    def get_game_logic_interface(self):
        return GameLogicInterface(is_tournament=False)


class TournamentConsumer(BaseConsumer):

    def get_game_logic_interface(self):
        return GameLogicInterface(is_tournament=True)

    async def add_user_to_channel_group(self):
        await super().add_user_to_channel_group()
        self.game.channel.assignation_sender = self.send_assignations

#     async def join(self, message):
#         await super().join(message)
#         if self.game.arena_id is None:
#             if self.game.is_ready_to_start():
#                 asyncio.create_task(self.send_assignations_with_delay())

#     async def send_assignations_with_delay(self):
#         await asyncio.sleep(2)
#         await self.send_assignations()

    async def send_assignations(self):
        logger.info("Sending assignations")
        assignations: dict[str, Any] = self.game.get_assignations()
        await self.send_update({ASSIGNATIONS: assignations})
