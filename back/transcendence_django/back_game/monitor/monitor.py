import asyncio
import json
from back_game.game_entities.ball import Ball
from back_game.game_entities.paddle import Paddle
from back_game.game_arena.map import Map
from back_game.game_arena.playerMode import PlayerMode
from back_game.game_arena.arena import Arena
from back_game.monitor.game_engine_singleton import gameEngine

import logging
logger = logging.getLogger(__name__)
class Monitor:

    arenas = {}
    def __init__(self, gameData): #json
        self.gameConfig = {
          "playerMode": PlayerMode(),
          "paddle": Paddle(),
          "ball": Ball(),
          "map": Map(),
        }
        for key in gameData.keys():
            if key in self.gameConfig:
                self.gameConfig[key].update(gameData[key])
            else:
                raise ValueError(f"Key '{key}' not found in gameConfig.")

    def getGameConfig(self):
        return {k: v.to_dict() for k, v in self.gameConfig.items()}

    async def getNewArena(self):
      newArena = Arena(self.gameConfig)
      self.arenas[newArena.id] = newArena
      # add the new arena to the gameEngine
      await gameEngine.addArena(newArena)
      await gameEngine.start()
      return {"arenaID": newArena.id}

    def deleteArena(self, id):
        for elt in self.arenas:
            if elt.id == id:
                self.arenas.remove(elt)
                break