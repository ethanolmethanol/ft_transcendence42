from back_game.app_settings.base_consumer import BaseConsumer
from back_game.app_settings.game_logic_interface import GameLogicInterface
from transcendence_django.dict_keys import ASSIGNATIONS, TOURNAMENT_MAP
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
        self.game.channel.assignations_sender = self.send_assignations
        self.game.channel.tournament_map_sender = self.send_tournament_map

    async def send_players(self):
        await super().send_players()
        await self.send_tournament_map()

    async def send_assignations(self, assignations: dict[str, Any]):
        await self.send_update(assignations)

    async def send_tournament_map(self):
        tournament_map = self.game.get_tournament_map()
        await self.send_update({TOURNAMENT_MAP: tournament_map})

