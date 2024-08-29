import logging
from typing import Any, Callable, Coroutine, Optional

from back_game.app_settings.channel_error import ChannelError
from back_game.game_settings.game_constants import (
    INVALID_ARENA,
    INVALID_CHANNEL,
    NOT_ENTERED,
    NOT_JOINED,
    UNKNOWN_ARENA_ID,
    UNKNOWN_CHANNEL_ID,
)
from back_game.monitor.monitor import get_monitor

from back_game.monitor.channel.channel import Channel

logger = logging.getLogger(__name__)


class GameLogicInterface:
    def __init__(self, is_tournament: bool = False):
        self.channel: Channel | None = None
        self.arena_id: str | None = None
        self.user_id: int = -1
        self.has_joined: bool = False
        self.is_tournament: bool = is_tournament
        self.monitor = get_monitor()

    def init_channel(self, channel_id: str):
        logger.info("GameInterface %s: Initializing channel %s", id(self), channel_id)
        self.channel = self.monitor.channel_manager.get_channel(channel_id)
        if self.channel is None:
            raise ChannelError(INVALID_CHANNEL, UNKNOWN_CHANNEL_ID)

    async def join(
        self,
        user_id: int,
        player_name: str,
        arena_id: str | None,
        callbacks: dict[str, Optional[Callable[[Any], Coroutine[Any, Any, None]]]],
    ):
        if arena_id is not None:
            await self.__join_arena(user_id, player_name, arena_id, callbacks)
            self.arena_id = arena_id
        else:
            await self.monitor.add_user_to_channel(self.channel.id, None, user_id)
        self.user_id = user_id
        self.has_joined = True

    def leave(self):
        if not self.has_joined:
            raise ChannelError(NOT_JOINED, "Attempt to leave without joining.")
        try:
            self.monitor.leave_arena(self.user_id, self.channel.id, self.arena_id)
        except KeyError as e:
            raise ChannelError(
                NOT_ENTERED, "User cannot leave or has already left this arena."
            ) from e
        self.has_joined = False

    def give_up(self):
        if not self.has_joined:
            raise ChannelError(NOT_JOINED, "Attempt to give up without joining.")
        self.monitor.give_up(self.user_id, self.channel.id, self.arena_id)
        self.has_joined = False

    def rematch(self):
        if not self.has_joined:
            raise ChannelError(NOT_JOINED, "Attempt to rematch without joining.")
        self.monitor.rematch(self.user_id, self.channel.id, self.arena_id)

    def move_paddle(self, player_name: str, direction: int) -> dict[str, Any]:
        if not self.has_joined:
            raise ChannelError(NOT_JOINED, "Attempt to move paddle without joining.")
        try:
            return self.monitor.move_paddle(
                self.channel.id, self.arena_id, player_name, direction
            )
        except KeyError as e:
            raise ChannelError(NOT_ENTERED, "User cannot move paddle.") from e

    def is_channel_full(self) -> bool:
        return self.channel.is_full()

    def is_ready_to_start(self) -> bool:
        return self.channel.is_ready_to_start()

    def get_assignations(self) -> dict[str, Any]:
        return self.channel.get_assignations()

    async def __join_arena(
        self,
        user_id: int,
        player_name: str,
        arena_id: str,
        callbacks: dict[str, Optional[Callable[[Any], Coroutine[Any, Any, None]]]]
    ):
        try:
            logger.info("Joining arena %s", arena_id)
            self.monitor.init_arena(
                self.channel.id,
                arena_id,
                callbacks,
            )
        except KeyError as e:
            raise ChannelError(INVALID_ARENA, UNKNOWN_ARENA_ID) from e
        try:
            await self.monitor.join_arena(user_id, player_name, self.channel.id, arena_id)
        except (KeyError, ValueError) as e:
            logger.error("Error: %s", e)
            raise ChannelError(NOT_ENTERED, "User cannot join this arena.") from e
