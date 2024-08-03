import logging
from typing import Any

from back_game.game_entities.ball_speed_randomizer import BallSpeedRandomizer
from back_game.game_entities.paddle import Paddle
from back_game.game_geometry.position import Position
from back_game.game_physics.speed import Speed
from back_game.game_settings.game_constants import BALL_RADIUS, GAME_HEIGHT, GAME_WIDTH
from transcendence_django.dict_keys import (
    BALL_X_OUT_OF_BOUNDS,
    BALL_Y_OUT_OF_BOUNDS,
    POSITION,
    RADIUS,
    SPEED,
)

logger = logging.getLogger(__name__)

speed_rate = {
    0: 2,
    1: 5,
    2: 8,
    3: 14,
    4: 20,
}


class Ball:

    def __init__(self, paddles: dict[str, Paddle], speed_index: int):
        self.position: Position = Position(GAME_WIDTH / 2, GAME_HEIGHT / 2)
        self.radius: float = BALL_RADIUS
        self.paddles: dict[str, Paddle] = paddles
        self.player_turn = 0
        self.speed = Speed(0, 0)
        self.speed_rate = speed_rate[speed_index]
        self.__set_random_speed()

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

    def set_speed(self, speed: Speed):
        speed.multiply_by_scalar(self.speed_rate)
        logger.info("New speed is: %s", speed.__dict__)
        self.speed.update(speed)

    def reset(self):
        self.position = Position(GAME_WIDTH / 2, GAME_HEIGHT / 2)
        self.__set_random_speed()

    def __set_random_speed(self):
        self.set_speed(BallSpeedRandomizer.generate_random_speed(self.player_turn))
        self.player_turn = (self.player_turn + 1) % 2
