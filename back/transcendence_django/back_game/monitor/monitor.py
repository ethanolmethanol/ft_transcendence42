import asyncio
import logging
import random
import string
from typing import Any

from back_game.game_arena.arena import Arena
from back_game.game_arena.game import GameStatus
from back_game.game_settings.game_constants import (
    DEAD,
    DYING,
    MONITOR_LOOP_INTERVAL,
    OVER,
    RUN_LOOP_INTERVAL,
    STARTED,
    TIMEOUT_GAME_OVER,
    TIMEOUT_INTERVAL,
)
from back_game.game_arena.player import Player

logger = logging.getLogger(__name__)


class Monitor:

    def __init__(self):
        self.channels: dict[str, Any] = {}  # key: channel_id, value: dict [key: arena_id, value: arena]
        self.user_game_table: dict[int, Any] = {}

    def generate_random_id(self, length: int) -> str:
        letters_and_digits = string.ascii_letters + string.digits
        return "".join(random.choice(letters_and_digits) for _ in range(length))

    async def get_channel(self, user_id: int, players_specs: dict[str, int]) -> dict[str, Any]:
        channel = self.get_channel_from_user_id(user_id)
        if channel is None:
            return await self.get_new_channel(user_id, players_specs)
        return channel

    async def get_new_channel(self, user_id: int, players_specs: dict[str, int]) -> dict[str, Any]:
        new_arena = Arena(players_specs)
        channel_id = self.generate_random_id(10)
        self.channels[channel_id] = {new_arena.id: new_arena}
        asyncio.create_task(
            self.monitor_arenas_loop(channel_id, self.channels[channel_id])
        )
        asyncio.create_task(self.run_game_loop(self.channels[channel_id]))
        self.user_game_table[user_id] = {
            "channel_id": channel_id,
            "arena": new_arena.to_dict(),
        }
        logger.info("New arena: %s", new_arena.to_dict())
        return self.user_game_table[user_id]

    def get_channel_from_user_id(self, user_id: int) -> dict[str, Any] | None:
        channel = self.user_game_table.get(user_id)
        if channel is None:
            return None
        channel_id = channel["channel_id"]
        arena_id = channel["arena"]["id"]
        arena = self.channels[channel_id][arena_id]
        channel = {"channel_id": channel_id, "arena": arena.to_dict()}
        return channel

    def delete_arena(self, arenas: dict[str, Arena], arena_id: str):
        player_list: dict[str, Player] = arenas[arena_id].get_players()
        for player in player_list.values():
            self.delete_user(player.user_id)
        arenas.pop(arena_id)

    def add_user(self, user_id: int, channel_id: str, arena_id: int):
        self.user_game_table[user_id] = {
            "channel_id": channel_id,
            "arena": self.channels[channel_id][arena_id].to_dict(),
        }

    def delete_user(self, user_id: int):
        try:
            self.user_game_table.pop(user_id)
            logger.info("User %s deleted from user_game_table", user_id)
        except KeyError:
            pass

    def is_user_in_game(self, user_id: int, channel_id: str, arena_id: int) -> bool:
        return self.user_game_table.get(user_id) == {
            "channel_id": channel_id,
            "arena": arena_id,
        }

    def delete_channel(self, channel_id: str):
        del self.channels[channel_id]

    async def monitor_arenas_loop(self, channel_id: str, arenas: dict[str, Arena]):
        while arenas:
            await self.update_game_states(arenas)
            await asyncio.sleep(MONITOR_LOOP_INTERVAL)
        self.delete_channel(channel_id)

    async def update_game_states(self, arenas: dict[str, Arena]):
        for arena in arenas.values():
            if arena.get_status() == GameStatus(STARTED) and arena.is_empty():
                arena.conclude_game()
            if arena.get_status() == GameStatus(OVER):
                logger.info("Game over in arena %s", arena.id)
                await self.game_over(arenas, arena)
                break

    async def run_game_loop(self, arenas: dict[str, Arena]):
        while arenas:
            for arena in arenas.values():
                if arena.get_status() == GameStatus(STARTED):
                    update_message = arena.update_game()
                    if arena.game_update_callback is not None:
                        await arena.game_update_callback(update_message)
            await asyncio.sleep(RUN_LOOP_INTERVAL)

    async def game_over(self, arenas: dict[str, Arena], arena: Arena):
        arena.set_status(GameStatus(DYING))
        time = TIMEOUT_GAME_OVER + 1
        while arena.get_status() == GameStatus(DYING) and time > 0:
            time -= TIMEOUT_INTERVAL
            if arena.game_over_callback is not None:
                await arena.game_over_callback("Game Over! Thank you for playing.", time)
            if time == 0:
                arena.set_status(GameStatus(DEAD))
                self.delete_arena(arenas, arena.id)
            else:
                await asyncio.sleep(TIMEOUT_INTERVAL)


monitor = Monitor()
