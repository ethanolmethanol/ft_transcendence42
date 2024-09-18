import logging
from typing import Any, Callable, Coroutine, Optional

from back_game.game_arena.arena import Arena
from back_game.monitor.channel_manager import ChannelManager
from django.apps import apps
from django.conf import settings
from transcendence_django.dict_keys import (
    OVER_CALLBACK,
    START_TIMER_CALLBACK,
    UPDATE_CALLBACK,
)

logger = logging.getLogger(__name__)


class Monitor:
    MONITOR_INSTANCE = None

    def __init__(self):
        if not apps.ready:
            apps.populate(settings.INSTALLED_APPS)
        self.channel_manager = ChannelManager()

    async def create_new_channel(
        self, user_id: int, players_specs: dict[str, int]
    ) -> dict[str, Any]:
        await self.channel_manager.create_new_channel(user_id, players_specs)
        return self.channel_manager.get_channel_dict_from_user_id(user_id)

    async def join_channel(
        self, user_id: int, channel_id: str
    ) -> dict[str, Any] | None:
        await self.channel_manager.join_channel(user_id, channel_id)
        return self.channel_manager.get_channel_dict_from_user_id(user_id)

    def join_already_created_channel(
        self, user_id: int, is_remote: bool
    ) -> dict[str, Any] | None:
        channel_dict = self.channel_manager.join_already_created_channel(
            user_id, is_remote
        )
        return channel_dict

    async def join_tournament(self, user_id: int) -> dict[str, Any] | None:
        channel_dict = await self.channel_manager.join_tournament(user_id)
        return channel_dict

    def get_arena(self, channel_id: str, arena_id: str) -> Arena:
        arena: Arena | None = self.channel_manager.get_arena(channel_id, arena_id)
        if arena is None:
            raise KeyError("Arena not found")
        return arena

    def get_arena_from_user_id(self, user_id: int) -> Arena | None:
        return self.channel_manager.get_arena_from_user_id(user_id)

    def is_user_in_channel(self, user_id: int) -> bool:
        return self.channel_manager.user_game_table.get(user_id) is not None

    async def add_user_to_channel(
        self, channel_id: str, arena_id: str | None, user_id: int
    ):
        logger.info("Adding user %s to channel %s", user_id, channel_id)
        channel = self.channel_manager.channels.get(channel_id)
        if channel:
            await self.channel_manager.add_user_to_channel(
                user_id, channel_id, arena_id
            )
        else:
            logger.error("Channel %s not found", channel_id)

    def init_arena(
        self,
        channel_id: str,
        arena_id: str,
        callbacks: dict[str, Optional[Callable[[Any], Coroutine[Any, Any, None]]]],
    ):
        arena: Arena = self.get_arena(channel_id, arena_id)
        arena.game_update_callback = callbacks[UPDATE_CALLBACK]
        arena.game_over_callback = callbacks[OVER_CALLBACK]
        arena.start_timer_callback = callbacks[START_TIMER_CALLBACK]

    async def join_arena(
        self, user_id: int, player_name: str, channel_id: str, arena_id: str
    ):
        if self.is_user_active_in_game(user_id, channel_id, arena_id):
            raise ValueError("User already in another arena")
        arena: Arena = self.get_arena(channel_id, arena_id)
        arena.enter_arena(user_id, player_name)
        await self.add_user_to_channel(channel_id, arena_id, user_id)

    def give_up(self, user_id: int, channel_id: str, arena_id: str | None):
        if arena_id is not None:
            arena: Arena = self.get_arena(channel_id, arena_id)
            arena.player_gave_up(user_id)
        self.channel_manager.delete_user_from_channel(user_id)

    def rematch(self, user_id: int, channel_id: str, arena_id: str):
        arena: Arena = self.get_arena(channel_id, arena_id)
        arena.rematch(user_id)

    def get_game_summary(self, channel_id: str, arena_id: str) -> dict[str, Any]:
        arena: Arena = self.get_arena(channel_id, arena_id)
        summary: dict[str, Any] = arena.get_game_summary()
        return summary

    def get_users_from_channel(self, channel_id: str) -> list[int]:
        return self.channel_manager.get_users_from_channel(channel_id)

    def move_paddle(
        self,
        channel_id: str,
        arena_id: str,
        player_name: str,
        direction: int,
    ) -> dict[str, Any]:
        arena: Arena = self.get_arena(channel_id, arena_id)
        return arena.move_paddle(player_name, direction)

    def leave_arena(self, user_id: int, channel_id: str, arena_id: str | None):
        if arena_id is not None:
            self.channel_manager.leave_arena(user_id, channel_id, arena_id)

    def is_user_active_in_game(
        self, user_id: int, channel_id: str, arena_id: str
    ) -> bool:
        return self.channel_manager.is_user_active_in_game(
            user_id, channel_id, arena_id
        )

    @classmethod
    def get_instance(cls):
        if cls.MONITOR_INSTANCE is None:
            cls.MONITOR_INSTANCE = cls()
        return cls.MONITOR_INSTANCE


def get_monitor() -> Monitor:
    return Monitor.get_instance()
