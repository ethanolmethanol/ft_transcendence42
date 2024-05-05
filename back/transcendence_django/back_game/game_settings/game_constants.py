# Channels errors
NOT_JOINED = 1
INVALID_ARENA = 2
INVALID_CHANNEL = 3

# Game area dimensions
GAME_HEIGHT = 500
GAME_WIDTH = 700

# Game arena
MIN_PLAYER = 2
MAX_PLAYER = 10

# # Ball parameters
# BALL_INITIAL_POSITION = {'x': 50, 'y': 50}
# BALL_INITIAL_VELOCITY = {'x': 5, 'y': 5}
INITIAL_SPEEDX = 5
INITIAL_SPEEDY = 5
BALL_RADIUS = 15

# Paddle parameters
PADDLE_INITIAL_SPEED_RATE = 0.025
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
PADDLE_OFFSET = 60

# Game mode
LOCAL_MODE = 0
ONLINE_MODE = 1

# Game status
WAITING = 0
STARTED = 1
OVER = 2
# When all arenas are DEAD, the corresponding channel can be deleted
DYING = 3
DEAD = 4

# Game loop parameters
MONITOR_LOOP_INTERVAL = 0.5
RUN_LOOP_INTERVAL = 0.01
TIMEOUT_GAME_OVER = 5
TIMEOUT_INTERVAL = 1
