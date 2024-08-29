import asyncio
import logging
from typing import Any

from back_game.monitor.channel.classic_channel import ClassicChannel
from back_game.monitor.channel.tournament_channel import TournamentChannel
from back_game.game_arena.arena import Arena
from back_game.game_settings.game_constants import (
    DEAD,
    DYING,
    MONITOR_LOOP_INTERVAL,
    OVER,
    RUN_LOOP_INTERVAL,
    STARTED,
    TIMEOUT_GAME_OVER,
    TIMEOUT_INTERVAL,
    TOURNAMENT_SPECS,
    WAITING
)
from back_game.monitor.channel.channel import Channel

logger = logging.getLogger(__name__)


class ChannelManager:
    def __init__(self):
        self.channels: dict[str, Channel] = {}
        self.user_game_table: dict[int, Channel] = {}

    async def add_user_to_channel(
        self, channel: Channel, arena_id: str | None, user_id: int
    ) -> dict[str, Any]:
        if arena_id is None:
            arena = channel.get_available_arena()
            if arena is None:
                return {}
            arena_id = arena.id
        await channel.add_user_into_arena(user_id, arena_id)
        self.user_game_table[user_id] = channel

    def delete_user_from_channel(self, user_id: int, channel: Channel = None):
        try:
            if channel is None:
                channel = self.user_game_table.get(user_id)
            elif channel != self.user_game_table.get(user_id):
                raise KeyError
            self.user_game_table.pop(user_id)
            if channel is not None:
                channel.delete_user(user_id)
                if channel.can_be_deleted():
                    self.delete_channel(channel.id)
                logger.info("User %s deleted from user_game_table", user_id)
        except KeyError:
            pass

    def delete_channel(self, channel_id: str):
        channel = self.get_channel(channel_id)
        if channel is not None:
            if channel.users:
                for user_id in list(channel.users.keys()):
                    self.delete_user_from_channel(user_id, channel)
            else:
                channel.disable()
                self.channels.pop(channel_id)
                logger.info("Channel %s deleted", channel_id)

    async def join_channel(
        self, user_id: int, channel_id: str
    ) -> Channel | None:
        channel = self.get_channel(channel_id)
        if channel is None:
            return None
        arena_id: str = list(self.channel.arenas.keys())[0]
        logger.info("Arena id: %s", arena_id)
        await self.add_user_to_channel(channel, arena_id, user_id)
        return channel

    def join_already_created_channel(
        self, user_id: int, is_remote: bool
    ) -> dict[str, Any] | None:
        channel = self.user_game_table.get(user_id)
        if channel is None and is_remote:
            logger.info("User %s is not in a channel and is remote", user_id)
            return self.__get_available_channel()
        if channel is None or channel.is_tournament():
            return None
        arena = self.get_arena_from_user_id(user_id)
        return {"channel_id": channel.id, "arena": arena.to_dict()}

    async def create_new_channel(
        self, user_id: int, players_specs: dict[str, int], is_tournament: bool = False
    ) -> Channel:
        if is_tournament:
            new_channel = TournamentChannel(players_specs)
        else:
            new_channel = ClassicChannel(players_specs)
        self.channels[new_channel.id] = new_channel
        arenas = new_channel.arenas
        new_arena = list(arenas.values())[0]
        for arena in arenas.values():
            asyncio.create_task(self.__arena_loop(new_channel, arena))
            asyncio.create_task(new_channel.run_game_loop(arena))
        await self.add_user_to_channel(new_channel, new_arena.id, user_id)
        logger.info("New arena: %s", new_arena.to_dict())
        return new_channel

    async def __arena_loop(self, channel: Channel, arena: Arena):
        await channel.arena_loop(arena)
        if channel is not None and channel.can_be_deleted():
            self.delete_channel(channel.id)

    async def join_tournament(self, user_id: int) -> dict[str, Any] | None:
        channel_dict = self.__get_available_channel(is_tournament=True)
        if channel_dict is None:
            channel = await self.create_new_channel(user_id, TOURNAMENT_SPECS, is_tournament=True)
            return self.get_channel_dict_from_user_id(user_id)
        return channel_dict

    def get_channel(self, channel_id: str) -> Channel | None:
        return self.channels.get(channel_id)

    def get_channel_dict_from_user_id(self, user_id: int) -> dict[str, Any] | None:
        channel: Channel | None = self.user_game_table.get(user_id)
        if channel is None:
            return None
        arena = channel.get_arena_from_user_id(user_id)
        return {"channel_id": channel.id, "arena": arena.to_dict()}

    def get_arena(self, channel_id: str, arena_id: str) -> Arena | None:
        channel = self.get_channel(channel_id)
        if channel:
            return channel.get_arena(arena_id)
        return None

    def leave_arena(self, user_id: int, channel_id: str, arena_id: str):
        channel = self.get_channel(channel_id)
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

    def get_users_from_channel(self, channel_id: str) -> list[int]:
        channel = self.get_channel(channel_id)
        if channel is None:
            return []
        return list(channel.users.keys())

    def is_user_active_in_game(
        self, user_id: int, channel_id: str, arena_id: str
    ) -> bool:
        channel = self.get_channel(channel_id)
        arena = channel.get_arena_from_user_id(user_id)
        if arena and arena.id == arena_id:
            return arena.is_user_active_in_game(user_id)
        return False

    def get_arena_from_user_id(self, user_id: int) -> Arena | None:
        channel = self.user_game_table.get(user_id)
        if channel is None:
            return None
        return channel.get_arena_from_user_id(user_id)

    def __get_available_channel(self, is_tournament: bool = False) -> dict[str, Any] | None:
        for channel in self.channels.values():
            if channel.is_tournament() == is_tournament:
                available_arena = channel.get_available_arena()
                logger.info("Available arena: %s in channel %s", available_arena, channel.id)
                if available_arena:
                    return {"channel_id": channel.id, "arena": available_arena.to_dict()}
        return None
