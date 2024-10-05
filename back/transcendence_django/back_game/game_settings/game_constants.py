import math
from enum import IntEnum

from transcendence_django.dict_keys import IS_REMOTE, NB_PLAYERS, OPTIONS

# Lobby errors
NOT_JOINED = 1
INVALID_ARENA = 2
INVALID_LOBBY = 3
NOT_ENTERED = 4
UNKNOWN_LOBBY_ID = "Unknown lobby_id"
UNKNOWN_ARENA_ID = "Unknown arena_id"

# Game area dimensions
GAME_HEIGHT = 800
GAME_WIDTH = 1200

# Game arena
MIN_PLAYER = 2
MAX_PLAYER = 2
MAXIMUM_SCORE = 10

# # Ball parameters
INITIAL_SPEED_X = 5
INITIAL_SPEED_Y = 5
INITIAL_BALL_SPEED_COEFF = math.sqrt(INITIAL_SPEED_X**2 + INITIAL_SPEED_Y**2)
BALL_RADIUS = 15
SPEED_INCREASE_RATE = 1.05

# Paddle parameters
PADDLE_INITIAL_SPEED_RATE = 0.025
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
PADDLE_OFFSET = PADDLE_WIDTH / 2
LEFT_SLOT = 1
RIGHT_SLOT = 2
BOTTOM_SLOT = 3
TOP_SLOT = 4
CONVEXITY = 90
VALID_DIRECTIONS = [-1, 1]

# Tournament

TOURNAMENT_SPECS = {
    NB_PLAYERS: 2,
    IS_REMOTE: "online",
    OPTIONS: {
        "ball_speed": 2,
        "paddle_size": 2,
        "human_opponents_local": 1,
        "human_opponents_online": 0,
        "ai_opponents_local": 0,
        "ai_opponents_online": 0,
        "is_private": 0,
    },
}

TOURNAMENT_ARENA_COUNT = 2
TOURNAMENT_MAX_ROUND = int(math.log2(TOURNAMENT_ARENA_COUNT) + 1)

# Game loop parameters
ARENA_LOOP_INTERVAL = 0.5
LOBBY_LOOP_INTERVAL = 0.5
MONITOR_LOOP_INTERVAL = 0.5
NEXT_ROUND_LOOP_INTERVAL = 0.5
WAIT_NEXT_ROUND_INTERVAL = 3
RUN_LOOP_INTERVAL = 0.005
TIMEOUT_GAME_OVER = 5
TIMEOUT_INTERVAL = 1
AFK_TIMEOUT = 30  # seconds
AFK_WARNING_THRESHOLD = 10  # seconds

TIME_START = 3
TIME_START_INTERVAL = 1

# Rectangle
TANGENT_FACTOR = 1 / (2 * math.tan(CONVEXITY / 2))

class PaddleStatus(IntEnum):
    LISTENING = 1
    PROCESSING = 2
    MOVED = 3

class GameStatus(IntEnum):
    CREATED = 0
    WAITING = 1
    READY_TO_START = 2
    STARTED = 3
    OVER = 4
    DYING = 5
    DEAD = 6
