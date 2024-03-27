import pytest
import json
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from game.models import Game

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_user(db):
    return User.objects.create_user(username='testuser', password='testpassword')

@pytest.fixture
def game(db):
    return Game.objects.create(
        ball_postion={'x': 0, 'y': 0},
        ball_velocity={'x': 1, 'y': 1},
        paddle_positions={'left': 0, 'right': 0},
        game_state="ongoing",
    )

@pytest.fixture
def authenticated_client(api_client, test_user):
    api_client.login(username='testuser', password='testpass')
    return api_client

def test_game_initialization(authenticated_client, game):
    response = authenticated_client.get('/api/game/')
    assert response.status_code == 200
    assert json.loads(response.content) == {
        'message': 'Game state',
        'ball_position': {'x': 0, 'y': 0},
        'paddle_positions': {'left': 0, 'right': 0}
    }

def test_game_update(authenticated_client, game):
    data = {
        'ball_position': {'x': 1, 'y': 1},
        'ball_velocity': {'x': 2, 'y': 2},
        'paddle_positions': {'left': 1, 'right': 1}
    }
    response = authenticated_client.post('/api/game/', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert json.loads(response.content) == {'message': 'Game state updated'}