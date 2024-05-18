import logging
import math

from typing import NewType
from back_game.game_physics.position import Position
from back_game.game_physics.rectangle import Rectangle
from back_game.game_physics.vector import Vector
from back_game.game_settings.game_constants import (
    GAME_HEIGHT,
    GAME_WIDTH,
    INITIAL_BALL_SPEED_COEFF,
    LEFT_SLOT,
    LISTENING,
    PADDLE_HEIGHT,
    PADDLE_INITIAL_SPEED_RATE,
    PADDLE_OFFSET,
    PADDLE_WIDTH,
    PROCESSING,
    RIGHT_SLOT,
)

log = logging.getLogger(__name__)

PaddleStatus = NewType("PaddleStatus", [LISTENING, PROCESSING])

class Paddle:
    def __init__(self, slot: int, num_players: int):
        self.slot: int = slot
        self.status: PaddleStatus = LISTENING
        self.speed: float = PADDLE_INITIAL_SPEED_RATE
        self.rectangle: Rectangle = Rectangle(slot, Position(0, 0), PADDLE_WIDTH, PADDLE_HEIGHT)
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
        return {"start": start.round(), "end": end.round()}

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
        return {"start": start.round(), "end": end.round()}

    def __convert_rate_to_position(self, rate: float) -> Position:
        return Position(
            self.axis["start"].x + (self.axis["end"].x - self.axis["start"].x) * rate,
            self.axis["start"].y + (self.axis["end"].y - self.axis["start"].y) * rate,
        ).round()

    def to_dict(self) -> dict:
        return {
            "slot": self.slot,
            "position": self.rectangle.position.__dict__,
            "speed": self.speed,
            "width": self.rectangle.width,
            "height": self.rectangle.height,
        }

    def get_dict_update(self) -> dict:
        return {
            "slot": self.slot,
            "position": self.rectangle.position.__dict__,
        }

    def get_edges(self) -> dict[str, Position]:
        return self.rectangle.edges

    def get_position(self) -> Position:
        return self.rectangle.position

    def reset(self):
        self.rate = 0.5
        self.__update_position()

    def update(self, config: dict):
        self.rectangle.width = config["width"]
        self.rectangle.height = config["height"]

    def move(self, direction: int):
        self.rate = min(max(self.rate + self.speed * direction, 0), 1)
        self.__update_position()

    def get_ball_speed_after_paddle_collision(self, collision_point: Position) -> Vector:
        speed_component = self.__get_ball_speed_direction(collision_point)
        u_speed = speed_component.unit_vector()
        return Vector(
            INITIAL_BALL_SPEED_COEFF * u_speed.x, INITIAL_BALL_SPEED_COEFF * u_speed.y
        )

    def __get_ball_speed_direction(self, collision_point: Position) -> Vector:
        if self.slot == LEFT_SLOT:
            speed_component_x = self.rectangle.distance_from_center
        elif self.slot == RIGHT_SLOT:
            speed_component_x = (-1) * self.rectangle.distance_from_center
        speed_component_y = collision_point.y - self.rectangle.convexity_center.y
        return Vector(speed_component_x, speed_component_y)
