import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
#from game.models import Game, Player
from back_game.game_settings.game_constants import *


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user1(db):
    return User.objects.create_user(username='testuser1', password='testpassword1')


@pytest.fixture
def test_user2(db):
    return User.objects.create_user(username='testuser2', password='testpassword2')


@pytest.fixture
def game(db, test_user1, test_user2):
    game = Game.objects.create(
        ball_position={'x': 0, 'y': 0},
        ball_velocity={'x': 1, 'y': 1},
        paddle_positions={'left': 0, 'right': 0},
        game_state="ongoing",
    )
    Player.objects.create(user=test_user1, game=game, score=0, side='left', paddle_position=game.paddle_positions['left'])
    Player.objects.create(user=test_user2, game=game, score=0, side='right', paddle_position=game.paddle_positions['right'])
    return game

# @pytest.fixture
# def game_config():
#     # Set the dimensions of the arena
#     GAME_WIDTH = 100
#     GAME_HEIGHT = 100
#
#     # Set the dimensions of the paddles
#     PADDLE_WIDTH = 10
#     PADDLE_HEIGHT = 20
#
#     # Set the initial position of the ball
#     BALL_INITIAL_POSITION = {'x': 50, 'y': 50}
#
#     # Set the initial velocity of the ball
#     BALL_INITIAL_VELOCITY = {'x': 5, 'y': 5}
#
#     # Set the player slots
#     LEFT = 0
#     RIGHT = 1
#
#     return {
#         'GAME_WIDTH': GAME_WIDTH,
#         'GAME_HEIGHT': GAME_HEIGHT,
#         'PADDLE_WIDTH': PADDLE_WIDTH,
#         'PADDLE_HEIGHT': PADDLE_HEIGHT,
#         'BALL_INITIAL_POSITION': BALL_INITIAL_POSITION,
#         'BALL_INITIAL_VELOCITY': BALL_INITIAL_VELOCITY,
#         'LEFT': LEFT,
#         'RIGHT': RIGHT,
#     }

@pytest.fixture
def authenticated_client(api_client, test_user1):
    api_client.login(username='testuser1', password='testpassword1')
    return api_client