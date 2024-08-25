from abc import ABC, abstractmethod
import logging
import random
import string
from typing import Any, Dict

from back_game.game_arena.arena import Arena
from back_game.game_arena.game import GameStatus
from back_game.game_settings.game_constants import CREATED, WAITING, DEAD

logger = logging.getLogger(__name__)

class Channel(ABC):

    def __init__(self, players_specs: dict[str, int]):
        self.id: str = self._generate_random_id(10)
        self.users: Dict[int, Arena] = {}
        self.arenas: Dict[str, Arena] = {}
        self.user_count = 0

    @abstractmethod
    def is_tournament(self) -> bool:
        pass

    def to_dict(self) -> Dict[str, Any]:
        return {
            "channel_id": self.id,
            "arenas": [arena.to_dict() for arena in self.arenas.values()],
            "is_tournament": self.is_tournament(),
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

    def get_assignations(self) -> Dict[str, Any]:
        assignations = {}
        for user_id, arena in self.users.items():
            assignations[user_id] = arena.id
        return assignations

    def count_non_dead_arenas(self) -> int:
        return sum(1 for arena in self.arenas.values() if not arena.get_status() == GameStatus(DEAD))

    def delete_user(self, user_id: int):
        if user_id in self.users:
            del self.users[user_id]

    def is_empty(self) -> bool:
        return not bool(self.arenas)

    def is_full(self) -> bool:
        return len(self.users) == self.user_count

    def _generate_random_id(self, length: int) -> str:
        letters_and_digits = string.ascii_letters + string.digits
        return "".join(random.choice(letters_and_digits) for _ in range(length))