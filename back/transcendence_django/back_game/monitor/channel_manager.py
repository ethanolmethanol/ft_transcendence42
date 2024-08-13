import logging
import random
import string
from typing import Any

from back_game.game_arena.arena import Arena
from back_game.game_arena.game import GameStatus
from back_game.game_arena.player import Player
from back_game.game_settings.game_constants import DEAD, WAITING
from back_game.monitor.channel import Channel
from transcendence_django.dict_keys import ID

logger = logging.getLogger(__name__)


class ChannelManager:
    def __init__(self):
        self.channels: dict[str, Channel] = {}
        self.user_game_table: dict[int, Channel] = {}

    def add_user_to_channel(
        self, channel: Channel, arena_id: str, user_id: int
    ) -> dict[str, Any]:
        channel.add_user_into_arena(user_id, arena_id)
        self.user_game_table[user_id] = channel

    def delete_user_from_channel(self, user_id: int):
        try:
            self.user_game_table.pop(user_id)
            logger.info("User %s deleted from user_game_table", user_id)
        except KeyError:
            pass

    async def join_channel(
        self, user_id: int, channel_id: str
    ) -> Channel | None:
        channel = self.channels.get(channel_id)
        if channel is None:
            return None
        arena_id: str = list(self.channel.arenas.keys())[0]
        logger.info("Arena id: %s", arena_id)
        self.add_user_to_channel(channel, arena_id, user_id)
        return channel

    def join_already_created_channel(
        self, user_id: int, is_remote: bool
    ) -> dict[str, Any] | None:
        channel = self.user_game_table.get(user_id)
        if channel is None and is_remote:
            logger.info("User %s is not in a channel and is remote", user_id)
            return self.__get_available_channel()
        if channel is None:
            return None
        logger.info("(Joining already) User %s is already in a channel", user_id)
        arena = self.get_arena_from_user_id(user_id)
        logger.info("Arena gotten: %s", arena.to_dict())
        return {"channel_id": channel.id, "arena": arena.to_dict()}

    async def create_new_channel(
        self, user_id: int, players_specs: dict[str, int]
    ) -> Channel:
        new_arena: Arena = Arena(players_specs)
        new_channel = Channel(new_arena)
        self.channels[new_channel.id] = new_channel
        self.add_user_to_channel(new_channel, new_arena.id, user_id)
        logger.info("New arena: %s", new_arena.to_dict())
        return new_channel

    def get_channel_dict_from_user_id(self, user_id: int) -> dict[str, Any] | None:
        channel: dict[str, Any] | None = self.user_game_table.get(user_id)
        if channel is None:
            return None
        arena = channel.get_arena_from_user_id(user_id)
        return {"channel_id": channel.id, "arena": arena.to_dict()}

    def delete_arena(self, arenas: dict[str, Arena], arena_id: str):
        arena = arenas[arena_id]
        arena.set_status(GameStatus(DEAD))
        logger.info("Arena %s is dead", arena.id)
        player_list: dict[str, Player] = arena.get_players()
        for player in player_list.values():
            self.delete_user_from_channel(player.user_id)
        arenas.pop(arena_id)

    def get_arena(self, channel_id: str, arena_id: str) -> Arena | None:
        logger.info("Trying to get arena %s in channel %s", arena_id, channel_id)
        channel = self.channels.get(channel_id)
        if channel:
            return channel.get_arena(arena_id)
        return None

    def leave_arena(self, user_id: int, channel_id: str, arena_id: str):
        channel = self.channels.get(channel_id)
        if channel is None:
            return
        arena = channel.arenas.get(arena_id)
        if arena is None:
            return
        if arena and not arena.did_player_give_up(user_id):
            if arena.get_status() == WAITING:
                arena.player_gave_up(user_id)
            else:
                arena.player_leave(user_id)

    def is_user_active_in_game(
        self, user_id: int, channel_id: str, arena_id: str
    ) -> bool:
        channel = self.channels.get(channel_id)
        arena = channel.get_arena_from_user_id(user_id)
        if arena and arena.id == arena_id:
            return arena.is_user_active_in_game(user_id)
        return False

    def delete_channel(self, channel_id: str):
        del self.channels[channel_id]

    def __get_available_channel(self) -> dict[str, Any] | None:
        for channel in self.channels.values():
            available_arena = channel.get_available_arena()
            if available_arena:
                return {"channel_id": channel.id, "arena": available_arena.to_dict()}
        return None
