import json
from game.game_settings.game_constants import LOCAL_MODE

class Position:
   def __init__(self, x=0, y=0):
      self.x = x
      self.y = y

   def setCoordinates(self, x, y):
      self.x = x
      self.y = y

class Vector(Position):

   def __init__(self, x=0, y=0):
      super().__init__(x, y)

class PlayerMode:
   def __init__(self):
      self.nbPlayers = 2
      self.mode = LOCAL_MODE

   def update(self, nbPlayers, mode):
      self.nbPlayers = nbPlayers
      self.mode = mode

class Paddle:
   def __init__(self):
      self.position = Position()
      self.speed = Vector(1, 1)
      self.width = 5
      self.height = 50

   def update(self, x, y):
      self.speed.setCoordinates(x, y)

class Ball:
   def __init__(self):
      self.position = Position()
      self.speed = Vector(1, 1)
      self.radius = 2

   def update(self, newPosition, newSpeed, newRadius):
      self.position.setCoordinates(newPosition.x, newPosition.y)
      self.speed.setCoordinates(newSpeed.x, newSpeed.y)
      self.radius = newRadius

class Map:
    def __init__(self):
      self.width = 900
      self.height = 500

    def update(self, newWidth, newHeight):
        self.width = newWidth
        self.height = newHeight

class Monitor:
    game_config = {
      "playerMode": PlayerMode(),
      "paddle": Paddle(),
      "ball": Ball(),
      "map": Map(),
    }

    def __init__(self, json_game_data):
        game_data = json.loads(json_game_data)
        for key in game_data.keys():
            if key in self.game_config:
                self.game_config[key].update(game_data[key])
            else:
                raise ValueError(f"Key '{key}' not found in game_config.")


# json_game_data = '{ "playerMode": {"nbPlayer, mode"}, "paddle": {"height": 10, "width": 10}, "ball": {"speed": {"x": 1, "y": 2}, "radius": 5}}'
