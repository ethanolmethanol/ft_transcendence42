import logging
import random
import string
from typing import Any

from back_game.game_arena.arena import Arena
from back_game.game_arena.game import GameStatus
from back_game.game_arena.player import Player
from back_game.game_settings.game_constants import CREATED, DEAD, TOURNAMENT_ARENA_COUNT, WAITING
from transcendence_django.dict_keys import ID

logger = logging.getLogger(__name__)


class ChannelManager:
    def __init__(self):
        self.channels: dict[str, dict[str, Arena]] = {}
        self.user_game_table: dict[int, dict[str, Any]] = {}

    def can_channel_be_joined(self, channel_id: str, user_id: int) -> bool:
        if channel_id not in self.channels:
            return False
        channel = self.channels[channel_id]
        if channel["is_tournament"]:
            return False
        arena_id: str = list(channel["arenas"])[0]
        arena: Arena = channel["arenas"][arena_id]
        return arena.get_status() == GameStatus(WAITING)

    async def join_channel(
        self, user_id: int, channel_id: str
    ) -> dict[str, Any] | None:
        if not self.can_channel_be_joined(channel_id, user_id):
            return None
        arena_id: str = list(self.channels[channel_id]["arenas"])[0]
        logger.info("Arena id: %s", arena_id)
        self.add_user_to_channel(user_id, channel_id, arena_id)
        return self.get_channel_from_user_id(user_id)

    def join_already_created_channel(
        self, user_id: int, is_remote: bool, is_tournament: bool
    ) -> dict[str, Any] | None:
        channel = self.get_channel_from_user_id(user_id)
        if channel is None and is_remote:
            channel = self.__get_available_channel(is_tournament)
        if channel is None:
            return None
        return channel

    async def create_new_channel(
        self, user_id: int, players_specs: dict[str, int], is_tournament: bool = False
    ) -> dict[str, Any]:
        arena_count = 1
        if is_tournament:
            arena_count = TOURNAMENT_ARENA_COUNT
        arenas = []
        for _ in range(arena_count):
            new_arena: Arena = Arena(players_specs)
            arenas.append(new_arena)
        channel_id: str = self.__generate_random_id(10)
        self.channels[channel_id] = {
            "is_tournament": is_tournament,
            "arenas": {arena.id: arena for arena in arenas}
        }
        self.add_user_to_channel(user_id, channel_id, arenas[0].id)
        logger.info("New arenas: %s", arenas)
        return self.user_game_table[user_id]

    def get_channel_from_user_id(self, user_id: int) -> dict[str, Any] | None:
        channel: dict[str, Any] | None = self.user_game_table.get(user_id)
        if channel is None:
            return None
        return channel

    def add_user_to_channel(self, user_id: int, channel_id: str, arena_id: str):
        logger.info("Adding user %s to channel %s in arena %s", user_id, channel_id, arena_id)
        arena: Arena = self.channels[channel_id]["arenas"][arena_id]
        self.user_game_table[user_id] = {
            "channel_id": channel_id,
            "arena": arena.to_dict(),
        }

    def are_all_arenas_ready(self, channel_id: str) -> bool:
        channel = self.channels[channel_id]
        arenas = channel["arenas"]
        return all(arena.is_full() for arena in arenas.values())

    def delete_arena(self, arenas: dict[str, Arena], arena_id: str):
        arena = arenas[arena_id]
        arena.set_status(GameStatus(DEAD))
        logger.info("Arena %s is dead", arena.id)
        player_list: dict[str, Player] = arena.get_players()
        for player in player_list.values():
            self.delete_user(player.user_id, arena_id)
        arenas.pop(arena_id)

    def get_arena(self, channel_id: str, arena_id: str) -> Arena | None:
        logger.info("Trying to get arena %s in channel %s", arena_id, channel_id)
        channel = self.channels.get(channel_id)
        if channel:
            return channel["arenas"].get(arena_id)
        return None

    def leave_arena(self, user_id: int, channel_id: str, arena_id: str):
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
        self, user_id: int, channel_id: str, arena_id: str
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

    def delete_user(self, user_id: int, arena_id: str):
        try:
            user_data = self.user_game_table[user_id]
            if user_data["arena"][ID] == arena_id:
                self.user_game_table.pop(user_id)
                logger.info("User %s deleted from user_game_table", user_id)
        except KeyError:
            pass

    def __get_available_channel(self, is_tournament: bool) -> dict[str, Any] | None:
        channels = {
            channel_id: channel
            for channel_id, channel in self.channels.items()
            if channel["is_tournament"] == is_tournament
        }
        for channel_id, channel in channels.items():
            arenas_id: list[str] = list(channel["arenas"].keys())
            if not arenas_id:
                return None
            for arena_id in arenas_id:
                arena: Arena = channel["arenas"][arena_id]
                if arena.is_private() or arena.is_full():
                    continue
                if arena.get_status() in [GameStatus(CREATED), GameStatus(WAITING)]:
                    return {"channel_id": channel_id, "arena": arena.to_dict()}
        return None

    def __generate_random_id(self, length: int) -> str:
        letters_and_digits = string.ascii_letters + string.digits
        return "".join(random.choice(letters_and_digits) for _ in range(length))
