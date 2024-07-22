import logging
from typing import Any, NewType

from back_game.game_arena.map import Map
from back_game.game_entities.ball import Ball
from back_game.game_entities.paddle import Paddle, PaddleStatus
from back_game.game_physics.collision import Collision
from transcendence_django.dict_keys import STATUS
from back_game.game_settings.game_constants import (
    CREATED,
    LISTENING,
    OVER,
    PROCESSING,
    STARTED,
    VALID_DIRECTIONS,
)

logger = logging.getLogger(__name__)


GameStatus = NewType("GameStatus", int)


class Game:
    def __init__(self, players_specs: dict[str, Any]):
        try:
            nb_players = players_specs["nb_players"]
            options: dict[str, Any] = players_specs["options"]
            paddle_size = options["paddle_size"]
            ball_speed = options["ball_speed"]
            self.is_private: bool = options["is_private"]
        except KeyError as exc:
            raise ValueError("Options are missing.") from exc
        self.status: GameStatus = GameStatus(CREATED)
        self.paddles: dict[str, Paddle] = {
            f"{i + 1}": Paddle(i + 1, nb_players, paddle_size)
            for i in range(nb_players)
        }
        self.ball: Ball = Ball(self.paddles, ball_speed)
        self.map: Map = Map()  # depends on the number of players

    def add_paddle(self, player_name: str):
        for key, paddle in list(self.paddles.items()):
            if paddle.player_name is None:
                paddle.set_player_name(player_name)
                del self.paddles[key]
                self.paddles[player_name] = paddle
                break

    def remove_paddle(self, player_name: str):
        paddle = self.paddles[player_name]
        paddle.unset_player_name()

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
                Collision.update_ball_collision(self.ball, paddle)
            except ValueError:
                logger.error("Paddle cannot move due to collision.")
                paddle.move(-direction)
            paddle.status = PaddleStatus(LISTENING)
        return paddle.get_dict_update()

    def update(self) -> dict[str, Any]:
        ball_update: dict[str, Any] = Collision.resolve_collision(self.ball)
        game_status: dict[str, Any] = {STATUS: self.status}
        return {**ball_update, **game_status}

    def reset(self):
        for paddle in self.paddles.values():
            paddle.reset()
        self.ball.reset()
