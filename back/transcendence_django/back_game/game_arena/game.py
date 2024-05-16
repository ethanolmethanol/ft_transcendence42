import logging
from back_game.game_entities.ball import Ball
from back_game.game_arena.map import Map
from back_game.game_entities.paddle import Paddle
from back_game.game_settings.game_constants import (
    LISTENING,
    OVER,
    PROCESSING,
    STARTED,
    WAITING,
)

logger = logging.getLogger(__name__)


class Game:
    def __init__(self):
        self.status = WAITING
        self.paddles = {}
        self.ball = None
        self.map = None

    def add_paddle(self, player_name):
         self.paddles[player_name] = self.paddles.pop(f"{len(self.players)}")

    def start(self):
        self.set_status(STARTED)
        logger.info("Game started. %s", self.id)

    def conclude(self):
        self.set_status(OVER)
        for player in self.players.values():
            self.disable_player(player.user_id)

    def set_status(self, status):
        self.status = status

    def move_paddle(self, player_name, direction):
        if direction not in [-1, 1]:
            raise ValueError("Direction is invalid. It should be -1 or 1.")
        paddle = self.paddles[player_name]
        if paddle.status == LISTENING:
            paddle.status = PROCESSING
            paddle.move(direction)
            try:
                self.ball.update_collision(paddle)
            except ValueError:
                logger.error("Paddle cannot move due to collision.")
                paddle.move(-direction)
            paddle.status = LISTENING
        return paddle.get_dict_update()

    def update(self):
        ball_update = self.ball.move()
        game_status = {"status": self.status}
        return {**ball_update, **game_status}
    
    def reset(self):
        for paddle in self.paddles.values():
            paddle.reset()
        self.ball.reset()