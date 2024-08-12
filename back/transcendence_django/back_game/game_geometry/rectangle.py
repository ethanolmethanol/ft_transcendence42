from typing import Any

from back_game.game_geometry.edges import Edges
from back_game.game_geometry.position import Position
from back_game.game_settings.game_constants import LEFT_SLOT, RIGHT_SLOT, TOP_SLOT, BOT_SLOT, TANGENT_FACTOR
from transcendence_django.dict_keys import HEIGHT, POSITION, WIDTH


class Rectangle:
    def __init__(self, slot: int, position: Position, width: int, height: int):
        self.slot: int = slot
        self.position: Position = position
        if self.slot == LEFT_SLOT or self.slot == RIGHT_SLOT:
            self.width: int = width
            self.height: int = height
        else: # for horizontal paddles (aka top and bot)
            self.width: int = height
            self.height: int = width
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
        elif self.slot == BOT_SLOT: #TODO test when handling >2 players
            center_y = self.edges.top - self.distance_from_center
        elif self.slot == TOP_SLOT: #TODO test when handling >2 players
            center_y = self.edges.bottom + self.distance_from_center
        else:
            raise Exception("Oopsie! Too many paddles?")
        return Position(center_x, center_y)
