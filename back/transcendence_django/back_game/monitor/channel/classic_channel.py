import logging

from .channel import Channel
from typing import Dict
from back_game.game_arena.arena import Arena
from back_game.game_arena.game import GameStatus
from back_game.game_settings.game_constants import DEAD

logger = logging.getLogger(__name__)


class ClassicChannel(Channel):

    def __init__(self, players_specs: dict[str, int]):
        super().__init__(players_specs)
        self.add_arena()
        self.user_count = 2

    def is_tournament(self) -> bool:
        return False

    async def add_user_into_arena(self, user_id: int, arena_id: str):
        if user_id in self.users:
            return
        if len(self.users) < self.user_count:
            arena: Arena = self.arenas[arena_id]
            self.users[user_id] = arena
            logger.info("User %s added to channel %s", user_id, self.id)
            if self.is_full():
                logger.info("Channel %s is full!", self.id)
        else:
            logger.error("%s cannot be added in the arena %s: Channel %s is full!", user_id, arena_id, self.id)

    def is_ready_to_start(self) -> bool:
        return self.is_full()

    def set_next_round(self):
        pass

    def disable(self):
        pass

    def can_round_be_set(self) -> bool:
        return False

    def can_be_deleted(self) -> bool:
        if len(self.users) == 0:
            return True
        return self.are_all_arenas_in_status_list([GameStatus(DEAD)])
