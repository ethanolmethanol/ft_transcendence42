import logging

from back_game.game_entities.ball import Ball
from back_game.game_entities.paddle import Paddle
from back_game.game_geometry.edges import Edges
from back_game.game_geometry.position import Position
from back_game.game_settings.dict_keys import BOTTOM, LEFT, RIGHT, TOP
from back_game.game_settings.game_constants import GAME_HEIGHT, GAME_WIDTH

logger = logging.getLogger(__name__)


class BallCollider:

    @staticmethod
    def ball_collide_with_wall(new_position: Position, ball: Ball) -> int | None:
        collide_x = (
            new_position.x <= ball.radius or new_position.x >= GAME_WIDTH - ball.radius
        )
        collide_y = (
            new_position.y <= ball.radius or new_position.y >= GAME_HEIGHT - ball.radius
        )
        if collide_x:
            player_slot: int = int(new_position.x <= ball.radius)
            ball.reset()
            return player_slot
        if collide_y:
            ball.speed.reverse_y_direction()
        else:
            ball.position = new_position
        return None

    @staticmethod
    def push_ball(ball: Ball, paddle: Paddle):
        paddle_edges = paddle.get_edges()
        side = BallCollider.__get_collision_side(ball.position, paddle)
        push_position = Position(ball.position.x, ball.position.y)
        match side:
            case "top":
                push_position.y = paddle_edges.top - ball.radius
            case "bottom":
                push_position.y = paddle_edges.bottom + ball.radius
            case "left":
                push_position.x = paddle_edges.left - ball.radius
            case "right":
                push_position.x = paddle_edges.right + ball.radius
        ball.set_position(push_position)
        logger.info("Ball collided with paddle %s on the %s side.", paddle.slot, side)

    @staticmethod
    def __get_side(
        distance_x: float,
        distance_y: float,
        position: Position,
        paddle_position: Position,
    ) -> str:
        if abs(distance_x) > abs(distance_y):
            if distance_x > paddle_position.x - position.x:
                return RIGHT
            return LEFT
        if distance_y > paddle_position.y - position.y:
            return BOTTOM
        return TOP

    @staticmethod
    def __get_collision_side(position: Position, paddle: Paddle) -> str:
        """
        Determines which side of the paddle the ball collides with,
        accurately considering the ball's radius.
        """
        paddle_edges: Edges = paddle.get_edges()
        closest_x: float = max(min(position.x, paddle_edges.right), paddle_edges.left)
        closest_y: float = max(min(position.y, paddle_edges.bottom), paddle_edges.top)
        distance_x: float = position.x - closest_x
        distance_y: float = position.y - closest_y
        return BallCollider.__get_side(
            distance_x, distance_y, position, paddle.get_position()
        )
