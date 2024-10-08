import logging
from typing import Any, Callable, Coroutine, Optional

from back_game.app_settings.lobby_error import LobbyError
from back_game.game_settings.game_constants import (
    INVALID_ARENA,
    INVALID_LOBBY,
    NOT_ENTERED,
    NOT_JOINED,
    UNKNOWN_ARENA_ID,
    UNKNOWN_LOBBY_ID,
)
from back_game.monitor.lobby.lobby import Lobby
from back_game.monitor.lobby.tournament_lobby import RoundMapType, TournamentLobby
from back_game.monitor.monitor import get_monitor

logger = logging.getLogger(__name__)


class GameLogicInterface:
    def __init__(self, is_tournament: bool = False):
        self.lobby: Lobby | None = None
        self.arena_id: str | None = None
        self.user_id: int = -1
        self.has_joined: bool = False
        self.is_tournament: bool = is_tournament
        self.monitor = get_monitor()

    def init_lobby(self, lobby_id: str):
        self.lobby = self.monitor.lobby_manager.get_lobby(lobby_id)
        if self.lobby is None:
            raise LobbyError(INVALID_LOBBY, UNKNOWN_LOBBY_ID)

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
            await self.monitor.add_user_to_lobby(self.lobby.id, None, user_id)
        self.user_id = user_id
        self.has_joined = True

    def leave(self):
        if not self.has_joined:
            raise LobbyError(NOT_JOINED, "Attempt to leave without joining.")
        try:
            self.monitor.leave_arena(self.user_id, self.lobby.id, self.arena_id)
        except KeyError as e:
            raise LobbyError(
                NOT_ENTERED, "User cannot leave or has already left this arena."
            ) from e
        self.has_joined = False

    async def give_up(self):
        if not self.has_joined:
            raise LobbyError(NOT_JOINED, "Attempt to give up without joining.")
        await self.monitor.give_up(self.user_id, self.lobby.id, self.arena_id)
        self.has_joined = False

    def rematch(self):
        if not self.has_joined:
            raise LobbyError(NOT_JOINED, "Attempt to rematch without joining.")
        self.monitor.rematch(self.user_id, self.lobby.id, self.arena_id)

    def move_paddle(self, player_name: str, direction: int) -> dict[str, Any]:
        if not self.has_joined:
            raise LobbyError(NOT_JOINED, "Attempt to move paddle without joining.")
        try:
            return self.monitor.move_paddle(
                self.lobby.id, self.arena_id, player_name, direction
            )
        except KeyError:
            pass
        return {}

    def is_lobby_full(self) -> bool:
        return self.lobby.is_full()

    def is_ready_to_start(self) -> bool:
        return self.lobby.is_ready_to_start()

    async def __join_arena(
        self,
        user_id: int,
        player_name: str,
        arena_id: str,
        callbacks: dict[str, Optional[Callable[[Any], Coroutine[Any, Any, None]]]],
    ):
        try:
            self.monitor.init_arena(
                self.lobby.id,
                arena_id,
                callbacks,
            )
        except KeyError as e:
            raise LobbyError(INVALID_ARENA, UNKNOWN_ARENA_ID) from e
        try:
            await self.monitor.join_arena(
                user_id, player_name, self.lobby.id, arena_id
            )
        except (KeyError, ValueError) as e:
            logger.error("Error: %s", e)
            raise LobbyError(NOT_ENTERED, "User cannot join this arena.") from e

    def get_tournament_map(self) -> RoundMapType:
        if not self.is_tournament:
            raise LobbyError(
                INVALID_LOBBY, "Attempt to get tournament map in a non-tournament"
            )
        tournament_lobby: TournamentLobby = self.lobby
        return tournament_lobby.get_tournament_map()
