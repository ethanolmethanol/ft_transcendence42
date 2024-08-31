from back_game.app_settings.base_consumer import BaseConsumer
from back_game.app_settings.game_logic_interface import GameLogicInterface
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
        self.game.channel.sender = self.send_update

