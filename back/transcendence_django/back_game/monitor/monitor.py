import json
import uuid
from back_game.game_entities.ball import Ball
from back_game.game_entities.paddle import Paddle
from back_game.game_arena.map import Map
from back_game.game_arena.playerMode import PlayerMode
from back_game.game_arena.arena import Arena

class Monitor:
    gameConfig = {
      "playerMode": PlayerMode(),
      "paddle": Paddle(),
      "ball": Ball(),
      "map": Map(),
    }

    def __init__(self, gameData): #json
        for key in gameData.keys():
            if key in self.gameConfig:
                self.gameConfig[key].update(gameData[key])
            else:
                raise ValueError(f"Key '{key}' not found in gameConfig.")

    def getGameConfig(self):
        return {k: v.to_dict() for k, v in self.gameConfig.items()}

    def getNewArena(self):
      unique_id = 42#str(uuid.uuid4())
      newArena = Arena(self.gameConfig)
      print(newArena)
      # self.arenas[unique_id] = Arena()
      # returns the Arena id
      return {"arenaID": unique_id}
