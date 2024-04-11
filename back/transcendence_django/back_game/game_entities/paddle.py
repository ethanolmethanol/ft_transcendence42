#from game.game_settings.game_constants import *

#from game.game_settings.game_constants import PADDLE_WIDTH, PADDLE_HEIGHT, GAME_WIDTH, GAME_HEIGHT

# import math


# class Paddle:
#     def __init__(self, num_players, player_slot):
#         self._player_slot = player_slot
#         self._num_players = num_players
#         self._axis = self.calculate_axis()
#         self._position = self.calculate_initial_position()

#     @property
#     def position(self):
#         return self._position

#     @position.setter
#     def position(self, value):
#         raise AttributeError("Use update_position() to set position")

#     def calculate_axis(self):
#         # Calculate the angle of the axis based on the player slot and the number of players
#         angle = 2 * math.pi * self._player_slot / self._num_players

#         # Calculate the start and end points of the axis
#         start = {
#             'x': GAME_WIDTH / 2 + GAME_WIDTH / 2 * math.cos(angle),
#             'y': GAME_HEIGHT / 2 + GAME_HEIGHT / 2 * math.sin(angle)
#         }
#         end = {
#             'x': GAME_WIDTH / 2 + GAME_WIDTH / 2 * math.cos(angle + math.pi),
#             'y': GAME_HEIGHT / 2 + GAME_HEIGHT / 2 * math.sin(angle + math.pi)
#         }

#         return start, end

#     def calculate_initial_position(self):
#         # Calculate the initial position of the paddle as the midpoint of the axis
#         return {
#             'x': (self._axis[0]['x'] + self._axis[1]['x']) / 2,
#             'y': (self._axis[0]['y'] + self._axis[1]['y']) / 2
#         }

#     def calculate_position_with_progression(self, percentage):
#         # Ensure the percentage is between 0 and 100
#         if not (0 <= percentage <= 100):
#             raise ValueError("Percentage must be between 0 and 100.")

#         # Convert the percentage to a decimal
#         percentage /= 100

#         # Calculate the position using linear interpolation
#         return {
#             'x': round(self._axis[0]['x'] + (self._axis[1]['x'] - self._axis[0]['x']) * percentage),
#             'y': round(self._axis[0]['y'] + (self._axis[1]['y'] - self._axis[0]['y']) * percentage)
#         }

#     def move(self, percentage):
#         self._position = self.calculate_position_with_progression(percentage);

from back_game.game_physics.vector import Vector

class Paddle:
   def __init__(self, slot=0):
      self.slot = slot
      self.speed = Vector(1, 1)
      self.width = 5
      self.height = 50

   def update(self, config):
      self.speed.setCoordinates(config['x'], config['y'])
      self.width = config['width']
      self.height = config['height']

   def to_dict(self):
      return {
         'slot': self.slot,
         'speed': self.speed.to_dict(),
         'width': self.width,
         'height': self.height
      }
