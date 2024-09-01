import asyncio
from abc import ABC, abstractmethod
import logging
import random
import string
from typing import Any, Dict

from back_game.game_arena.arena import Arena
from back_game.game_arena.game import GameStatus
from back_game.game_settings.game_constants import (
    CREATED,
    DEAD,
    DYING,
    MONITOR_LOOP_INTERVAL,
    OVER,
    RUN_LOOP_INTERVAL,
    STARTED,
    TIMEOUT_INTERVAL,
    TIMEOUT_GAME_OVER,
    WAITING,
)
from back_game.monitor.history_manager import HistoryManager
from transcendence_django.dict_keys import ARENA, ID, START_TIME

logger = logging.getLogger(__name__)

class Channel(ABC):

    def __init__(self, players_specs: dict[str, int]):
        self.id: str = self._generate_random_id(10)
        self.history_manager = HistoryManager()
        self.users: Dict[int, Arena] = {}
        self.arenas: Dict[str, Arena] = {}
        self.user_count = 0

    @abstractmethod
    def is_tournament(self) -> bool:
        pass

    @abstractmethod
    def is_ready_to_start(self) -> bool:
        pass

    @abstractmethod
    def set_next_round(self) -> bool:
        pass

    @abstractmethod
    def can_round_be_set(self):
        pass

    @abstractmethod
    def disable(self):
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

    @abstractmethod
    async def add_user_into_arena(self, user_id: int, arena_id: str):
        pass

    def get_assignations(self) -> Dict[str, Any]:
        assignations = {}
        for user_id, arena in self.users.items():
            if arena.get_status() != GameStatus(DEAD):
                assignations[user_id] = arena.to_dict()
        return assignations

    def delete_user(self, user_id: int):
        if user_id in self.users:
            del self.users[user_id]

    def is_empty(self) -> bool:
        return not bool(self.arenas)

    def is_full(self) -> bool:
        return len(self.users) == self.user_count

    def are_all_arenas_in_status_list(self, status_list: list[GameStatus]) -> bool:
        return len(self.arenas) == sum(
            1 for arena in self.arenas.values() if arena.get_status() in status_list
            )

    async def save_game_summary(
            self,
            summary: dict[str, Any],
    ):
        if summary[START_TIME] is not None:
            await self.history_manager.save_game_summary(summary)

    async def __update_game_states(self, arena: Arena):
        arena_status = arena.get_status()
        if arena.can_be_started():
            await arena.start_game()
        elif arena.can_be_over():
            arena.conclude_game()
            summary = arena.get_game_summary()
            await self.save_game_summary(summary)
            if arena_status != GameStatus(STARTED):
                arena.set_status(GameStatus(DEAD))
        elif arena_status == GameStatus(OVER):
            await self.__game_over(arena)

    async def arena_loop(self, arena: Arena):
        while arena.get_status() != GameStatus(DEAD):
            await self.__update_game_states(arena)
            await asyncio.sleep(MONITOR_LOOP_INTERVAL)

    async def run_game_loop(self, arena: Arena):
        while arena:
            if arena.get_status() == GameStatus(STARTED):
                update_message = arena.update_game()
                await arena.send_update(update_message)
            await asyncio.sleep(RUN_LOOP_INTERVAL)

    async def __game_over(self, arena: Arena):
        logger.info("Game over in arena %s", arena.id)
        if self.is_tournament():
            arena.set_status(GameStatus(DEAD))
            await arena.send_update({ARENA: arena.to_dict()})
            return
        else:
            arena.set_status(GameStatus(DYING))
            await arena.send_update({ARENA: arena.to_dict()})
        time = TIMEOUT_GAME_OVER + 1
        while (
                arena.get_status() in [GameStatus(DYING), GameStatus(WAITING)] and time > 0
        ):
            time -= TIMEOUT_INTERVAL
            if arena.game_over_callback is not None:
                await arena.game_over_callback(time)
            if time <= 0 and arena.get_status() == GameStatus(DYING):
                arena.set_status(GameStatus(DEAD))
            else:
                await asyncio.sleep(TIMEOUT_INTERVAL)

    def _generate_random_id(self, length: int) -> str:
        letters_and_digits = string.ascii_letters + string.digits
        return "".join(random.choice(letters_and_digits) for _ in range(length))
