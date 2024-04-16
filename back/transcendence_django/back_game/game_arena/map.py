from back_game.game_settings.game_constants import GAME_WIDTH, GAME_HEIGHT

class Map:
   def __init__(self): # TODO Map size and shape depends on number of player
      self.width = GAME_WIDTH
      self.height = GAME_HEIGHT

   def update(self, newWidth, newHeight):
      self.width = newWidth
      self.height = newHeight

   def to_dict(self):
      return {
         'width': self.width,
         'height': self.height
      }
