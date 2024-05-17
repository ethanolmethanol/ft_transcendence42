import logging

from back_game.game_arena.game import Game
from back_game.game_arena.player import ENABLED
from back_game.game_arena.player_manager import PlayerManager
from back_game.game_settings.game_constants import (
    MAXIMUM_SCORE,
    WAITING,
)

logger = logging.getLogger(__name__)


class Arena:

    def __init__(self, players_specs: dict):
        self.id: str = str(id(self))
        self.player_manager: PlayerManager = PlayerManager(players_specs)
        self.game: Game = Game(self.player_manager.nb_players, self.ball_hit_wall)

    def __dict__(self) -> dict:
        return {
            "id": self.id,
            "status": self.game.status,
            "players": [player.player_name for player in self.player_manager.players.values()],
            "scores": self.player_manager.get_scores(),
            "ball": self.game.ball.to_dict(),
            "paddles": [paddle.to_dict() for paddle in self.game.paddles.values()],
            "map": self.game.map.to_dict(),
        }

    def is_empty(self) -> bool:
        return self.player_manager.is_empty()

    def is_full(self) -> bool:
        return self.player_manager.is_full()

    def get_winner(self) -> str:
        return self.player_manager.get_winner()

    def get_players(self) -> dict:
        return self.player_manager.players

    def get_status(self):
        return self.game.status

    def enter_arena(self, user_id: int):
        self.player_manager.allow_player_enter_arena(user_id)
        if self.player_manager.is_remote:
            self.__enter_remote_mode(user_id)
        else:
            self.__enter_local_mode(user_id)

    def start_game(self):
        self.__reset()
        self.game.start()
        logger.info("Game started. %s", self.id)

    def conclude_game(self):
        self.player_manager.disable_all_players()
        self.game.conclude()
        logger.info("Game is over. %s", self.id)

    def rematch(self, user_id: int) -> dict | None:
        self.player_manager.rematch(user_id)
        self.game.set_status(WAITING)
        if self.player_manager.are_all_players_ready():
            self.start_game()
            return self.__dict__()
        return None

    def disable_player(self, user_id: int):
        self.player_manager.disable_player(user_id)

    def player_gave_up(self, user_id: int):
        self.player_manager.player_gave_up(user_id)

    def ball_hit_wall(self, player_slot: int) -> dict:
        if not self.player_manager.is_remote:
            player_name = "Player2" if player_slot else "Player1"
            logger.info("Point was scored for %s. slot: %s", player_name, player_slot)
            player = self.player_manager.players[player_name]
            player.score += 1
            logger.info(
                "Point was scored for %s. Their score is %s", player_name, player.score
            )
            if player.score == MAXIMUM_SCORE:
                self.conclude_game()
            return {"score": {"player_name": player_name}}
        raise NotImplementedError()  # TO DO

    def move_paddle(self, player_name: str, direction: int) -> dict:
        paddle_dict: dict = self.game.move_paddle(player_name, direction)
        self.player_manager.update_activity_time(player_name)
        return paddle_dict

    def update_game(self) -> dict:
        update_dict: dict = self.game.update()
        logger.info("Updated_dict: %s", update_dict)
        kicked_players = self.player_manager.kick_afk_players()
        if kicked_players:
            update_dict["kicked_players"] = kicked_players
        return update_dict

    def set_status(self, status):
        self.game.set_status(status)

    def __reset(self):
        self.player_manager.reset()
        self.game.reset()

    def __enter_local_mode(self, user_id: int):
        if self.is_empty():
            self.__register_player(user_id, "Player1")
            self.__register_player(user_id, "Player2")

    def __enter_remote_mode(self, user_id: int):
        if self.player_manager.is_player_in_game(user_id):
            self.__register_player(user_id, user_id)
        else:
            self.player_manager.change_player_status(ENABLED)

    def __register_player(self, user_id: int, player_name: str):
        self.player_manager.add_player(user_id, player_name)
        self.game.add_paddle(player_name, len(self.player_manager.players))
        if self.is_full():
            self.start_game()
