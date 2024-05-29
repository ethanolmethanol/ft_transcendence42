import logging

from back_game.game_entities.ball import Ball
from back_game.game_entities.paddle import Paddle
from back_game.game_physics.position import Position
from back_game.game_physics.speed import Speed
from back_game.game_settings.game_constants import (
    INITIAL_BALL_SPEED_COEFF,
    LEFT_SLOT,
    RIGHT_SLOT,
)

logger = logging.getLogger(__name__)


class PaddleCollider:

    @staticmethod
    def get_collision_point(ball: Ball, paddle: Paddle) -> Position:
        paddle_edges = paddle.get_edges()
        closest_x = max(min(ball.position.x, paddle_edges.right), paddle_edges.left)
        closest_y = max(min(ball.position.y, paddle_edges.bottom), paddle_edges.top)
        return Position(closest_x, closest_y)

    @staticmethod
    def get_ball_speed_after_paddle_collision(
        paddle: Paddle, collision_point: Position
    ) -> Speed:
        speed_component = PaddleCollider.get_ball_speed_direction(
            paddle, collision_point
        )
        u_speed = speed_component.unit_vector()
        return Speed(
            INITIAL_BALL_SPEED_COEFF * u_speed.x, INITIAL_BALL_SPEED_COEFF * u_speed.y
        )

    @staticmethod
    def get_ball_speed_direction(paddle: Paddle, collision_point: Position) -> Speed:
        if paddle.slot == LEFT_SLOT:
            speed_component_x = paddle.rectangle.distance_from_center
        elif paddle.slot == RIGHT_SLOT:
            speed_component_x = (-1) * paddle.rectangle.distance_from_center
        speed_component_y = collision_point.y - paddle.rectangle.convexity_center.y
        return Speed(speed_component_x, speed_component_y)
