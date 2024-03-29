import pytest
import json
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from game.models import Game, Player

@pytest.mark.middle
@pytest.mark.auth
def test_unauthenticated_access(api_client, game):
    response = api_client.get(f'/api/game/{game.id}/')
    assert response.status_code == 403

@pytest.mark.middle
@pytest.mark.auth
def test_unauthorized_game_update(authenticated_client, game):
    # Create a new game that the authenticated user did not create
    unauthorized_game = Game.objects.create(
        ball_position={'x': 0, 'y': 0},
        ball_velocity={'x': 1, 'y': 1},
        paddle_positions={'left': 0, 'right': 0},
        game_state="ongoing",
    )
    data = {
        'ball_position': {'x': 1, 'y': 1},
        'ball_velocity': {'x': 2, 'y': 2},
        'paddle_positions': {'left': 1, 'right': 1},
    }
    response = authenticated_client.patch(
        f'/api/game/{unauthorized_game.id}/update/', 
        data=json.dumps(data), 
        content_type='application/json'
    )
    assert response.status_code == 403

@pytest.mark.middle
@pytest.mark.auth
def test_invalid_game_update(authenticated_client, game):
    data = {
        'ball_position': {'x': 100, 'y': 100},
    }
    response = authenticated_client.patch(
        f'/api/game/{game.id}/update/', 
        data=json.dumps(data), 
        content_type='application/json'
    )
    assert response.status_code == 400
    data = "This is not JSON"
    response = authenticated_client.patch(
        f'/api/game/{game.id}/update/', 
        data=data, 
        content_type='application/json'
    )
    assert response.status_code == 400

@pytest.mark.middle
@pytest.mark.auth
def test_missing_required_fields_in_game_update(authenticated_client, game):
    data = {
        'ball_position': {'x': 1, 'y': 1},
        # Missing 'ball_velocity' and 'paddle_positions'
    }
    response = authenticated_client.patch(
        f'/api/game/{game.id}/update/', 
        data=json.dumps(data), 
        content_type='application/json'
    )
    assert response.status_code == 400