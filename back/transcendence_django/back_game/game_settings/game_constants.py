import math

# Channels errors
NOT_JOINED = 1
INVALID_ARENA = 2
INVALID_CHANNEL = 3
NOT_ENTERED = 4
UNKNOWN_CHANNEL_ID = "Unknown channel_id"
UNKNOWN_ARENA_ID = "Unknown arena_id"

# Game area dimensions
GAME_HEIGHT = 600
GAME_WIDTH = 1000

# Game arena
MIN_PLAYER = 2
MAX_PLAYER = 10
MAXIMUM_SCORE = 10

# # Ball parameters
INITIAL_SPEED_X = 5
INITIAL_SPEED_Y = 5
INITIAL_BALL_SPEED_COEFF = math.sqrt(INITIAL_SPEED_X**2 + INITIAL_SPEED_Y**2)
BALL_RADIUS = 15

# Paddle parameters
PADDLE_INITIAL_SPEED_RATE = 0.025
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
PADDLE_OFFSET = PADDLE_WIDTH / 2
LEFT_SLOT = 1
RIGHT_SLOT = 2
CONVEXITY = 90
VALID_DIRECTIONS = [-1, 1]

# Game mode
# LOCAL_MODE = 0
# ONLINE_MODE = 1

# Tournament

DEFAULT_TOURNAMENT_SPECS = {
    "nb_players": 2,
    "type": "online",
    "options": {
        "ball_speed": 2,
        "paddle_size": 2,
        "human_players": 1,
        "online_players": 1,
        "ai_opponents_local": 0,
        "ai_opponents_online": 0,
        "is_private": 0
    },
}

TOURNAMENT_ARENA_COUNT = 2

# Game status
CREATED = 0
WAITING = 1
READY_TO_START = 2
STARTED = 3
OVER = 4
DYING = 5
DEAD = 6

# Game loop parameters
MONITOR_LOOP_INTERVAL = 0.5
RUN_LOOP_INTERVAL = 0.005
TIMEOUT_GAME_OVER = 5
TIMEOUT_INTERVAL = 1
AFK_TIMEOUT = 30  # seconds
AFK_WARNING_THRESHOLD = 10  # seconds

TIME_START = 3
TIME_START_INTERVAL = 1

# Paddle status
LISTENING = 1
PROCESSING = 2

# Rectangle
TANGENT_FACTOR = 1 / (2 * math.tan(CONVEXITY / 2))
