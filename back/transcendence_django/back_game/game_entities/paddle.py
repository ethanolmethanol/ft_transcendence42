import logging
import math
from typing import Any, NewType

from back_game.game_geometry.edges import Edges
from back_game.game_geometry.position import Position
from back_game.game_geometry.rectangle import Rectangle
from back_game.game_settings.dict_keys import (
    END,
    HEIGHT,
    POSITION,
    SLOT,
    SPEED,
    START,
    WIDTH,
)
from back_game.game_settings.game_constants import (
    GAME_HEIGHT,
    GAME_WIDTH,
    LISTENING,
    PADDLE_HEIGHT,
    PADDLE_INITIAL_SPEED_RATE,
    PADDLE_OFFSET,
    PADDLE_WIDTH,
)

log = logging.getLogger(__name__)

PaddleStatus = NewType("PaddleStatus", int)


class Paddle:
    def __init__(self, slot: int, num_players: int):
        self.slot: int = slot
        self.status: PaddleStatus = PaddleStatus(LISTENING)
        self.speed_rate: float = PADDLE_INITIAL_SPEED_RATE
        self.rectangle: Rectangle = Rectangle(
            slot, Position(0, 0), PADDLE_WIDTH, PADDLE_HEIGHT
        )
        self.rate: float = 0.5
        self.axis: dict[str, Position] = self.__calculate_axis(num_players)
        self.__update_position()
        log.info("Paddle created at %s", self.rectangle.position.__dict__)

    def __update_position(self):
        new_position = self.__convert_rate_to_position(self.rate)
        self.rectangle.update_position(new_position)

    def __calculate_axis(self, num_players: int) -> dict[str, Position]:
        if num_players == 2:
            return self.__calculate_axis_2_players()
        return self.__calculate_regular_axis(num_players)

    def __calculate_axis_2_players(self) -> dict[str, Position]:
        demi_height: float = self.rectangle.height / 2
        if self.slot == 1:
            start = Position(PADDLE_OFFSET, demi_height)
            end = Position(PADDLE_OFFSET, GAME_HEIGHT - demi_height)
        else:
            start = Position(GAME_WIDTH - PADDLE_OFFSET, demi_height)
            end = Position(GAME_WIDTH - PADDLE_OFFSET, GAME_HEIGHT - demi_height)
        return {START: start.round(), END: end.round()}

    def __calculate_regular_axis(self, num_players: int) -> dict[str, Position]:
        angle: float = 2 * math.pi * (self.slot - 1) / num_players

        start = Position(
            GAME_HEIGHT / 2 + GAME_HEIGHT / 2 * math.sin(angle),
            GAME_WIDTH / 2 + GAME_WIDTH / 2 * math.cos(angle),
        )
        end = Position(
            GAME_HEIGHT / 2 + GAME_HEIGHT / 2 * math.sin(angle + math.pi),
            GAME_WIDTH / 2 + GAME_WIDTH / 2 * math.cos(angle + math.pi),
        )
        log.info(
            "Slot: %s, Angle: %s, Start: %s, End: %s",
            self.slot,
            angle,
            start.__dict__,
            end.__dict__,
        )
        return {START: start.round(), END: end.round()}

    def __convert_rate_to_position(self, rate: float) -> Position:
        return Position(
            self.axis[START].x + (self.axis[END].x - self.axis[START].x) * rate,
            self.axis[START].y + (self.axis[END].y - self.axis[START].y) * rate,
        ).round()

    def to_dict(self) -> dict[str, Any]:
        return {
            SLOT: self.slot,
            POSITION: self.rectangle.position.__dict__,
            SPEED: self.speed_rate,
            WIDTH: self.rectangle.width,
            HEIGHT: self.rectangle.height,
        }

    def get_dict_update(self) -> dict[str, Any]:
        return {
            SLOT: self.slot,
            POSITION: self.rectangle.position.__dict__,
        }

    def get_edges(self) -> Edges:
        return self.rectangle.edges

    def get_position(self) -> Position:
        return self.rectangle.position

    def reset(self):
        self.rate = 0.5
        self.__update_position()

    def update(self, config: dict[str, Any]):
        self.rectangle.width = config[WIDTH]
        self.rectangle.height = config[HEIGHT]

    def move(self, direction: int):
        self.rate = min(max(self.rate + self.speed_rate * direction, 0), 1)
        self.__update_position()
