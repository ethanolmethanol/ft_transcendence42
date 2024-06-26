import logging
from typing import Any

from back_game.game_entities.ball_speed_randomizer import BallSpeedRandomizer
from back_game.game_entities.paddle import Paddle
from back_game.game_geometry.position import Position
from back_game.game_physics.speed import Speed
from back_game.game_settings.dict_keys import (
    BALL_X_OUT_OF_BOUNDS,
    BALL_Y_OUT_OF_BOUNDS,
    POSITION,
    RADIUS,
    SPEED,
)
from back_game.game_settings.game_constants import BALL_RADIUS, GAME_HEIGHT, GAME_WIDTH

logger = logging.getLogger(__name__)


class Ball:

    def __init__(self, paddles: dict[str, Paddle]):
        self.position: Position = Position(GAME_WIDTH / 2, GAME_HEIGHT / 2)
        self.radius: float = BALL_RADIUS
        self.paddles: dict[str, Paddle] = paddles
        self.player_turn = 0
        self.speed = BallSpeedRandomizer.generate_random_speed(self.player_turn)

    def update(self, new_position: Position, new_speed: Speed, new_radius: float):
        self.position.set_coordinates(new_position.x, new_position.y)
        self.speed.update(new_speed)
        self.radius = new_radius

    def to_dict(self) -> dict[str, Any]:
        return {
            POSITION: self.position.__dict__,
            SPEED: self.speed.__dict__,
            RADIUS: self.radius,
        }

    def set_position(self, position: Position):
        x = position.x
        y = position.y
        if x < self.radius or x > GAME_WIDTH - self.radius:
            raise ValueError(BALL_X_OUT_OF_BOUNDS)
        if y < self.radius or y > GAME_HEIGHT - self.radius:
            raise ValueError(BALL_Y_OUT_OF_BOUNDS)
        self.position.set_coordinates(x, y)

    def get_next_position(self) -> Position:
        return Position(self.position.x + self.speed.x, self.position.y + self.speed.y)

    def reset(self):
        self.position = Position(GAME_WIDTH / 2, GAME_HEIGHT / 2)
        self.__set_random_speed()

    def __set_random_speed(self):
        self.speed = BallSpeedRandomizer.generate_random_speed(self.player_turn)
        self.player_turn = (self.player_turn + 1) % 2
