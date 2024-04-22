import math

# Game area dimensions
GAME_HEIGHT = 500
GAME_WIDTH = 700

# Game arena
MIN_PLAYER = 2
MAX_PLAYER = 10

# # Ball parameters
# BALL_INITIAL_POSITION = {'x': 50, 'y': 50}
# BALL_INITIAL_VELOCITY = {'x': 5, 'y': 5}
INITIAL_SPEEDX = -5
INITIAL_SPEEDY = 0
INITIAL_BALL_SPEED_COEFF = math.sqrt(INITIAL_SPEEDX**2 + INITIAL_SPEEDY**2)
BALL_RADIUS = 15

# Paddle parameters
PADDLE_INITIAL_SPEED_RATE = 0.025
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
PADDLE_OFFSET = 60
LEFT_SLOT = 1
RIGHT_SLOT = 2
CONVEXITY = 90

# Game mode
LOCAL_MODE = 0
ONLINE_MODE = 1

# Game status
WAITING = 0
STARTED = 1
OVER = 2
# When all arenas are DEAD, the corresponding channel can be deleted
DEAD = 3
