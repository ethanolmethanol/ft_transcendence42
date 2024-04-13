import asyncio
from back_game.game_entities.ball import Ball
from back_game.game_entities.paddle import Paddle
from back_game.game_arena.map import Map
from back_game.game_arena.arena import Arena
from back_game.game_settings.game_constants import *
import logging
import uuid

logger = logging.getLogger(__name__)
class Monitor:

    def __init__(self): #json
        self.channels = {} # key: channelID, value: dict [key: arenaID, value: arena]

    # def getGameConfig(self):
    #     return {k: v.to_dict() for k, v in self.gameConfig.items()}

    def getUniqueID(self):
        return uuid.uuid4().int

    async def getNewChannel(self, playerSpecs):
      newArena = Arena(playerSpecs)
      channelID = self.getUniqueID()
      self.channels[channelID] = {newArena.id: newArena}
      asyncio.create_task(self.run_game_loop(channelID, self.channels[channelID].values()))
      return {"channelID": channelID, "arenaID": newArena.id}

    def deleteArena(self, channelID, arenaID):
        del self.channels[channelID][arenaID]

    async def run_game_loop(self, channelID, arenas):
        while any(arena.status != DEAD for arena in arenas):
            await self.update_game_states(arenas)
            await asyncio.sleep(1)
        del self.channels[channelID]

    async def update_game_states(self, arenas):
        for arena in arenas:
            if arena.status == DEAD:
                del arenas[arena.id]
            elif (arena.status == STARTED and len(arena.players) == 1):
                # make the only one player win and set the status to over
                pass
            elif (arena.status == STARTED and arena.isEmpty())\
                or arena.status == OVER:
                await self.gameOver(arena)
            
    async def gameOver(self, arena):
        arena.status = OVER
        if hasattr(arena, 'game_over_callback'):
            await arena.game_over_callback('Game Over! Thank you for playing.')

monitor = Monitor()