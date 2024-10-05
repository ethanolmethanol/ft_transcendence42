import asyncio
import logging
from typing import Any

from back_game.game_arena.arena import Arena
from back_game.game_settings.game_constants import (
    LOBBY_LOOP_INTERVAL,
    TOURNAMENT_SPECS,
    GameStatus,
)
from back_game.monitor.lobby.classic_lobby import ClassicLobby
from back_game.monitor.lobby.lobby import Lobby
from back_game.monitor.lobby.tournament_lobby import TournamentLobby
from requests import JSONDecodeError, Response
from requests import get as http_get
from transcendence_django.dict_keys import (
    AI_OPPONENTS_LOCAL,
    AI_OPPONENTS_ONLINE,
    ARENA_ID,
    LOBBY_ID,
    OPTIONS,
    USER_ID,
)

logger = logging.getLogger(__name__)


class LobbyManager:
    def __init__(self):
        self.lobbies: dict[str, Lobby] = {}

    async def add_to_lobby(
        self,
        user_id: int,
        lobby_id: str,
        arena_id: str | None,
    ):
        lobby = self.get_lobby(lobby_id)
        if lobby is None:
            return
        if arena_id is None:
            arena = lobby.get_available_arena()
            if arena is None:
                return
            arena_id = arena.id
        await lobby.add_user_into_arena(user_id, arena_id)

    def delete_user_from_lobby(self, user_id: int, lobby: Lobby = None):
        try:
            if lobby is None:
                lobby = self.get_lobby_from_user_id(user_id)
            elif lobby != self.get_lobby_from_user_id(user_id):
                raise KeyError
#             self.user_game_table.pop(user_id)
            if lobby is not None:
                lobby.delete_user(user_id)
                if lobby.can_be_deleted():
                    self.delete_lobby(lobby.id)
#                 logger.info("User %s deleted from user_game_table", user_id)
        except KeyError:
            pass

    def delete_lobby(self, lobby_id: str):
        lobby = self.get_lobby(lobby_id)
        if lobby is not None:
            if lobby.users:
                for user_id in list(lobby.users.keys()):
                    self.delete_user_from_lobby(user_id, lobby)
            else:
                lobby.disable()
                self.lobbies.pop(lobby_id)
                logger.info("Lobby %s deleted", lobby_id)

    async def join_lobby(self, user_id: int, lobby_id: str) -> Lobby | None:
        lobby = self.get_lobby(lobby_id)
        if lobby is None:
            return None
        arena_id: str = list(lobby.arenas.keys())[0]
        logger.info("Arena id: %s", arena_id)
        await self.add_user_to_lobby(user_id, lobby.id, arena_id)
        return lobby

    def join_already_created_lobby(
        self, user_id: int, is_remote: bool
    ) -> dict[str, Any] | None:
        lobby = self.get_lobby_from_user_id(user_id)
        if lobby is None and is_remote:
            logger.info("User %s is not in a lobby and is remote", user_id)
            return self.__get_available_lobby()
        if lobby is None or lobby.is_tournament():
            return None
        arena = self.get_arena_from_user_id(user_id)
        return {"lobby_id": lobby.id, "arena": arena.to_dict()}

    async def create_new_lobby(
        self, user_id: int, players_specs: dict[str, int], is_tournament: bool = False
    ) -> Lobby:
        if is_tournament:
            new_lobby = TournamentLobby(players_specs)
        else:
            new_lobby = ClassicLobby(players_specs)
        self.lobbies[new_lobby.id] = new_lobby
        arenas = new_lobby.arenas
        new_arena = list(arenas.values())[0]
        logger.info("New lobby %s created", new_lobby.id)
        await self.add_user_to_lobby(user_id, new_lobby.id, new_arena.id)
        await self.spawn_bots(players_specs, new_lobby.id, new_arena.id)
        asyncio.create_task(self.run_lobby_loop(new_lobby))
        return new_lobby

    async def run_lobby_loop(self, lobby: Lobby):
        while lobby and not lobby.can_be_deleted():
            await asyncio.sleep(LOBBY_LOOP_INTERVAL)
        self.delete_lobby(lobby.id)

    async def join_tournament(self, user_id: int) -> dict[str, Any] | None:
        lobby_dict = self.__get_available_lobby(is_tournament=True)
        if lobby_dict is None:
            lobby = self.get_lobby_from_user_id(user_id)
            if lobby is None:
                await self.create_new_lobby(user_id, TOURNAMENT_SPECS, is_tournament=True)
                return self.get_lobby_dict_from_user_id(user_id)
        return lobby_dict

    def get_lobby(self, lobby_id: str) -> Lobby | None:
        return self.lobbies.get(lobby_id)

    def get_lobby_dict_from_user_id(self, user_id: int) -> dict[str, Any] | None:
        lobby: Lobby | None = self.get_lobby_from_user_id(user_id)
        if lobby is None:
            return None
        arena = lobby.get_arena_from_user_id(user_id)
        return {"lobby_id": lobby.id, "arena": arena.to_dict()}

    async def spawn_bots(
        self, players_specs: dict[str, Any], lobby_id: str, arena_id: str
    ):
        bots: int = int(players_specs[OPTIONS][AI_OPPONENTS_LOCAL]) + int(
            players_specs[OPTIONS][AI_OPPONENTS_ONLINE]
        )
        while bots:
            bots -= 1
            try:
                aipi_response: Response = http_get(
                    url="https://back-aipi/aipi/spawn/",
                    verify=False,  # does not work otherwise
                    cert=("/etc/ssl/serv.crt", "/etc/ssl/serv.key"),
                    json={LOBBY_ID: lobby_id, ARENA_ID: arena_id},
                    timeout=3,
                )
                ai_user_id: int = aipi_response.json()[USER_ID]
                await self.add_ai_to_lobby(ai_user_id, lobby_id, arena_id)
            except (ConnectionRefusedError, JSONDecodeError) as e:
                logger.error(e)

    async def add_user_to_lobby(self, user_id: int, lobby_id: str, arena_id: str):
        await self.add_to_lobby(user_id, lobby_id, arena_id)

    async def add_ai_to_lobby(self, user_id: int, lobby_id: str, arena_id: str):
        await self.add_to_lobby(user_id, lobby_id, arena_id)

    def get_arena(self, lobby_id: str, arena_id: str) -> Arena | None:
        lobby = self.get_lobby(lobby_id)
        if lobby:
            return lobby.get_arena(arena_id)
        return None

    def leave_arena(self, user_id: int, lobby_id: str, arena_id: str):
        lobby = self.get_lobby(lobby_id)
        if lobby is None:
            return
        arena = lobby.arenas.get(arena_id)
        if arena is None:
            return
        if arena and not arena.did_player_give_up(user_id):
            if arena.get_status() == GameStatus.WAITING:
                arena.player_gave_up(user_id)
            else:
                arena.player_leave(user_id)

    def get_users_from_lobby(self, lobby_id: str) -> list[int]:
        lobby = self.get_lobby(lobby_id)
        if lobby is None:
            return []
        return list(lobby.users.keys())

    def is_user_active_in_game(
        self, user_id: int, lobby_id: str, arena_id: str
    ) -> bool:
        lobby = self.get_lobby(lobby_id)
        arena = lobby.get_arena_from_user_id(user_id)
        if arena and arena.id == arena_id:
            return arena.is_user_active_in_game(user_id)
        return False

    def get_arena_from_user_id(self, user_id: int) -> Arena | None:
        lobby = self.get_lobby_from_user_id(user_id)
        if lobby is None:
            return None
        return lobby.get_arena_from_user_id(user_id)

    def get_lobby_from_user_id(self, user_id: int) -> Lobby | None:
        for lobby in self.lobbies.values():
            if user_id in lobby.users:
                return lobby
        return None

    def __get_available_lobby(
        self, is_tournament: bool = False
    ) -> dict[str, Any] | None:
        for lobby in self.lobbies.values():
            if lobby.is_tournament() == is_tournament:
                available_arena = lobby.get_available_arena()
                logger.info(
                    "Available arena: %s in lobby %s", available_arena, lobby.id
                )
                if available_arena:
                    return {
                        "lobby_id": lobby.id,
                        "arena": available_arena.to_dict(),
                    }
        return None
