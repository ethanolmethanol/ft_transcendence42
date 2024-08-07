import asyncio
import logging
from typing import Any, Callable, Coroutine, Optional

from back_game.game_arena.arena import Arena
from back_game.game_arena.game import GameStatus
from back_game.game_settings.game_constants import (
    DYING,
    MONITOR_LOOP_INTERVAL,
    OVER,
    RUN_LOOP_INTERVAL,
    STARTED,
    TIMEOUT_GAME_OVER,
    TIMEOUT_INTERVAL,
    WAITING,
)
from back_game.monitor.channel_manager import ChannelManager
from back_game.monitor.history_manager import HistoryManager
from django.apps import apps
from django.conf import settings
from transcendence_django.dict_keys import (
    ARENA,
    CHANNEL_ID,
    OVER_CALLBACK,
    START_TIME,
    START_TIMER_CALLBACK,
    UPDATE_CALLBACK,
)

logger = logging.getLogger(__name__)


class Monitor:
    MONITOR_INSTANCE = None

    def __init__(self):
        if not apps.ready:
            apps.populate(settings.INSTALLED_APPS)
        self.game_summary = apps.get_model("shared_models", "GameSummary")
        self.history_manager = HistoryManager()
        self.channel_manager = ChannelManager()

    async def create_new_channel(
        self, user_id: int, players_specs: dict[str, int]
    ) -> dict[str, Any]:
        new_channel = await self.channel_manager.create_new_channel(
            user_id, players_specs
        )
        channel_id: str = new_channel[CHANNEL_ID]
        arenas = self.channel_manager.channels[channel_id]
        asyncio.create_task(self.__monitor_arenas_loop(channel_id, arenas))
        asyncio.create_task(self.__run_game_loop(arenas))
        return new_channel

    async def join_channel(
        self, user_id: int, channel_id: str
    ) -> dict[str, Any] | None:
        return await self.channel_manager.join_channel(user_id, channel_id)

    def join_already_created_channel(
        self, user_id: int, is_remote: bool
    ) -> dict[str, Any] | None:
        return self.channel_manager.join_already_created_channel(user_id, is_remote)

    def get_arena(self, channel_id: str, arena_id: str) -> Arena:
        arena: Arena | None = self.channel_manager.get_arena(channel_id, arena_id)
        if arena is None:
            raise KeyError("Arena not found")
        return arena

    def does_exist_channel(self, channel_id: str) -> bool:
        return self.channel_manager.channels.get(channel_id) is not None

    def is_user_in_channel(self, user_id: int) -> bool:
        return self.channel_manager.get_channel_from_user_id(user_id) is not None

    def add_user_to_channel(self, user_id: int, channel_id: str, arena_id: str):
        self.channel_manager.add_user_to_channel(user_id, channel_id, arena_id)

    def init_arena(
        self,
        channel_id: str,
        arena_id: str,
        callbacks: dict[str, Optional[Callable[[Any], Coroutine[Any, Any, None]]]],
    ):
        logger.info("User table: %s", self.channel_manager.user_game_table)
        arena: Arena = self.get_arena(channel_id, arena_id)
        arena.game_update_callback = callbacks[UPDATE_CALLBACK]
        arena.game_over_callback = callbacks[OVER_CALLBACK]
        arena.start_timer_callback = callbacks[START_TIMER_CALLBACK]

    def join_arena(
        self, user_id: int, player_name: str, channel_id: str, arena_id: str
    ):
        if self.is_user_active_in_game(user_id, channel_id, arena_id):
            raise ValueError("User already in another arena")
        arena: Arena = self.get_arena(channel_id, arena_id)
        arena.enter_arena(user_id, player_name)
        self.add_user_to_channel(user_id, channel_id, arena_id)

    def give_up(self, user_id: int, channel_id: str, arena_id: str):
        arena: Arena = self.get_arena(channel_id, arena_id)
        arena.player_gave_up(user_id)
        self.channel_manager.delete_user(user_id, arena_id)

    def rematch(self, user_id: int, channel_id: str, arena_id: str):
        arena: Arena = self.get_arena(channel_id, arena_id)
        arena.rematch(user_id)

    def get_game_summary(self, channel_id: str, arena_id: str) -> dict[str, Any]:
        arena: Arena = self.get_arena(channel_id, arena_id)
        summary: dict[str, Any] = arena.get_game_summary()
        return summary

    def move_paddle(
        self,
        channel_id: str,
        arena_id: str,
        player_name: str,
        direction: int,
    ) -> dict[str, Any]:
        arena: Arena = self.get_arena(channel_id, arena_id)
        return arena.move_paddle(player_name, direction)

    def leave_arena(self, user_id: int, channel_id: str, arena_id: str):
        self.channel_manager.leave_arena(user_id, channel_id, arena_id)

    def is_user_active_in_game(
        self, user_id: int, channel_id: str, arena_id: str
    ) -> bool:
        return self.channel_manager.is_user_active_in_game(
            user_id, channel_id, arena_id
        )

    async def save_game_summary(
        self,
        summary: dict[str, Any],
    ):
        if summary[START_TIME] is not None:
            await self.history_manager.save_game_summary(summary)

    async def update_game_states(self, arenas: dict[str, Arena]):
        for arena in arenas.values():
            arena_status = arena.get_status()
            if arena.can_be_started():
                await arena.start_game()
            elif arena.can_be_over():
                arena.conclude_game()
                summary = arena.get_game_summary()
                await self.save_game_summary(summary)
                if arena_status != GameStatus(STARTED):
                    self.channel_manager.delete_arena(arenas, arena.id)
                    break
            elif arena_status == GameStatus(OVER):
                logger.info("Game over in arena %s", arena.id)
                await self.__game_over(arenas, arena)
                break

    async def __monitor_arenas_loop(self, channel_id: str, arenas: dict[str, Arena]):
        while arenas:
            await self.update_game_states(arenas)
            await asyncio.sleep(MONITOR_LOOP_INTERVAL)
        self.channel_manager.delete_channel(channel_id)

    async def __run_game_loop(self, arenas: dict[str, Arena]):
        while arenas:
            for arena in arenas.values():
                if arena.get_status() == GameStatus(STARTED):
                    update_message = arena.update_game()
                    if arena.game_update_callback is not None:
                        await arena.game_update_callback(update_message)
            await asyncio.sleep(RUN_LOOP_INTERVAL)

    async def __game_over(self, arenas: dict[str, Arena], arena: Arena):
        arena.set_status(GameStatus(DYING))
        if arena.game_update_callback is not None:
            logger.info("Sending game over message to arena %s", arena.id)
            await arena.game_update_callback({ARENA: arena.to_dict()})
        time = TIMEOUT_GAME_OVER + 1
        while (
            arena.get_status() in [GameStatus(DYING), GameStatus(WAITING)] and time > 0
        ):
            time -= TIMEOUT_INTERVAL
            if arena.game_over_callback is not None:
                await arena.game_over_callback(time)
            if time <= 0 and arena.get_status() == GameStatus(DYING):
                self.channel_manager.delete_arena(arenas, arena.id)
            else:
                await asyncio.sleep(TIMEOUT_INTERVAL)

    @classmethod
    def get_instance(cls):
        if cls.MONITOR_INSTANCE is None:
            cls.MONITOR_INSTANCE = cls()
        return cls.MONITOR_INSTANCE


def get_monitor() -> Monitor:
    return Monitor.get_instance()
