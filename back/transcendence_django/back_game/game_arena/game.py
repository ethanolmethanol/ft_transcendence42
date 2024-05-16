import logging
from back_game.game_entities.ball import Ball
from back_game.game_arena.map import Map
from back_game.game_entities.paddle import Paddle
from back_game.game_settings.game_constants import (
    LISTENING,
    OVER,
    PROCESSING,
    STARTED,
    VALID_DIRECTIONS,
    WAITING,
)

logger = logging.getLogger(__name__)


class Game:
    def __init__(self, nb_players, ball_hit_wall):
        self.status = WAITING
        self.paddles = {
            f"{i + 1}": Paddle(i + 1, nb_players) for i in range(nb_players)
        }
        self.ball = Ball(self.paddles.values(), ball_hit_wall)
        self.map = Map()  # depends on the number of players

    def add_paddle(self, player_name, index):
         self.paddles[player_name] = self.paddles.pop(f"{index}")

    def start(self):
        self.set_status(STARTED)

    def conclude(self):
        self.set_status(OVER)

    def set_status(self, status):
        self.status = status

    def move_paddle(self, player_name, direction):
        if direction not in VALID_DIRECTIONS:
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
