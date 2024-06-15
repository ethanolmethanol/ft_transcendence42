import logging
from typing import Any, Callable, Coroutine, Optional

from back_game.app_settings.channel_error import ChannelError
from back_game.game_settings.game_constants import (
    INVALID_ARENA,
    NOT_ENTERED,
    NOT_JOINED,
    UNKNOWN_ARENA_ID,
)
from back_game.monitor.monitor import monitor

logger = logging.getLogger(__name__)


class GameLogicInterface:
    def __init__(self):
        self.channel_id: str = ""
        self.arena_id: str = ""
        self.user_id: int = -1
        self.has_joined: bool = False

    def join(
        self,
        user_id: int,
        player_name: str,
        arena_id: str,
        callbacks: dict[str, Optional[Callable[[str, Any], Coroutine[Any, Any, None]]]]
    ):
        try:
            logger.info("Joining arena %s", arena_id)
            monitor.init_arena(
                self.channel_id,
                arena_id,
                callbacks,
            )
        except KeyError as e:
            raise ChannelError(INVALID_ARENA, UNKNOWN_ARENA_ID) from e
        try:
            monitor.join_arena(user_id, player_name, self.channel_id, arena_id)
        except (KeyError, ValueError) as e:
            logger.error("Error: %s", e)
            raise ChannelError(NOT_ENTERED, "User cannot join this arena.") from e
        self.user_id = user_id
        self.arena_id = arena_id
        self.has_joined = True

    def leave(self):
        if not self.has_joined:
            raise ChannelError(NOT_JOINED, "Attempt to leave without joining.")
        try:
            monitor.leave_arena(self.user_id, self.channel_id, self.arena_id)
        except KeyError as e:
            raise ChannelError(
                NOT_ENTERED,
                "User cannot leave or has already left this arena."
            ) from e
        self.has_joined = False

    def give_up(self):
        if not self.has_joined:
            raise ChannelError(NOT_JOINED, "Attempt to give up without joining.")
        monitor.give_up(self.user_id, self.channel_id, self.arena_id)
        self.has_joined = False

    def rematch(self):
        if not self.has_joined:
            raise ChannelError(NOT_JOINED, "Attempt to rematch without joining.")
        monitor.rematch(self.user_id, self.channel_id, self.arena_id)

    def move_paddle(self, player_name: str, direction: int) -> dict[str, Any]:
        if not self.has_joined:
            raise ChannelError(NOT_JOINED, "Attempt to move paddle without joining.")
        return monitor.move_paddle(
            self.channel_id, self.arena_id, player_name, direction
        )
