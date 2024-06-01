import time
from typing import NewType

from back_game.game_settings.game_constants import AFK_TIMEOUT

ENABLED = 0
DISABLED = 1
GIVEN_UP = 2
WAITING = 3

PlayerStatus = NewType("PlayerStatus", int)


class Player:
    def __init__(self, user_id: int, player_name: str):
        self.user_id: int = user_id
        self.player_name: str = player_name
        self.score: int = 0
        self.status: PlayerStatus = PlayerStatus(ENABLED)
        self.last_activity_time: float = time.time()

    def update_activity_time(self):
        self.last_activity_time = time.time()

    def reset(self):
        self.score = 0
        self.update_activity_time()

    def get_time_left_before_kick(self) -> float:
        current_time: float = time.time()
        return self.last_activity_time + AFK_TIMEOUT - current_time
