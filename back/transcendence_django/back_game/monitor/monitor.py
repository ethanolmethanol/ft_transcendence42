import json
import uuid
from ..game_settings.game_constants import LOCAL_MODE

class Position:
   def __init__(self, x=0, y=0):
      self.x = x
      self.y = y

   def setCoordinates(self, x, y):
      self.x = x
      self.y = y

   def to_dict(self):
      return {
         'x': self.x,
         'y': self.y
      }

class Vector(Position):

   def __init__(self, x=0, y=0):
      super().__init__(x, y)

class PlayerMode:
   def __init__(self):
      self.nbPlayers = 2
      self.mode = LOCAL_MODE

   def update(self, config):
      self.nbPlayers = config['nbPlayers']
      self.mode = config['mode']

   def to_dict(self):
        return {
            'nbPlayers': self.nbPlayers,
            'mode': self.mode
        }

class Paddle:
   def __init__(self):
      self.position = Position()
      self.speed = Vector(1, 1)
      self.width = 5
      self.height = 50

   def update(self, config):
      self.speed.setCoordinates(config['x'], config['y'])

   def to_dict(self):
      return {
         'position': self.position.to_dict(),
         'speed': self.speed.to_dict()
      }

class Ball:
   def __init__(self):
      self.position = Position()
      self.speed = Vector(1, 1)
      self.radius = 2

   def update(self, newPosition, newSpeed, newRadius):
      self.position.setCoordinates(newPosition.x, newPosition.y)
      self.speed.setCoordinates(newSpeed.x, newSpeed.y)
      self.radius = newRadius

   def to_dict(self):
      return {
         'position': self.position.to_dict(),
         'speed': self.speed.to_dict()
      }

class Map:
   def __init__(self):
      self.width = 900
      self.height = 500

   def update(self, newWidth, newHeight):
      self.width = newWidth
      self.height = newHeight

   def to_dict(self):
      return {
         'width': self.width,
         'height': self.height
      }


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
      # self.arenas[unique_id] = Arena()
      # returns the Arena id
      return {"arenaID": unique_id}
