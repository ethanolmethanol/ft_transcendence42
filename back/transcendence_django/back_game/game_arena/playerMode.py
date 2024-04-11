from back_game.game_settings.game_constants import LOCAL_MODE

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
