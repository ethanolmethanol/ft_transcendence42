import logging
import math
import random
from typing import Callable

from back_game.game_entities.paddle import Paddle
from back_game.game_physics.position import Position
from back_game.game_physics.speed import Speed
from back_game.game_settings.game_constants import (
    BALL_RADIUS,
    GAME_HEIGHT,
    GAME_WIDTH,
    INITIAL_SPEED_X,
    INITIAL_SPEED_Y,
)

logger = logging.getLogger(__name__)

random_ball_speeds = [
    {
        Speed(-INITIAL_SPEED_X, 0),
        Speed(-INITIAL_SPEED_X, -INITIAL_SPEED_Y / 2),
        Speed(-INITIAL_SPEED_X, INITIAL_SPEED_Y / 2),
        Speed(-INITIAL_SPEED_X, INITIAL_SPEED_Y / 3),
        Speed(-INITIAL_SPEED_X, -INITIAL_SPEED_Y / 3),
    },
    {
        Speed(INITIAL_SPEED_X, 0),
        Speed(INITIAL_SPEED_X, -INITIAL_SPEED_Y / 2),
        Speed(INITIAL_SPEED_X, INITIAL_SPEED_Y / 2),
        Speed(INITIAL_SPEED_X, -INITIAL_SPEED_Y / 3),
    },
]


class Ball:

    def __init__(self, paddles: dict, hit_wall_func: Callable[[int], dict[str, str]]):
        self.position = Position(GAME_WIDTH / 2, GAME_HEIGHT / 2)
        self.radius = BALL_RADIUS
        self.paddles = paddles
        self.hit_wall = hit_wall_func
        self.player_turn = 0
        self.speed = None
        self.__set_random_speed()

    def update(self, new_position: Position, new_speed: Speed, new_radius: float):
        self.position.set_coordinates(new_position.x, new_position.y)
        self.speed.update(new_speed)
        self.radius = new_radius

    def to_dict(self) -> dict:
        return {
            "position": self.position.__dict__,
            "speed": self.speed.__dict__,
            "radius": self.radius,
        }

    def set_position(self, position: Position):
        x = position.x
        y = position.y
        if x < self.radius or x > GAME_WIDTH - self.radius:
            raise ValueError("Ball x-coordinate is out of bounds.")
        if y < self.radius or y > GAME_HEIGHT - self.radius:
            raise ValueError("Ball y-coordinate is out of bounds.")
        self.position.set_coordinates(x, y)

    def move(self) -> dict:
        new_position = Position(
            self.position.x + self.speed.x, self.position.y + self.speed.y
        )
        update = self.update_position(new_position)
        ball_position_update = {"ball": {"position": self.position.__dict__}}
        return (
            {**update, **ball_position_update}
            if update is not None
            else ball_position_update
        )

    def update_collision(self, paddle: Paddle):
        if self.is_paddle_collision(self.position, paddle):
            self.update_position(self.position)

    def update_position(self, new_position: Position) -> int | None:
        for paddle in self.paddles:
            if self.is_paddle_collision(self.position, paddle):
                self.__collide_with_paddle(paddle)
                return None
        score = self.__update_wall_collision(new_position)
        return score

    def is_paddle_collision(self, position: Position, paddle: Paddle) -> bool:
        """
        Checks if the ball collides with a paddle.
        """
        paddle_edges = paddle.get_edges()
        closest_x = max(min(position.x, paddle_edges.right), paddle_edges.left)
        closest_y = max(min(position.y, paddle_edges.bottom), paddle_edges.top)
        distance_x = position.x - closest_x
        distance_y = position.y - closest_y
        distance = math.sqrt(distance_x**2 + distance_y**2)
        return distance < self.radius

    def reset(self):
        self.position = Position(GAME_WIDTH / 2, GAME_HEIGHT / 2)
        self.__set_random_speed()

    def __get_side(self, distance_x: float, distance_y: float, position: Position, paddle_position: Position) -> str:
        if abs(distance_x) > abs(distance_y):
            if distance_x > paddle_position.x - position.x:
                return "right"
            return "left"
        if distance_y > paddle_position.y - position.y:
            return "bottom"
        return "top"

    def __get_collision_point(self, paddle: Paddle) -> Position:
        paddle_edges = paddle.get_edges()
        closest_x = max(min(self.position.x, paddle_edges.right), paddle_edges.left)
        closest_y = max(min(self.position.y, paddle_edges.bottom), paddle_edges.top)
        return Position(closest_x, closest_y)

    def __get_collision_side(self, position: Position, paddle: Paddle) -> str:
        """
        Determines which side of the paddle the ball collides with,
        accurately considering the ball's radius.
        """
        paddle_edges = paddle.get_edges()
        closest_x = max(min(position.x, paddle_edges.right), paddle_edges.left)
        closest_y = max(min(position.y, paddle_edges.bottom), paddle_edges.top)
        distance_x = position.x - closest_x
        distance_y = position.y - closest_y
        return self.__get_side(distance_x, distance_y, position, paddle.get_position())

    def __collide_with_paddle(self, paddle: Paddle):
        self.__push_ball(paddle)
        collision_point = self.__get_collision_point(paddle)
        self.speed = paddle.get_ball_speed_after_paddle_collision(collision_point)
        logger.info("New speed is: %s", self.speed.__dict__)

    def __push_ball(self, paddle: Paddle):
        paddle_edges = paddle.get_edges()
        side = self.__get_collision_side(self.position, paddle)
        push_position = Position(self.position.x, self.position.y)
        match side:
            case "top":
                push_position.y = paddle_edges.top - self.radius
            case "bottom":
                push_position.y = paddle_edges.bottom + self.radius
            case "left":
                push_position.x = paddle_edges.left - self.radius
            case "right":
                push_position.x = paddle_edges.right + self.radius
        self.set_position(push_position)
        logger.info("Ball collided with paddle %s on the %s side.", paddle.slot, side)

    def __update_wall_collision(self, new_position: Position) -> dict[str, str] | None:
        collide_x = (
            new_position.x <= self.radius or new_position.x >= GAME_WIDTH - self.radius
        )
        collide_y = (
            new_position.y <= self.radius or new_position.y >= GAME_HEIGHT - self.radius
        )
        if collide_x:
            player_slot = new_position.x <= self.radius
            self.reset()
            return self.hit_wall(player_slot)
        if collide_y:
            self.speed.reverse_y_direction()
        else:
            self.position = new_position
        return None

    def __set_random_speed(self):
        chosen_set = random_ball_speeds[self.player_turn]
        self.speed = random.choice(list(chosen_set))
        self.player_turn = (self.player_turn + 1) % 2

