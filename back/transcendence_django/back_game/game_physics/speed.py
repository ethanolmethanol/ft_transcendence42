import math

from back_game.game_physics.vector import Vector


class Speed(Vector):

    def __init__(self, speed_x, speed_y):
        self.x = speed_x
        self.y = speed_y
        self.absolute_velocity = self.magnitude()

    def update(self, new_speed: 'Speed'):
        self.x = new_speed.x
        self.y = new_speed.y
        self.absolute_velocity = new_speed.absolute_velocity