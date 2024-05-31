import logging
from typing import Any, NewType

from back_game.game_arena.map import Map
from back_game.game_entities.ball import Ball
from back_game.game_entities.paddle import Paddle, PaddleStatus
from back_game.game_settings.dict_keys import STATUS
from back_game.game_settings.game_constants import (
    LISTENING,
    OVER,
    PROCESSING,
    STARTED,
    VALID_DIRECTIONS,
    WAITING,
)

logger = logging.getLogger(__name__)


GameStatus = NewType("GameStatus", int)


class Game:
    def __init__(self, nb_players: int):
        self.status: GameStatus = GameStatus(WAITING)
        self.paddles: dict[str, Paddle] = {
            f"{i + 1}": Paddle(i + 1, nb_players) for i in range(nb_players)
        }
        self.ball: Ball = Ball(self.paddles)
        self.map: Map = Map()  # depends on the number of players

    def add_paddle(self, player_name: str, index: int):
        self.paddles[player_name] = self.paddles.pop(f"{index}")

    def start(self):
        self.set_status(GameStatus(STARTED))

    def conclude(self):
        self.set_status(GameStatus(OVER))

    def set_status(self, status):
        self.status = status

    def move_paddle(self, player_name: str, direction: int) -> dict[str, Any]:
        if direction not in VALID_DIRECTIONS:
            raise ValueError("Direction is invalid. It should be -1 or 1.")
        paddle = self.paddles[player_name]
        if paddle.status == PaddleStatus(LISTENING):
            paddle.status = PaddleStatus(PROCESSING)
            paddle.move(direction)
            try:
                self.ball.update_collision(paddle)
            except ValueError:
                logger.error("Paddle cannot move due to collision.")
                paddle.move(-direction)
            paddle.status = PaddleStatus(LISTENING)
        return paddle.get_dict_update()

    def update(self) -> dict[str, Any]:
        ball_update: dict[str, Any] = self.ball.move()
        game_status: dict[str, Any] = {STATUS: self.status}
        return {**ball_update, **game_status}

    def reset(self):
        for paddle in self.paddles.values():
            paddle.reset()
        self.ball.reset()
