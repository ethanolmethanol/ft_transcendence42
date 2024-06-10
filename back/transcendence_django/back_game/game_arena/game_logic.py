import logging

from back_game.game_entities.ball import Ball
from back_game.game_entities.paddle import Paddle
from back_game.game_geometry.position import Position
from back_game.game_physics.collision import Collision
from back_game.game_settings.dict_keys import BALL, POSITION

logger = logging.getLogger(__name__)


class GameLogic:

    @staticmethod
    def handle_collision(ball: Ball, paddle: Paddle):
        if Collision.is_paddle_collision(ball, paddle):
            Collision.collide_with_paddle(ball, paddle)
            return True
        return False

    @staticmethod
    def detect_collision(ball: Ball, new_position: Position) -> dict[str, any]:
        update = Collision.handle_collision(new_position, ball)
        ball_position_update = {BALL: {POSITION: ball.position.__dict__}}
        return (
            {**update, **ball_position_update}
            if update is not None
            else ball_position_update
        )

    @staticmethod
    def update_ball_position(new_position: Position):
        ball_position_update = {BALL: {POSITION: new_position.__dict__}}
        return ball_position_update
