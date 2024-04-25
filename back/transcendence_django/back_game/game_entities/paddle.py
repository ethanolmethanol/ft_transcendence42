from back_game.game_settings.game_constants import LISTENING, PADDLE_OFFSET, PADDLE_INITIAL_SPEED_RATE, PADDLE_HEIGHT, PADDLE_WIDTH, GAME_WIDTH, GAME_HEIGHT
import math
from back_game.game_physics.position import Position

import logging
log = logging.getLogger(__name__)
class Paddle:
   def __init__(self, slot=1, num_players=2):
      self.slot = slot
      self.status = LISTENING
      self.speed = PADDLE_INITIAL_SPEED_RATE
      self.width = PADDLE_WIDTH
      self.height = PADDLE_HEIGHT
      self.rate = 0.5
      self.axis = self.__calculate_axis(num_players)
      self.__update_position()
      log.info(f"Paddle created at {self.position.to_dict()}")

   def __update_position(self):
      self.position = self.__convert_rate_to_position(self.rate)
      self.bottom = self.position.y + self.height / 2
      self.top = self.position.y - self.height / 2
      self.left = self.position.x - self.width / 2
      self.right = self.position.x + self.width / 2

   def __calculate_axis(self, num_players):
      if (num_players == 2):
         return self.__calculate_axis_2_players()
      else:
         return self.__calculate_regular_axis(num_players)

   def __calculate_axis_2_players(self):
      demi_height = self.height / 2
      if (self.slot == 1):
         start = Position(PADDLE_OFFSET, demi_height)
         end = Position(PADDLE_OFFSET, GAME_HEIGHT - demi_height)
      else:
         start = Position(GAME_WIDTH - PADDLE_OFFSET, demi_height)
         end = Position(GAME_WIDTH - PADDLE_OFFSET, GAME_HEIGHT - demi_height)
      return {'start': start.round(), 'end': end.round()}

   def __calculate_regular_axis(self, num_players):
      # Calculate the angle of the axis based on the player slot and the number of players
      angle =  2 * math.pi * (self.slot - 1) / num_players

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
      return {'start': start.round(), 'end': end.round()}

   def __convert_rate_to_position(self, rate):
      return Position(
         self.axis['start'].x + (self.axis['end'].x - self.axis['start'].x) * rate,
         self.axis['start'].y + (self.axis['end'].y - self.axis['start'].y) * rate
      ).round()


   def to_dict(self):
      return {
         'slot': self.slot,
         'position': self.position.to_dict(),
         'speed': self.speed,
         'width': self.width,
         'height': self.height,
      }

   def update(self, config):
      # self.speed.setCoordinates(config['x'], config['y'])
      self.width = config['width']
      self.height = config['height']

   def move(self, direction):
      self.rate = min(max(self.rate + self.speed * direction, 0), 1)
      self.__update_position()
