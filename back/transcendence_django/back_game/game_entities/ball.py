import logging
from typing import Callable

from back_game.game_entities.paddle import Paddle
from back_game.game_entities.ball_speed_randomizer import BallSpeedRandomizer
from back_game.game_physics.position import Position
from back_game.game_physics.speed import Speed
from back_game.game_settings.game_constants import (
    BALL_RADIUS,
    GAME_HEIGHT,
    GAME_WIDTH,
)
from back_game.game_settings.dict_keys import (
    POSITION,
    SPEED,
    RADIUS,
    BALL_X_OUT_OF_BOUNDS,
    BALL_Y_OUT_OF_BOUNDS,
)

logger = logging.getLogger(__name__)


class Ball:

    def __init__(self, paddles: dict, hit_wall_func: Callable[[int], dict[str, str]]):
        self.position: Position = Position(GAME_WIDTH / 2, GAME_HEIGHT / 2)
        self.radius: float = BALL_RADIUS
        self.paddles: dict = paddles
        self.hit_wall: Callable[[int], dict[str, str]] = hit_wall_func
        self.player_turn: int = 0
        self.speed: Speed = None
        self.__set_random_speed()

    def update(self, new_position: Position, new_speed: Speed, new_radius: float):
        self.position.set_coordinates(new_position.x, new_position.y)
        self.speed.update(new_speed)
        self.radius = new_radius

    def to_dict(self) -> dict:
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

    def move(self) -> dict:
        new_position = Position(
            self.position.x + self.speed.x, self.position.y + self.speed.y
        )
        update = Collision.detect_collision(new_position, self)
        logger.info("UPDATE COLISION: %s", update)
        return update

    def update_collision(self, paddle: Paddle):
        logger.info("UPDATE PADDLE COLISION BRO")
        if Collision.is_paddle_collision(self, paddle):
            Collision.handle_collision(self.position, self)

    def reset(self):
        self.position = Position(GAME_WIDTH / 2, GAME_HEIGHT / 2)
        self.__set_random_speed()

    def __set_random_speed(self):
        self.speed = BallSpeedRandomizer.generate_random_speed(self.player_turn)
        self.player_turn = (self.player_turn + 1) % 2

from back_game.game_physics.collision import Collision
