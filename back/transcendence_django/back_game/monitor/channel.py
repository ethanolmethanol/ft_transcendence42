import logging
import random
import string

from typing import Any

from back_game.game_arena.arena import Arena
from back_game.game_arena.game import GameStatus
from back_game.game_settings.game_constants import CREATED, WAITING


logger = logging.getLogger(__name__)


class Channel:
    def __init__(self, arenas: dict[int, Arena], is_tournament: bool = False):
        self.id: str = self.__generate_random_id(10)
        self.arenas = arenas
        self.is_tournament = is_tournament
        self.users = {}
        self.user_count = len(arenas) * 2

    def to_dict(self) -> dict[str, Any]:
        return {
            "channel_id": self.id,
            "arenas": [arena.to_dict() for arena in self.arenas.values()],
        }

    def get_available_arena(self) -> Arena | None:
        if self.is_full():
            return None
        for arena in self.arenas.values():
            if not arena.is_private() and arena.get_status() in [GameStatus(CREATED), GameStatus(WAITING)]:
                if self.is_arena_available(arena):
                    return arena
        return None

    def is_arena_available(self, arena: Arena) -> bool:
        user_count_in_arena = sum(1 for user_arena in self.users.values() if user_arena == arena)
        return user_count_in_arena < arena.player_manager.nb_players

    def get_arena_from_user_id(self, user_id: int) -> Arena | None:
        return self.users.get(user_id)

    def get_arena(self, arena_id: int) -> Arena | None:
        return self.arenas.get(arena_id)

    def add_arena(self, arena: Arena):
        self.arenas[arena.id] = arena

    def add_user_into_arena(self, user_id: int, arena_id: str):
        if len(self.users) < self.user_count:
            arena: Arena = self.arenas[arena_id]
            self.users[user_id] = arena
            logger.info("User %s added to channel %s", user_id, self.id)
            if self.is_full():
                logger.info("Channel %s is full!", self.id)
        else:
            logger.error("%s cannot be added in the arena %s: Channel %s is full!", user_id, arena_id, self.id)

    def get_assignations(self) -> dict[str, Any]:
        assignations = {}
        for user_id, arena in self.users.items():
            assignations[user_id] = arena.id
        return assignations

    def delete_user_from_arena(self, user_id: int):
        if user_id in self.users:
            del self.users[user_id]

    def delete_arena(self, arena_id: str):
        if arena_id in self.arenas:
            del self.arenas[arena_id]

    def is_empty(self) -> bool:
        return not bool(self.arenas)

    def is_full(self) -> bool:
        return len(self.users) == self.user_count

    def __generate_random_id(self, length: int) -> str:
        letters_and_digits = string.ascii_letters + string.digits
        return "".join(random.choice(letters_and_digits) for _ in range(length))
