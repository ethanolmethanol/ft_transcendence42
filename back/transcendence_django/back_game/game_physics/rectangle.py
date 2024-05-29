import math

from back_game.game_physics.edges import Edges
from back_game.game_settings.game_constants import CONVEXITY, LEFT_SLOT, RIGHT_SLOT
from back_game.game_physics.position import Position
from back_game.game_settings.dict_keys import (
    POSITION,
    WIDTH,
    HEIGHT,
)

class Rectangle:
    def __init__(self, slot: int, position: Position, width: int, height: int):
        self.slot: int = slot
        self.position: Position = position
        self.width: int = width
        self.height: int = height
        self.edges: Edges = Edges(position, width, height)
        self.convexity_center: Position = self.__get_convexity_center()
        self.distance_from_center: int = 0

    def to_dict(self) -> dict:
        return {
            POSITION: self.position.__dict__,
            WIDTH: self.width,
            HEIGHT: self.height,
        }

    def update_position(self, position: Position):
        self.position = position
        self.edges.update(position, self.width, self.height)
        self.convexity_center = self.__get_convexity_center()

    def __get_convexity_center(self) -> Position:
        self.distance_from_center = self.height / (2 * math.tan(CONVEXITY / 2))
        if self.slot == LEFT_SLOT:
            center_x = self.edges.right - self.distance_from_center
        elif self.slot == RIGHT_SLOT:
            center_x = self.edges.left + self.distance_from_center
        return Position(center_x, self.position.y)
