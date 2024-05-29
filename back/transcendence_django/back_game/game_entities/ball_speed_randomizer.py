import logging
import random

from back_game.game_physics.speed import Speed
from back_game.game_settings.game_constants import INITIAL_SPEED_X, INITIAL_SPEED_Y

logger = logging.getLogger(__name__)

random_ball_speeds = [
    {
        Speed(-INITIAL_SPEED_X, 0),
        Speed(-INITIAL_SPEED_X, -INITIAL_SPEED_Y / 2),
        Speed(-INITIAL_SPEED_X, INITIAL_SPEED_Y / 2),
        Speed(-INITIAL_SPEED_X, INITIAL_SPEED_Y / 3),
        Speed(-INITIAL_SPEED_X, -INITIAL_SPEED_Y / 3),
    },
    {
        Speed(INITIAL_SPEED_X, 0),
        Speed(INITIAL_SPEED_X, -INITIAL_SPEED_Y / 2),
        Speed(INITIAL_SPEED_X, INITIAL_SPEED_Y / 2),
        Speed(INITIAL_SPEED_X, -INITIAL_SPEED_Y / 3),
    },
]


class BallSpeedRandomizer:

    @staticmethod
    def generate_random_speed(player_turn) -> Speed:
        chosen_set = random_ball_speeds[player_turn]
        random_speed = random.choice(list(chosen_set))
        return random_speed
