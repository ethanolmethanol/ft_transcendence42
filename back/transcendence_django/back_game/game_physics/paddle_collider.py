import logging

from back_game.game_entities.ball import Ball
from back_game.game_entities.paddle import Paddle
from back_game.game_geometry.edges import Edges
from back_game.game_geometry.position import Position
from back_game.game_physics.speed import Speed
from back_game.game_settings.game_constants import (
    INITIAL_BALL_SPEED_COEFF,
    LEFT_SLOT,
    RIGHT_SLOT,
    TOP_SLOT,
    BOT_SLOT,
)

logger = logging.getLogger(__name__)


class PaddleCollider:

    @staticmethod
    def get_collision_point(ball: Ball, paddle: Paddle) -> Position:
        paddle_edges: Edges = paddle.get_edges()
        closest_x: float = max(
            min(ball.position.x, paddle_edges.right), paddle_edges.left
        )
        closest_y: float = max(
            min(ball.position.y, paddle_edges.bottom), paddle_edges.top
        )
        return Position(closest_x, closest_y)

    @staticmethod
    def get_ball_speed_after_paddle_collision(
        paddle: Paddle, collision_point: Position
    ) -> Speed:
        speed_component = PaddleCollider.__get_ball_speed_direction(
            paddle, collision_point
        )
        u_speed = speed_component.unit_vector()
        return Speed(
            INITIAL_BALL_SPEED_COEFF * u_speed.x, INITIAL_BALL_SPEED_COEFF * u_speed.y
        )

    @staticmethod
    def __get_ball_speed_direction(paddle: Paddle, collision_point: Position) -> Speed:
        if paddle.slot == LEFT_SLOT:
            speed_component_x = paddle.rectangle.distance_from_center
        elif paddle.slot == RIGHT_SLOT:
            speed_component_x = (-1) * paddle.rectangle.distance_from_center
        elif paddle.slot == BOT_SLOT: #TODO test when handling >2 players
            speed_component_y = paddle.rectangle.distance_from_center
        elif paddle.slot == TOP_SLOT: #TODO test when handling >2 players
            speed_component_y = (-1) * paddle.rectangle.distance_from_center
        else:
            raise Exception("Oopsie! Too many paddles?")
        if paddle.slot == LEFT_SLOT or paddle.slot == RIGHT_SLOT:
            speed_component_y = collision_point.y - paddle.rectangle.convexity_center.y
        else:
            speed_component_x = collision_point.x - paddle.rectangle.convexity_center.x
        return Speed(speed_component_x, speed_component_y)
