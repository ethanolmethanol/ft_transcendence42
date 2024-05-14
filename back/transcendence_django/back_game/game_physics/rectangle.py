import math

from back_game.game_physics.edges import Edges
from back_game.game_settings.game_constants import CONVEXITY, LEFT_SLOT, RIGHT_SLOT
from back_game.game_physics.position import Position


class Rectangle:
    def __init__(self, slot, position, width, height):
        self.slot = slot
        self.position = position
        self.width = width
        self.height = height
        self.edges = Edges(position, width, height)
        self.convexity_center = self.__get_convexity_center()
        self.distance_from_center = None

    def to_dict(self):
        return {
            "position": self.position.to_dict(),
            "width": self.width,
            "height": self.height,
        }

    def update_position(self, position):
        self.position = position
        self.edges.update(position, self.width, self.height)
        self.convexity_center = self.__get_convexity_center()

    def __get_convexity_center(self):
        self.distance_from_center = self.height / (2 * math.tan(CONVEXITY / 2))
        if self.slot == LEFT_SLOT:
            center_x = self.edges.right - self.distance_from_center
        elif self.slot == RIGHT_SLOT:
            center_x = self.edges.left + self.distance_from_center
        return Position(center_x, self.position.y)
