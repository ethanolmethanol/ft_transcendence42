import logging
import math

from back_game.game_entities.ball import Ball
from back_game.game_entities.paddle import Paddle
from back_game.game_physics.position import Position
# from back_game.game_physics.speed import Speed
# from back_game.game_settings.game_constants import (
#     INITIAL_BALL_SPEED_COEFF,
#     LEFT_SLOT,
#     RIGHT_SLOT,
# )
from back_game.game_physics.ball_collision_handler import BallCollisionHandler
from back_game.game_physics.paddle_collision_handler import PaddleCollisionHandler

logger = logging.getLogger(__name__)

class Collision:

    @staticmethod
    def is_paddle_collision(ball: Ball, paddle: Paddle) -> bool:
        """
        Checks if the ball collides with a paddle.
        """
        paddle_edges = paddle.get_edges()
        closest_x = max(min(ball.position.x, paddle_edges.right), paddle_edges.left)
        closest_y = max(min(ball.position.y, paddle_edges.bottom), paddle_edges.top)
        distance_x = ball.position.x - closest_x
        distance_y = ball.position.y - closest_y
        distance = math.sqrt(distance_x**2 + distance_y**2)
        return distance < ball.radius

    # @staticmethod
    # def ball_collide_with_wall(new_position: Position, ball: Ball) -> dict[str, str] | None:
    #     collide_x = (
    #         new_position.x <= ball.radius or new_position.x >= GAME_WIDTH - ball.radius
    #     )
    #     collide_y = (
    #         new_position.y <= ball.radius or new_position.y >= GAME_HEIGHT - ball.radius
    #     )
    #     if collide_x:
    #         player_slot = new_position.x <= ball.radius
    #         ball.reset()
    #         return ball.hit_wall(player_slot)
    #     if collide_y:
    #         ball.speed.reverse_y_direction()
    #     else:
    #         ball.position = new_position
    #     return None

    # @staticmethod
    # def get_side(distance_x: float, distance_y: float, position: Position, paddle_position: Position) -> str:
    #     if abs(distance_x) > abs(distance_y):
    #         if distance_x > paddle_position.x - position.x:
    #             return "right"
    #         return "left"
    #     if distance_y > paddle_position.y - position.y:
    #         return "bottom"
    #     return "top"

    # @staticmethod
    # def get_collision_side(position: Position, paddle: Paddle) -> str:
    #     """
    #     Determines which side of the paddle the ball collides with,
    #     accurately considering the ball's radius.
    #     """
    #     paddle_edges = paddle.get_edges()
    #     closest_x = max(min(position.x, paddle_edges.right), paddle_edges.left)
    #     closest_y = max(min(position.y, paddle_edges.bottom), paddle_edges.top)
    #     distance_x = position.x - closest_x
    #     distance_y = position.y - closest_y
    #     return Collision.get_side(distance_x, distance_y, position, paddle.get_position())

    # @staticmethod
    # def push_ball(ball: Ball, paddle: Paddle):
    #     paddle_edges = paddle.get_edges()
    #     side = Collision.get_collision_side(ball.position, paddle)
    #     push_position = Position(ball.position.x, ball.position.y)
    #     match side:
    #         case "top":
    #             push_position.y = paddle_edges.top - ball.radius
    #         case "bottom":
    #             push_position.y = paddle_edges.bottom + ball.radius
    #         case "left":
    #             push_position.x = paddle_edges.left - ball.radius
    #         case "right":
    #             push_position.x = paddle_edges.right + ball.radius
    #     ball.set_position(push_position)
    #     logger.info("Ball collided with paddle %s on the %s side.", paddle.slot, side)

    # @staticmethod
    # def get_collision_point(ball: Ball, paddle: Paddle) -> Position:
    #     paddle_edges = paddle.get_edges()
    #     closest_x = max(min(ball.position.x, paddle_edges.right), paddle_edges.left)
    #     closest_y = max(min(ball.position.y, paddle_edges.bottom), paddle_edges.top)
    #     return Position(closest_x, closest_y)

    # @staticmethod
    # def get_ball_speed_after_paddle_collision(paddle: Paddle, collision_point: Position) -> Speed:
    #     speed_component = Collision.get_ball_speed_direction(paddle, collision_point)
    #     u_speed = speed_component.unit_vector()
    #     return Speed(
    #         INITIAL_BALL_SPEED_COEFF * u_speed.x, INITIAL_BALL_SPEED_COEFF * u_speed.y
    #     )

    # @staticmethod
    # def get_ball_speed_direction(paddle: Paddle, collision_point: Position) -> Speed:
    #     if paddle.slot == LEFT_SLOT:
    #         speed_component_x = paddle.rectangle.distance_from_center
    #     elif paddle.slot == RIGHT_SLOT:
    #         speed_component_x = (-1) * paddle.rectangle.distance_from_center
    #     speed_component_y = collision_point.y - paddle.rectangle.convexity_center.y
    #     return Speed(speed_component_x, speed_component_y)

    @staticmethod
    def collide_with_paddle(ball: Ball, paddle: Paddle):
        BallCollisionHandler.push_ball(ball, paddle)
        collision_point = PaddleCollisionHandler.get_collision_point(ball, paddle)
        ball.speed = PaddleCollisionHandler.get_ball_speed_after_paddle_collision(paddle, collision_point)
        logger.info("New speed is: %s", ball.speed.__dict__)

    @staticmethod
    def handle_collision(new_position: Position, ball: Ball):
        for paddle in ball.paddles:
            if Collision.is_paddle_collision(ball, paddle):
                Collision.collide_with_paddle(ball, paddle)
                return None
        score_update = BallCollisionHandler.ball_collide_with_wall(new_position, ball)
        return score_update

    @staticmethod
    def detect_collision(new_position: Position, ball: Ball) -> dict:
        update = Collision.handle_collision(new_position, ball)
        ball_position_update = {"ball": {"position": ball.position.__dict__}}
        return (
            {**update, **ball_position_update}
            if update is not None
            else ball_position_update
        )
