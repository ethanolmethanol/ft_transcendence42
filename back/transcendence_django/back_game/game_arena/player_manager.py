import logging
import time

from back_game.game_arena.player import DISABLED, ENABLED, Player
from back_game.game_settings.game_constants import (
    AFK_WARNING_THRESHOLD,
    GIVEN_UP,
    MAX_PLAYER,
    MIN_PLAYER,
)

logger = logging.getLogger(__name__)


class PlayerManager:
    def __init__(self, player_specs):
        self.__fill_player_specs(player_specs)
        self.players = {}
        self.last_kick_check = time.time()

    def is_empty(self):
        return all(player.status == GIVEN_UP for player in self.players.values())

    def is_full(self):
        return len(self.players) == self.nb_players

    def add_player(self, user_id, player_name):
        player = Player(user_id, player_name)
        self.players[player_name] = player

    def allow_player_enter_arena(self, user_id):
        if self.did_player_give_up(user_id):
            raise ValueError("The player has given up.")
        if not self.is_player_in_game(user_id) and self.is_full():
            raise ValueError("The arena is full.")

    def disable_player(self, user_id):
        self.change_player_status(user_id, DISABLED)

    def enable_player(self, user_id):
        self.change_player_status(user_id, ENABLED)

    def player_gave_up(self, user_id):
        self.change_player_status(user_id, GIVEN_UP)

    def disable_all_players(self):
        for player in self.players.values():
            self.disable_player(player.user_id)

    def is_player_in_game(self, user_id):
        if self.is_remote:
            return user_id in self.players and self.players[user_id].status != GIVEN_UP
        return self.players and any(
            player.user_id == user_id for player in self.players.values()
        )

    def rematch(self, user_id):
        if not self.is_player_in_game(user_id):
            raise KeyError("This user is unknown")
        self.enable_player(user_id)

    def are_all_players_ready(self):
        return self.is_full and all(
            player.status == ENABLED for player in self.players.values()
        )

    def did_player_give_up(self, user_id):
        try:
            if not self.is_remote:
                return self.players and all(
                    player.status == GIVEN_UP for player in self.players.values()
                )
            return self.players[user_id].status == GIVEN_UP
        except KeyError:
            return False

    def get_winner(self):
        winner = max(self.players.values(), key=lambda player: player.score)
        return winner.player_name

    def update_activity_time(self, player_name):
        self.players[player_name].update_activity_time()

    def kick_afk_players(self):
        kicked_players = []
        if time.time() - self.last_kick_check >= 1:
            kicked_players = self.__get_afk_players()
            self.last_kick_check = time.time()
        return kicked_players

    def reset(self):
        for player in self.players.values():
            player.reset()

    def change_player_status(self, user_id, status):
        if not self.did_player_give_up(user_id):
            if self.is_remote:
                self.players[user_id].status = status
            else:
                for player in self.players.values():
                    player.status = status

    def get_scores(self):
        if not self.players:
            scores = [0 for _ in range(self.nb_players)]
        else:
            scores = [player.score for player in self.players.values()]
        return scores

    def __fill_player_specs(self, players_specs):
        self.nb_players = players_specs["nb_players"]
        if self.nb_players not in range(MIN_PLAYER, MAX_PLAYER):
            raise ValueError("The number of players is out of allowed range.")
        self.is_remote = players_specs["mode"]

    def __get_afk_players(self):
        kicked_players = []
        for player in self.players.values():
            time_left_before_kick = player.get_time_left_before_kick()
            if time_left_before_kick <= AFK_WARNING_THRESHOLD:
                kicked_players.append(
                    {"player_name": player.player_name, "time_left": round(time_left_before_kick)}
                )
            if time_left_before_kick <= 0:
                self.player_gave_up(player.user_id)
                logger.info("Player %s was kicked due to inactivity.", player.player_name)
        return kicked_players
