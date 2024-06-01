import logging
import time
from typing import Any

from back_game.game_arena.player import (
    DISABLED,
    ENABLED,
    GIVEN_UP,
    Player,
    PlayerStatus,
)
from back_game.game_settings.dict_keys import (
    ARENA_FULL,
    INVALID_NB_PLAYERS,
    MODE,
    NB_PLAYERS,
    PLAYER_GAVE_UP,
    PLAYER_NAME,
    TIME_LEFT,
    UNKNOWN_USER,
)
from back_game.game_settings.game_constants import (
    AFK_WARNING_THRESHOLD,
    MAX_PLAYER,
    MIN_PLAYER,
)

logger = logging.getLogger(__name__)


class PlayerManager:
    def __init__(self, player_specs: dict[str, int]):
        self.__fill_player_specs(player_specs)
        self.players: dict[str, Player] = {}
        self.last_kick_check: float = time.time()

    def is_empty(self) -> bool:
        return all(
            player.status == PlayerStatus(GIVEN_UP) for player in self.players.values()
        )

    def is_full(self) -> bool:
        return len(self.players) == self.nb_players

    def add_player(self, user_id: int, player_name: str):
        player = Player(user_id, player_name)
        self.players[player_name] = player

    def allow_player_enter_arena(self, user_id: int):
        if self.did_player_give_up(user_id):
            raise ValueError(PLAYER_GAVE_UP)
        if not self.is_player_in_game(user_id) and self.is_full():
            raise ValueError(ARENA_FULL)

    def disable_player(self, user_id: int):
        self.change_player_status(user_id, PlayerStatus(DISABLED))

    def enable_player(self, user_id: int):
        self.change_player_status(user_id, PlayerStatus(ENABLED))

    def player_gave_up(self, user_id: int):
        self.change_player_status(user_id, PlayerStatus(GIVEN_UP))

    def disable_all_players(self):
        for player in self.players.values():
            self.disable_player(player.user_id)

    def is_player_in_game(self, user_id: int) -> bool:
        if self.is_remote:
            return any(
                player.user_id == user_id and player.status != PlayerStatus(GIVEN_UP)
                for player in self.players.values()
            )
        return any(player.user_id == user_id for player in self.players.values())

    def has_enough_players(self) -> bool:
        count_active_players = 0
        for player in self.players.values():
            count_active_players += player.status == PlayerStatus(ENABLED)
        return count_active_players >= 2

    def rematch(self, user_id: int):
        if not self.is_player_in_game(user_id):
            raise KeyError(UNKNOWN_USER)
        self.enable_player(user_id)

    def are_all_players_ready(self) -> bool:
        return self.is_full() and all(
            player.status == (ENABLED) for player in self.players.values()
        )

    def did_player_give_up(self, user_id: int) -> bool:
        try:
            if not self.is_remote:
                return len(self.players) > 0 and all(
                    player.status == PlayerStatus(GIVEN_UP)
                    for player in self.players.values()
                )
            player = self.__get_player_from_user_id(user_id)
            return player.status == PlayerStatus(GIVEN_UP)
        except KeyError:
            return False

    def get_winner(self) -> str:
        winner = max(self.players.values(), key=lambda player: player.score)
        return winner.player_name

    def update_activity_time(self, player_name: str):
        self.players[player_name].update_activity_time()

    def kick_afk_players(self) -> list[dict[str, Any]]:
        kicked_players: list[dict[str, Any]] = []
        if time.time() - self.last_kick_check >= 1:
            kicked_players = self.__get_afk_players()
            self.last_kick_check = time.time()
        return kicked_players

    def reset(self):
        for player in self.players.values():
            player.reset()

    def change_player_status(self, user_id: int, status: PlayerStatus):
        if not self.did_player_give_up(user_id):
            if self.is_remote:
                player = self.__get_player_from_user_id(user_id)
                player.status = status
            else:
                for player in self.players.values():
                    player.status = status

    def get_scores(self) -> list[int]:
        if len(self.players) < self.nb_players:
            scores = [0 for _ in range(self.nb_players)]
        else:
            scores = [player.score for player in self.players.values()]
        return scores

    def __fill_player_specs(self, players_specs: dict[str, int]):
        self.nb_players = players_specs[NB_PLAYERS]
        if self.nb_players not in range(MIN_PLAYER, MAX_PLAYER):
            raise ValueError(INVALID_NB_PLAYERS)
        self.is_remote = players_specs[MODE]

    def __get_afk_players(self) -> list[dict[str, Any]]:
        kicked_players: list[dict[str, Any]] = []
        for player in self.players.values():
            time_left_before_kick = player.get_time_left_before_kick()
            if time_left_before_kick <= AFK_WARNING_THRESHOLD:
                kicked_players.append(
                    {
                        PLAYER_NAME: player.player_name,
                        TIME_LEFT: round(time_left_before_kick),
                    }
                )
            if time_left_before_kick <= 0:
                self.player_gave_up(player.user_id)
                logger.info(
                    "Player %s was kicked due to inactivity.", player.player_name
                )
        return kicked_players

    def __get_player_from_user_id(self, user_id: int) -> Player:
        for player in self.players.values():
            if player.user_id == user_id:
                return player
        raise KeyError(UNKNOWN_USER)
