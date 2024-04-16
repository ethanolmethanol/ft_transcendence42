from back_game.game_settings.game_constants import PADDLE_INITIAL_SPEED_RATE, PADDLE_HEIGHT, PADDLE_WIDTH, GAME_WIDTH, GAME_HEIGHT
import math
from back_game.game_physics.position import Position
from back_game.game_physics.vector import Vector

import logging
log = logging.getLogger(__name__)
class Paddle:
   def __init__(self, slot=1, num_players=2):
      self.slot = slot
      self.speed = PADDLE_INITIAL_SPEED_RATE
      self.width = PADDLE_WIDTH
      self.height = PADDLE_HEIGHT
      self.axis = self.__calculate_axis(num_players)
      self.position = self.__convert_rate_to_position(0.5)
      log.info(f"Paddle created at {self.position.to_dict()}")

   def __calculate_axis(self, num_players):
      # Calculate the angle of the axis based on the player slot and the number of players
      angle = math.pi * (self.slot - 1)

      # Calculate the start and end points of the axis
      start = Position(
         GAME_HEIGHT / 2 + GAME_HEIGHT / 2 * math.sin(angle),
         GAME_WIDTH / 2 + GAME_WIDTH / 2 * math.cos(angle)
      )
      end = Position(
         GAME_HEIGHT / 2 + GAME_HEIGHT / 2 * math.sin(angle + math.pi),
         GAME_WIDTH / 2 + GAME_WIDTH / 2 * math.cos(angle + math.pi)
      )
      log.info(f"Slot: {self.slot}, Angle: {angle}, Start: {start.to_dict()}, End: {end.to_dict()}")
      return {'start': start, 'end': end}

   def __convert_rate_to_position(self, rate):
      # Ensure the rate is between 0 and 1
      if not (0 <= rate <= 1):
          raise ValueError("Rate must be between 0 and 1.")

      # Calculate the position using linear interpolation
      return Position (
         round(self.axis['start'].x + (self.axis['end'].x - self.axis['start'].x) * rate),
         round(self.axis['start'].y + (self.axis['end'].y - self.axis['start'].y) * rate)
      )

   def to_dict(self):
      return {
         'slot': self.slot,
         'position': self.position.to_dict(),
         'speed': self.speed,
         'width': self.width,
         'height': self.height
      }

   def update(self, config):
      # self.speed.setCoordinates(config['x'], config['y'])
      self.width = config['width']
      self.height = config['height']

   def move(self, rate):
      self.position = self.__convert_rate_to_position(rate)
