import random
import string

from typing import Any

from back_game.game_arena.arena import Arena
from back_game.game_arena.game import GameStatus
from back_game.game_settings.game_constants import WAITING

class Channel:
    def __init__(self, arenas: dict[int, Arena], is_tournament: bool = False):
        self.id: str = self.__generate_random_id(10)
        self.arenas = arenas
        self.users = {}
        self.is_tournament = is_tournament

    def to_dict(self) -> dict[str, Any]:
        return {
            "channel_id": self.id,
            "arenas": [arena.to_dict() for arena in self.arenas.values()],
        }

    def get_available_arena(self) -> Arena | None:
        for arena in self.arenas.values():
            if not arena.is_private() and arena.get_status() == GameStatus(WAITING):
                return arena
        return None

    def get_arena_from_user_id(self, user_id: int) -> Arena | None:
        return self.users.get(user_id)

    def get_arena(self, arena_id: int) -> Arena | None:
        return self.arenas.get(arena_id)

    def add_arena(self, arena: Arena):
        self.arenas[arena.id] = arena

    def add_user_into_arena(self, user_id: int, arena_id: str):
        arena: Arena = self.arenas[arena_id]
        self.users[user_id] = arena

    def delete_arena(self, arena_id: str):
        if arena_id in self.arenas:
            del self.arenas[arena_id]

    def is_empty(self) -> bool:
        return not bool(self.arenas)

    def __generate_random_id(self, length: int) -> str:
        letters_and_digits = string.ascii_letters + string.digits
        return "".join(random.choice(letters_and_digits) for _ in range(length))
