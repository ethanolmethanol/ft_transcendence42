import logging
from typing import Any, Callable, Coroutine, Optional

from back_game.game_arena.arena import Arena
from back_game.monitor.lobby_manager import LobbyManager
from django.apps import apps
from django.conf import settings

logger = logging.getLogger(__name__)


class Monitor:
    MONITOR_INSTANCE = None

    def __init__(self):
        if not apps.ready:
            apps.populate(settings.INSTALLED_APPS)
        self.lobby_manager = LobbyManager()

    async def create_new_lobby(
        self, user_id: int, players_specs: dict[str, int]
    ) -> dict[str, Any]:
        await self.lobby_manager.create_new_lobby(user_id, players_specs)
        return self.lobby_manager.get_lobby_dict_from_user_id(user_id)

    async def join_lobby(
        self, user_id: int, lobby_id: str
    ) -> dict[str, Any] | None:
        await self.lobby_manager.join_lobby(user_id, lobby_id)
        return self.lobby_manager.get_lobby_dict_from_user_id(user_id)

    def join_already_created_lobby(
        self, user_id: int, is_remote: bool
    ) -> dict[str, Any] | None:
        lobby_dict = self.lobby_manager.join_already_created_lobby(
            user_id, is_remote
        )
        return lobby_dict

    async def join_tournament(self, user_id: int) -> dict[str, Any] | None:
        lobby_dict = await self.lobby_manager.join_tournament(user_id)
        if lobby_dict is None:
            raise ValueError("User is already in a lobby.")
        return lobby_dict

    def get_arena(self, lobby_id: str, arena_id: str) -> Arena:
        arena: Arena | None = self.lobby_manager.get_arena(lobby_id, arena_id)
        if arena is None:
            raise KeyError("Arena not found")
        return arena

    def get_arena_from_user_id(self, user_id: int) -> Arena | None:
        return self.lobby_manager.get_arena_from_user_id(user_id)

    def is_user_in_lobby(self, user_id: int) -> bool:
        return self.lobby_manager.get_lobby_from_user_id(user_id) is not None

    async def add_user_to_lobby(
        self, lobby_id: str, arena_id: str | None, user_id: int
    ):
        logger.info("Adding user %s to lobby %s", user_id, lobby_id)
        lobby = self.lobby_manager.lobbies.get(lobby_id)
        if lobby:
            await self.lobby_manager.add_user_to_lobby(
                user_id, lobby_id, arena_id
            )
        else:
            logger.error("Lobby %s not found", lobby_id)

    def init_arena(
        self,
        lobby_id: str,
        arena_id: str,
        callbacks: dict[str, Optional[Callable[[Any], Coroutine[Any, Any, None]]]],
    ):
        arena: Arena = self.get_arena(lobby_id, arena_id)
        arena.update_callbacks(callbacks)

    async def join_arena(
        self, user_id: int, player_name: str, lobby_id: str, arena_id: str
    ):
        found_arena: Arena | None = self.lobby_manager.get_arena_from_user_id(user_id)
        if found_arena and found_arena.id != arena_id:
            raise ValueError("User already in another arena")
        arena: Arena = self.get_arena(lobby_id, arena_id)
        arena.enter_arena(user_id, player_name)
        await self.add_user_to_lobby(lobby_id, arena_id, user_id)

    async def give_up(self, user_id: int, lobby_id: str, arena_id: str | None):
        if arena_id is not None:
            arena: Arena = self.get_arena(lobby_id, arena_id)
            arena.player_gave_up(user_id)
        await self.lobby_manager.delete_user_from_lobby(user_id)

    def get_game_summary(self, lobby_id: str, arena_id: str) -> dict[str, Any]:
        arena: Arena = self.get_arena(lobby_id, arena_id)
        summary: dict[str, Any] = arena.get_game_summary()
        return summary

    def get_users_from_lobby(self, lobby_id: str) -> list[int]:
        return self.lobby_manager.get_users_from_lobby(lobby_id)

    def move_paddle(
        self,
        lobby_id: str,
        arena_id: str,
        player_name: str,
        direction: int,
    ) -> dict[str, Any]:
        arena: Arena = self.get_arena(lobby_id, arena_id)
        return arena.move_paddle(player_name, direction)

    def leave_arena(self, user_id: int, lobby_id: str, arena_id: str | None):
        if arena_id is not None:
            self.lobby_manager.leave_arena(user_id, lobby_id, arena_id)

    def is_user_active_in_game(
        self, user_id: int, lobby_id: str, arena_id: str
    ) -> bool:
        return self.lobby_manager.is_user_active_in_game(
            user_id, lobby_id, arena_id
        )

    @classmethod
    def get_instance(cls):
        if cls.MONITOR_INSTANCE is None:
            cls.MONITOR_INSTANCE = cls()
        return cls.MONITOR_INSTANCE


def get_monitor() -> Monitor:
    return Monitor.get_instance()
