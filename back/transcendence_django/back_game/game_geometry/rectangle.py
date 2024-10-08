from typing import Any

from back_game.game_geometry.edges import Edges
from back_game.game_geometry.position import Position
from back_game.game_settings.game_constants import (
    BOTTOM_SLOT,
    LEFT_SLOT,
    RIGHT_SLOT,
    TANGENT_FACTOR,
    TOP_SLOT,
)
from transcendence_django.dict_keys import HEIGHT, POSITION, WIDTH


class Rectangle:
    def __init__(self, slot: int, position: Position, width: int, height: int):
        self.slot: int = slot
        self.position: Position = position
        self.width: int = width
        self.height: int = height
        if self.slot not in (LEFT_SLOT, RIGHT_SLOT):
            self.width = height
            self.height = width
        self.edges: Edges = Edges(position, width, height)
        self.convexity_center: Position = self.__get_convexity_center()
        self.distance_from_center: float = 0

    def to_dict(self) -> dict[str, Any]:
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
        self.distance_from_center = self.height * TANGENT_FACTOR
        center_x, center_y = self.position.x, self.position.y
        if self.slot == LEFT_SLOT:
            center_x = self.edges.right - self.distance_from_center
        elif self.slot == RIGHT_SLOT:
            center_x = self.edges.left + self.distance_from_center
        elif self.slot == BOTTOM_SLOT:
            center_y = self.edges.top - self.distance_from_center
        elif self.slot == TOP_SLOT:
            center_y = self.edges.bottom + self.distance_from_center
        else:
            raise ValueError("Oopsie! Too many paddles?")
        return Position(center_x, center_y)
