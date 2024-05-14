import logging
import math
import random

from back_game.game_physics.position import Position
from back_game.game_physics.vector import Vector
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
        Vector(-INITIAL_SPEED_X, 0),
        Vector(-INITIAL_SPEED_X, -INITIAL_SPEED_Y / 2),
        Vector(-INITIAL_SPEED_X, INITIAL_SPEED_Y / 2),
        Vector(-INITIAL_SPEED_X, INITIAL_SPEED_Y / 3),
        Vector(-INITIAL_SPEED_X, -INITIAL_SPEED_Y / 3),
    },
    {
        Vector(INITIAL_SPEED_X, 0),
        Vector(INITIAL_SPEED_X, -INITIAL_SPEED_Y / 2),
        Vector(INITIAL_SPEED_X, INITIAL_SPEED_Y / 2),
        Vector(INITIAL_SPEED_X, -INITIAL_SPEED_Y / 3),
    },
]


class Ball:

    def __init__(self, paddles, hit_wall_func):
        self.position = Position(GAME_WIDTH / 2, GAME_HEIGHT / 2)
        self.radius = BALL_RADIUS
        self.paddles = paddles
        self.hit_wall = hit_wall_func
        self.player_turn = 0
        self.speed = None
        self.__set_random_speed()

    def update(self, new_position, new_speed, new_radius):
        self.position.set_coordinates(new_position.x, new_position.y)
        self.speed.set_coordinates(new_speed.x, new_speed.y)
        self.radius = new_radius

    def to_dict(self):
        return {
            "position": self.position.to_dict(),
            "speed": self.speed.to_dict(),
            "radius": self.radius,
        }

    def set_position(self, position):
        x = position.x
        y = position.y
        if x < self.radius or x > GAME_WIDTH - self.radius:
            raise ValueError("Ball x-coordinate is out of bounds.")
        if y < self.radius or y > GAME_HEIGHT - self.radius:
            raise ValueError("Ball y-coordinate is out of bounds.")
        self.position.set_coordinates(x, y)

    def move(self):
        new_position = Position(
            self.position.x + self.speed.x, self.position.y + self.speed.y
        )
        update = self.update_position(new_position)
        ball_position_update = {"ball": {"position": self.position.to_dict()}}
        return (
            {**update, **ball_position_update}
            if update is not None
            else ball_position_update
        )

    def update_collision(self, paddle):
        if self.is_paddle_collision(self.position, paddle):
            self.update_position(self.position)

    def update_position(self, new_position):
        for paddle in self.paddles:
            if self.is_paddle_collision(self.position, paddle):
                self.__push_ball(paddle)
                collision_point = self.get_collision_point(paddle)
                self.speed = paddle.get_speed_after_collision(collision_point)
                logger.info("New speed is: (%s, %s)", self.speed.x, self.speed.y)
                return None
        score = self.__update_wall_collision(new_position)
        return score

    def get_collision_point(self, paddle):
        closest_x = max(min(self.position.x, paddle.right), paddle.left)
        closest_y = max(min(self.position.y, paddle.bottom), paddle.top)
        return Position(closest_x, closest_y)

    def __push_ball(self, paddle):
        side = self.get_collision_side(self.position, paddle)
        push_position = Position(self.position.x, self.position.y)
        if side == "top":
            push_position.y = paddle.top - self.radius
        elif side == "bottom":
            push_position.y = paddle.bottom + self.radius
        elif side == "left":
            push_position.x = paddle.left - self.radius
        elif side == "right":
            push_position.x = paddle.right + self.radius
        self.set_position(push_position)
        logger.info("Ball collided with paddle %s on the %s side.", paddle.slot, side)

    def is_paddle_collision(self, position, paddle):
        """
        Checks if the ball collides with a paddle.
        """
        closest_x = max(min(position.x, paddle.right), paddle.left)
        closest_y = max(min(position.y, paddle.bottom), paddle.top)
        distance_x = position.x - closest_x
        distance_y = position.y - closest_y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        return distance < self.radius

    def get_collision_side(self, position, paddle):
        """
        Determines which side of the paddle the ball collides with,
        accurately considering the ball's radius.
        """
        closest_x = max(min(position.x, paddle.right), paddle.left)
        closest_y = max(min(position.y, paddle.bottom), paddle.top)
        distance_x = position.x - closest_x
        distance_y = position.y - closest_y

        return self.__get_side(distance_x, distance_y, position, paddle)

    def __get_side(self, distance_x, distance_y, position, paddle):
        if abs(distance_x) > abs(distance_y):
            if distance_x > paddle.position.x - position.x:
                return "right"
            return "left"
        if distance_y > paddle.position.y - position.y:
            return "bottom"
        return "top"

    def __update_wall_collision(self, new_position):
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
            self.speed.y *= -1
        else:
            self.position = new_position
        return None

    def reset(self):
        self.position = Position(GAME_WIDTH / 2, GAME_HEIGHT / 2)
        self.__set_random_speed()

    def __set_random_speed(self):
        chosen_set = random_ball_speeds[self.player_turn]
        self.speed = random.choice(list(chosen_set))
        self.player_turn = (self.player_turn + 1) % 2
