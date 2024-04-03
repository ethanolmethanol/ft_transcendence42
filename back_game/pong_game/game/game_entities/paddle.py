from game.game_settings.game_constants import *

from game.game_settings.game_constants import PADDLE_WIDTH, PADDLE_HEIGHT,\
    LEFT, RIGHT, GAME_WIDTH, GAME_HEIGHT

import math


class Paddle:
    def __init__(self, num_players, player_slot):
        self._player_slot = player_slot
        self._num_players = num_players
        self._axis = self.calculate_axis()
        self._position = self.calculate_initial_position()

    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, value):
        raise AttributeError("Use update_position() to set position")

    def update_position_with_delta(self, delta_y):
        new_y = self._position['y'] + delta_y
        new_y = max(0, min(GAME_HEIGHT - PADDLE_HEIGHT, new_y))
        self._position['y'] = new_y

    def calculate_axis(self):
        # Calculate the angle of the axis based on the player slot and the number of players
        angle = 2 * math.pi * self._player_slot / self._num_players

        # Calculate the start and end points of the axis
        start = {
            'x': GAME_WIDTH / 2 + GAME_WIDTH / 2 * math.cos(angle),
            'y': GAME_HEIGHT / 2 + GAME_HEIGHT / 2 * math.sin(angle)
        }
        end = {
            'x': GAME_WIDTH / 2 + GAME_WIDTH / 2 * math.cos(angle + math.pi),
            'y': GAME_HEIGHT / 2 + GAME_HEIGHT / 2 * math.sin(angle + math.pi)
        }

        return start, end

    def calculate_initial_position(self):
        # Calculate the initial position of the paddle as the midpoint of the axis
        return {
            'x': (self._axis[0]['x'] + self._axis[1]['x']) / 2,
            'y': (self._axis[0]['y'] + self._axis[1]['y']) / 2
        }