import asyncio
import logging
import random
import string
from typing import Any

from back_game.game_arena.arena import Arena
from back_game.game_arena.game import GameStatus
from back_game.game_arena.player import Player
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
from back_game.monitor.channel import Channel
from back_game.monitor.history_manager import HistoryManager
from transcendence_django.dict_keys import ARENA, ID, START_TIME

logger = logging.getLogger(__name__)


class ChannelManager:
    def __init__(self):
        self.channels: dict[str, Channel] = {}
        self.user_game_table: dict[int, Channel] = {}
        self.history_manager = HistoryManager()

    def add_user_to_channel(
        self, channel: Channel, arena_id: str | None, user_id: int
    ) -> dict[str, Any]:
        if arena_id is None:
            arena = channel.get_available_arena()
            if arena is None:
                return {}
            arena_id = arena.id
        channel.add_user_into_arena(user_id, arena_id)
        self.user_game_table[user_id] = channel

    def delete_user_from_channel(self, user_id: int, channel: Channel = None):
        try:
            if channel is None:
                channel = self.user_game_table.get(user_id)
            elif channel == self.user_game_table.get(user_id):
                self.user_game_table.pop(user_id)
            if channel is not None:
                channel.delete_user_from_arena(user_id)
                if not channel.users:
                    self.delete_channel(channel.id)
            logger.info("User %s deleted from user_game_table", user_id)
        except KeyError:
            pass

    async def join_channel(
        self, user_id: int, channel_id: str
    ) -> Channel | None:
        channel = self.get_channel(channel_id)
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
        arena = self.get_arena_from_user_id(user_id)
        return {"channel_id": channel.id, "arena": arena.to_dict()}

    async def create_new_channel(
        self, user_id: int, players_specs: dict[str, int], is_tournament: bool = False
    ) -> Channel:
        arenas_count = 2 if is_tournament else 1
        logger.info("Creating new channel with %s arenas", arenas_count)
        arenas = {}
        for _ in range(arenas_count):
            new_arena: Arena = Arena(players_specs)
            arenas[new_arena.id] = new_arena
        new_channel = Channel(arenas, is_tournament=is_tournament)
        self.channels[new_channel.id] = new_channel
        self.add_user_to_channel(new_channel, new_arena.id, user_id)
        for arena in arenas.values():
            asyncio.create_task(self.__arena_loop(new_channel, arena))
            asyncio.create_task(self.__run_game_loop(arena))
        logger.info("New arena: %s", new_arena.to_dict())
        return new_channel

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

    def delete_arena(self, channel_id: string, arena_id: str):
        channel = self.get_channel(channel_id)
        arena = channel.arenas[arena_id]
        arena.set_status(GameStatus(DEAD))
        logger.info("Arena %s is dead", arena.id)
        player_list: dict[str, Player] = arena.get_players()
        for player in player_list.values():
            self.delete_user_from_channel(player.user_id, channel)
        channel.delete_arena(arena_id)

    def get_arena(self, channel_id: str, arena_id: str) -> Arena | None:
        logger.info("Trying to get arena %s in channel %s", arena_id, channel_id)
        channel = self.get_channel(channel_id)
        if channel:
            return channel.get_arena(arena_id)
        return None

    def get_assignations(self, channel_id: str) -> dict[str, Any]:
        channel = self.get_channel(channel_id)
        if channel:
            return channel.get_assignations()
        return {}

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

    def delete_channel(self, channel_id: str):
        channel = self.get_channel(channel_id)
        if channel is not None:
            del channel
            logger.info("Channel %s deleted", channel_id)

    def __get_available_channel(self, is_tournament: bool = False) -> dict[str, Any] | None:
        for channel in self.channels.values():
            if channel.is_tournament == is_tournament:
                available_arena = channel.get_available_arena()
                logger.info("Available arena: %s in channel %s", available_arena, channel.id)
                if available_arena:
                    return {"channel_id": channel.id, "arena": available_arena.to_dict()}
        return None

    async def save_game_summary(
        self,
        summary: dict[str, Any],
    ):
        if summary[START_TIME] is not None:
            await self.history_manager.save_game_summary(summary)

    async def __update_game_states(self, arena: Arena):
        arena_status = arena.get_status()
        if arena.can_be_started():
            await arena.start_game()
        elif arena.can_be_over():
            arena.conclude_game()
            summary = arena.get_game_summary()
            await self.save_game_summary(summary)
            if arena_status != GameStatus(STARTED):
                arena.set_status(GameStatus(DEAD))
        elif arena_status == GameStatus(OVER):
            logger.info("Game over in arena %s", arena.id)
            await self.__game_over(arena)

    async def __arena_loop(self, channel: Channel, arena: Arena):
        while arena.get_status() != GameStatus(DEAD):
            await self.__update_game_states(arena)
            await asyncio.sleep(MONITOR_LOOP_INTERVAL)
        self.delete_arena(channel.id, arena.id)
        if channel is not None and len(channel.arenas) == 0:
            self.delete_channel(channel.id)

    async def __run_game_loop(self, arena: Arena):
        while arena:
            if arena.get_status() == GameStatus(STARTED):
                update_message = arena.update_game()
                if arena.game_update_callback is not None:
                    await arena.game_update_callback(update_message)
            await asyncio.sleep(RUN_LOOP_INTERVAL)

    async def __game_over(self, arena: Arena):
        arena.set_status(GameStatus(DYING))
        if arena.game_update_callback is not None:
            logger.info("Sending game over message to arena %s", arena.id)
            await arena.game_update_callback({ARENA: arena.to_dict()})
        time = TIMEOUT_GAME_OVER + 1
        while (
            arena.get_status() in [GameStatus(DYING), GameStatus(WAITING)] and time > 0
        ):
            time -= TIMEOUT_INTERVAL
            if arena.game_over_callback is not None:
                await arena.game_over_callback(time)
            if time <= 0 and arena.get_status() == GameStatus(DYING):
                arena.set_status(GameStatus(DEAD))
            else:
                await asyncio.sleep(TIMEOUT_INTERVAL)

