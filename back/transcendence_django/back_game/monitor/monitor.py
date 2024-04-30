import asyncio
from back_game.game_entities.ball import Ball
from back_game.game_entities.paddle import Paddle
from back_game.game_arena.map import Map
from back_game.game_arena.arena import Arena
from back_game.game_settings.game_constants import *
import logging
import random
import string

logger = logging.getLogger(__name__)
class Monitor:

    def __init__(self): #json
        self.channels = {} # key: channelID, value: dict [key: arenaID, value: arena]
        self.userGameTable = {}

    # def getGameConfig(self):
    #     return {k: v.to_dict() for k, v in self.gameConfig.items()}

    def generateRandomID(self, length):
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join(random.choice(letters_and_digits) for _ in range(length))

    async def getChannel(self, username, playerSpecs):
        channel = self.get_channel_from_username(username)
        if channel is None:
            return await self.getNewChannel(username, playerSpecs)
        return channel

    async def getNewChannel(self, username, playerSpecs):
        newArena = Arena(playerSpecs)
        channelID = self.generateRandomID(10)
        self.channels[channelID] = {newArena.id: newArena}
        asyncio.create_task(self.monitor_arenas_loop(channelID, self.channels[channelID]))
        asyncio.create_task(self.run_game_loop(channelID, self.channels[channelID].values()))
        self.userGameTable[username] = {"channelID": channelID, "arena": newArena.to_dict()}
        return self.userGameTable[username]

    def get_channel_from_username(self, username):
        channel = self.userGameTable.get(username)
        if channel is None:
            return None
        channelID = channel["channelID"]
        arenaID = channel["arena"]["id"]
        arena = self.channels[channelID][arenaID]
        channel = {"channelID": channelID, "arena": arena.to_dict()}
        return channel

    def deleteArena(self, arenas, arenaID):
        player_list = arenas.pop(arenaID).players
        for player in player_list.values():
            try:
                self.userGameTable.pop(player.owner_name)
            except KeyError:
                pass
        logger.info(f"userGameTable: {self.userGameTable}")
        logger.info(f"Deleting arena {arenaID}")
        logger.info(f"userGameTable: {self.userGameTable}")

    async def monitor_arenas_loop(self, channelID, arenas):
        while True:
            await self.update_game_states(arenas)
            await asyncio.sleep(1)

    async def update_game_states(self, arenas):
        arenas_values_copy = list(self.arenas.values())
        for arena in arenas_values_copy:
            logger.info(f"Status of arena {arena.id} is {arena.status}")
            if arena.status == DEAD:
                logger.info(f"Deleting arena {arena.id}")
                self.deleteArena(arenas, arena.id)
            elif (arena.status == STARTED and arena.is_empty()):
                arena.status = DEAD
            elif arena.status == OVER:
                logger.info(f"Game over in arena {arena.id}")
                await self.gameOver(arena)

    async def run_game_loop(self, channelID, arenas):
        while any(arena.status != DEAD for arena in arenas):
            for arena in arenas:
                if arena.status == STARTED:
                    update_message = arena.update_game()
                    await arena.game_update_callback(update_message)
            await asyncio.sleep(0.01)

    async def gameOver(self, arena):
        if hasattr(arena, 'game_over_callback'):
            await arena.game_over_callback('Game Over! Thank you for playing.')
        arena.status = DYING
        await asyncio.sleep(10)
        if arena.status == DYING:
            arena.status = DEAD
        logger.info(f"Status of arena {arena.id} is {arena.status}")


monitor = Monitor()
