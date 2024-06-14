import logging
import random
import string

from typing import Any

from back_game.game_arena.arena import Arena
from back_game.game_arena.game import GameStatus
from back_game.game_settings.game_constants import DEAD, WAITING
from back_game.game_arena.player import Player

logger = logging.getLogger(__name__)


class ChannelManager:
    def __init__(self):
        self.channels: dict[str, dict[int, Arena]] = {}
        self.user_game_table: dict[int, dict[str, Any]] = {}

    async def join_channel(self, user_id: int, channel_id: str) -> dict[str, Any]:
        channel = self.get_channel_from_user_id(user_id)
        if self.channels[channel_id] is None:
            return None
        arena_id: int = self.channels[channel_id].keys()[0]
        self.add_user_to_channel(user_id, channel_id, arena_id)
        return channel

    def join_already_created_channel(
        self, user_id: int, is_remote: bool
    ) -> dict[str, Any] | None:
        channel = self.get_channel_from_user_id(user_id)
        if channel is None and is_remote:
            channel = self.__get_available_channel()
        if channel is None:
            return None
        return channel

    async def create_new_channel(
        self, user_id: int, players_specs: dict[str, int]
    ) -> dict[str, Any]:
        new_arena: Arena = Arena(players_specs)
        channel_id = self.__generate_random_id(10)
        self.channels[channel_id] = {new_arena.id: new_arena}
        self.add_user_to_channel(user_id, channel_id, new_arena.id)
        logger.info("New arena: %s", new_arena.to_dict())
        return self.user_game_table[user_id]

    def get_channel_from_user_id(self, user_id: int) -> dict[str, Any] | None:
        channel: dict[str, Any] | None = self.user_game_table.get(user_id)
        if channel is None:
            return None
        return channel

    def add_user_to_channel(self, user_id: int, channel_id: str, arena_id: int):
        arena: Arena = self.channels[channel_id][arena_id]
        self.user_game_table[user_id] = {
            "channel_id": channel_id,
            "arena": arena.to_dict(),
        }

    def delete_arena(self, arenas: dict[str, Arena], arena_id: str):
        arena = arenas[arena_id]
        arena.set_status(GameStatus(DEAD))
        logger.info("Arena %s is dead", arena.id)
        player_list: dict[str, Player] = arena.get_players()
        for player in player_list.values():
            self.delete_user(player.user_id)
        arenas.pop(arena_id)

    def get_arena(self, channel_id: str, arena_id: int) -> Arena | None:
        channel = self.channels.get(channel_id)
        if channel:
            return channel.get(arena_id)
        return None

    def leave_arena(self, user_id: int, channel_id: str, arena_id: int):
        channel = self.channels.get(channel_id)
        if channel is None:
            return
        arena = channel.get(arena_id)
        if arena is None:
            return
        if arena and not arena.did_player_give_up(user_id):
            if arena.get_status() == WAITING:
                arena.player_gave_up(user_id)
            else:
                arena.player_leave(user_id)

    def is_user_active_in_game(
        self, user_id: int, channel_id: str, arena_id: int
    ) -> bool:
        if self.user_game_table.get(user_id) == {
            "channel_id": channel_id,
            "arena": arena_id,
        }:
            arena: Arena = self.channels[channel_id][arena_id]
            return arena.is_user_active_in_game(user_id)
        return False

    def delete_channel(self, channel_id: str):
        del self.channels[channel_id]

    def delete_user(self, user_id: int):
        try:
            self.user_game_table.pop(user_id)
            logger.info("User %s deleted from user_game_table", user_id)
        except KeyError:
            pass

    def __get_available_channel(self) -> dict[str, Any] | None:
        for channel_id, channel in self.channels.items():
            arena_id = list(channel.keys())[0]
            arena = channel[arena_id]
            if arena.get_status() == GameStatus(WAITING):
                return {"channel_id": channel_id, "arena": arena.to_dict()}
        return None

    def __generate_random_id(self, length: int) -> str:
        letters_and_digits = string.ascii_letters + string.digits
        return "".join(random.choice(letters_and_digits) for _ in range(length))
