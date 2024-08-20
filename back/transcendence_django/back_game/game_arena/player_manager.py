import logging
import time
from typing import Any

from back_game.game_arena.player import (
    DISABLED,
    ENABLED,
    GIVEN_UP,
    OVER,
    Player,
    PlayerStatus,
)
from back_game.game_settings.game_constants import (
    AFK_WARNING_THRESHOLD,
    MAX_PLAYER,
    MIN_PLAYER,
)
from transcendence_django.dict_keys import (
    AI_OPPONENTS_LOCAL,
    AI_OPPONENTS_ONLINE,
    ARENA_FULL,
    HUMAN_OPPONENTS_LOCAL,
    HUMAN_OPPONENTS_ONLINE,
    INVALID_NB_PLAYERS,
    IS_BOT,
    IS_REMOTE,
    NB_PLAYERS,
    OPTIONS,
    PLAYER_NAME,
    PLAYERS,
    SCORE,
    TIME_LEFT,
    UNKNOWN_USER,
    USER_ID,
    WINNER,
)

logger = logging.getLogger(__name__)


class PlayerManager:
    def __init__(self, player_specs: dict[str, Any]):
        self.__fill_player_specs(player_specs)
        self.players: dict[str, Player] = {}
        self.last_kick_check: float = time.time()

    def is_empty(self) -> bool:
        return self.__count_players(PlayerStatus(ENABLED)) == 0

    def is_full(self) -> bool:
        enable_players_count = self.__count_players(PlayerStatus(ENABLED))
        disable_players_count = self.__count_players(PlayerStatus(DISABLED))
        logger.info(
            f"IS FULL? {enable_players_count} + {disable_players_count} vs"
            + f" {self.nb_players}"
        )
        return enable_players_count + disable_players_count == self.nb_players

    def add_player(self, user_id: int, player_name: str, is_bot: bool):
        player = Player(user_id, player_name, is_bot)
        self.players[player_name] = player

    def remove_player(self, player_name):
        del self.players[player_name]

    def allow_player_enter_arena(self, user_id: int):
        if not self.is_player_in_game(user_id) and self.is_full():
            raise ValueError(ARENA_FULL)

    def disable_player(self, user_id: int):
        self.__change_player_status(user_id, PlayerStatus(DISABLED))

    def enable_player(self, user_id: int):
        self.__change_player_status(user_id, PlayerStatus(ENABLED))

    def player_gave_up(self, user_id: int):
        self.__change_player_status(user_id, PlayerStatus(GIVEN_UP))

    def finish_active_players(self):
        for player in self.players.values():
            if player.is_active():
                self.__finish_player(player.user_id)

    def is_player_in_game(self, user_id: int) -> bool:
        return any(player.user_id == user_id for player in self.players.values())

    def has_enough_players(self) -> bool:
        enable_players_count = self.__count_players(PlayerStatus(ENABLED))
        disable_players_count = self.__count_players(PlayerStatus(DISABLED))
        return enable_players_count + disable_players_count == self.nb_players

    def rematch(self, user_id: int):
        if not self.is_player_in_game(user_id):
            raise KeyError(UNKNOWN_USER)
        self.enable_player(user_id)

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

    def get_game_summary(self) -> dict[str, Any]:
        winner = self.__get_winner()
        return {
            PLAYERS: [
                {
                    USER_ID: player.user_id,
                    SCORE: player.score,
                    IS_BOT: player.is_bot,
                }
                for player in self.players.values()
            ],
            WINNER: (
                {PLAYER_NAME: winner.player_name, USER_ID: winner.user_id}
                if winner
                else None
            ),
            IS_REMOTE: self.is_remote,
        }

    def finish_given_up_players(self):
        for player in self.players.values():
            if player.status == PlayerStatus(GIVEN_UP):
                player.status = PlayerStatus(OVER)

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

    def get_scores(self) -> list[int]:
        if len(self.players) < self.nb_players:
            scores = [0 for _ in range(self.nb_players)]
        else:
            scores = [player.score for player in self.players.values()]
        return scores

    def get_player_name(self, user_id: int) -> str:
        return self.__get_player_from_user_id(user_id).player_name

    def __get_winner(self) -> Player | None:
        active_players = [
            player for player in self.players.values() if player.is_active()
        ]
        if not active_players:
            return None
        winner = max(active_players, key=lambda player: player.score)
        return winner

    def __count_players(self, state: PlayerStatus = PlayerStatus(ENABLED)) -> int:
        return sum(player.status == state for player in self.players.values())

    def __change_player_status(self, user_id: int, status: PlayerStatus):
        if self.is_remote:
            player = self.__get_player_from_user_id(user_id)
            player.status = status
            logger.info("Player %s status changed to %s", player.player_name, status)
        else:
            for player in self.players.values():
                player.status = status

    def __finish_player(self, user_id: int):
        self.__change_player_status(user_id, PlayerStatus(OVER))

    def __fill_player_specs(self, players_specs: dict[str, Any]):
        self.nb_players = players_specs[NB_PLAYERS]
        self.nb_humans = (
            players_specs[OPTIONS][HUMAN_OPPONENTS_LOCAL]
            or players_specs[OPTIONS][HUMAN_OPPONENTS_ONLINE]
        )
        self.nb_robots = (
            players_specs[OPTIONS][AI_OPPONENTS_LOCAL]
            or players_specs[OPTIONS][AI_OPPONENTS_ONLINE]
        )
        if self.nb_players not in range(MIN_PLAYER, MAX_PLAYER + 1):
            raise ValueError(INVALID_NB_PLAYERS)
        self.is_remote = players_specs[IS_REMOTE] == "online"

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
