import asyncio
import logging
import random
import string

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
)

logger = logging.getLogger(__name__)


class Monitor:

    def __init__(self):
        self.channels = {}  # key: channel_id, value: dict [key: arena_id, value: arena]
        self.user_game_table = {}

    def generate_random_id(self, length: int) -> str:
        letters_and_digits = string.ascii_letters + string.digits
        return "".join(random.choice(letters_and_digits) for _ in range(length))

    async def get_channel(self, user_id: str, players_specs: dict) -> dict:
        channel = self.get_channel_from_user_id(user_id)
        if channel is None:
            return await self.get_new_channel(user_id, players_specs)
        return channel

    async def get_new_channel(self, user_id: str, players_specs: dict) -> dict:
        new_arena = Arena(players_specs)
        channel_id = self.generate_random_id(10)
        self.channels[channel_id] = {new_arena.id: new_arena}
        asyncio.create_task(
            self.monitor_arenas_loop(channel_id, self.channels[channel_id])
        )
        asyncio.create_task(self.run_game_loop(self.channels[channel_id].values()))
        self.user_game_table[user_id] = {
            "channel_id": channel_id,
            "arena": new_arena.to_dict(),
        }
        logger.info("New arena: %s", new_arena.to_dict())
        return self.user_game_table[user_id]

    def get_channel_from_user_id(self, user_id: str) -> dict:
        channel = self.user_game_table.get(user_id)
        if channel is None:
            return None
        channel_id = channel["channel_id"]
        arena_id = channel["arena"]["id"]
        arena = self.channels[channel_id][arena_id]
        channel = {"channel_id": channel_id, "arena": arena.to_dict()}
        return channel

    def delete_arena(self, arenas: dict, arena_id: int):
        player_list = arenas[arena_id].get_players()
        for player in player_list.values():
            self.delete_user(player.user_id)
        arenas.pop(arena_id)

    def add_user(self, user_id: str, channel_id: str, arena_id: int):
        self.user_game_table[user_id] = {
            "channel_id": channel_id,
            "arena": self.channels[channel_id][arena_id].to_dict(),
        }

    def delete_user(self, user_id: str):
        try:
            self.user_game_table.pop(user_id)
            logger.info("User %s deleted from user_game_table", user_id)
        except KeyError:
            pass

    def is_user_in_game(self, user_id: str, channel_id: str, arena_id: int) -> dict:
        return self.user_game_table.get(user_id) == {
            "channel_id": channel_id,
            "arena": arena_id,
        }

    def delete_channel(self, channel_id: str):
        del self.channels[channel_id]

    async def monitor_arenas_loop(self, channel_id: str, arenas: dict):
        while arenas:
            await self.update_game_states(arenas)
            await asyncio.sleep(MONITOR_LOOP_INTERVAL)
        self.delete_channel(channel_id)

    async def update_game_states(self, arenas: dict):
        for arena in arenas.values():
            if arena.get_status() == STARTED and arena.is_empty():
                arena.conclude_game()
            if arena.get_status() == OVER:
                logger.info("Game over in arena %s", arena.id)
                await self.game_over(arenas, arena)
                break

    async def run_game_loop(self, arenas: dict):
        while arenas:
            for arena in arenas:
                if arena.get_status() == STARTED:
                    update_message = arena.update_game()
                    await arena.game_update_callback(update_message)
            await asyncio.sleep(RUN_LOOP_INTERVAL)

    async def game_over(self, arenas: dict, arena: Arena):
        arena.set_status(DYING)
        time = TIMEOUT_GAME_OVER + 1
        while arena.get_status() == DYING and time > 0:
            time -= TIMEOUT_INTERVAL
            await arena.game_over_callback("Game Over! Thank you for playing.", time)
            if time == 0:
                arena.set_status(DEAD)
                self.delete_arena(arenas, arena.id)
            else:
                await asyncio.sleep(TIMEOUT_INTERVAL)


monitor = Monitor()
