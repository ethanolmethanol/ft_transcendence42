import pytest
import json
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from game.models import Game, Player

@pytest.mark.soft
@pytest.mark.api
def test_game_initialization(authenticated_client, game):
    response = authenticated_client.get(f'/api/game/{game.id}/')
    assert response.status_code == 200
    response_data = json.loads(response.content)
    assert response_data['ball_position'] == {'x': 0, 'y': 0}
    assert response_data['paddle_positions'] == {'left': 0, 'right': 0}
    assert response_data['game_state'] == 'ongoing'

@pytest.mark.soft
@pytest.mark.api
def test_game_update(authenticated_client, game):
    data = {
        'ball_position': {'x': 1, 'y': 1},
        'ball_velocity': {'x': 2, 'y': 2},
        'paddle_positions': {'left': 1, 'right': 1},
        'game_state': 'ongoing'
    }
    response = authenticated_client.patch(
        f'/api/game/{game.id}/update/', 
        data=json.dumps(data), 
        content_type='application/json'
    )
    assert response.status_code == 200
    assert json.loads(response.content) == {'message': 'Game state updated'}

@pytest.mark.soft
@pytest.mark.api
def test_player_join(authenticated_client, game):
    response = authenticated_client.post(f'/api/game/{game.id}/join/')
    assert response.status_code == 200
    assert json.loads(response.content) == {'message': 'Player joined game'}

@pytest.mark.middle
@pytest.mark.api
@pytest.mark.parametrize("score1, score2, expected_winner, expected_loser", [
    (10, 8, 'testuser1', 'testuser2'),
    (7, 10, 'testuser2', 'testuser1'),
])
def test_game_result(authenticated_client, game, test_user1, test_user2, score1, score2, expected_winner, expected_loser):
    Player.objects.filter(user=test_user1, game=game).update(score=score1)
    Player.objects.filter(user=test_user2, game=game).update(score=score2)
    game.game_state = "finished"
    game.save()

    response = authenticated_client.get(f'/api/game/{game.id}/result/')
    assert response.status_code == 200
    result = json.loads(response.content)
    assert result['winner'] == expected_winner
    assert result['loser'] == expected_loser
    assert 'scores' in result

@pytest.mark.middle
@pytest.mark.api
def test_game_progression(authenticated_client, game):
    data = {
        'ball_position': {'x': 1, 'y': 1},
        'ball_velocity': {'x': 2, 'y': 2},
        'paddle_positions': {'left': 1, 'right': 1},
    }
    response = authenticated_client.patch(
        f'/api/game/{game.id}/update/', 
        data=json.dumps(data), 
        content_type='application/json'
    )
    assert response.status_code == 200
    assert json.loads(response.content) == {'message': 'Game state updated'}

# @pytest.mark.parametrize("score1, score2, expected_winner, expected_loser", [
#     (10, 8, 'testuser1', 'testuser2'),
#     (7, 10, 'testuser2', 'testuser1'),
# ])
@pytest.mark.middle
@pytest.mark.api
def test_game_termination_by_score(authenticated_client, game, test_user1, test_user2):
    Player.objects.filter(user=test_user1, game=game).update(score=10)
    game.game_state = "finished"
    game.save()

    response = authenticated_client.get(f'/api/game/{game.id}/result/')
    assert response.status_code == 200
    result = json.loads(response.content)
    assert result['winner'] == 'testuser1'
    assert result['loser'] == 'testuser2'

@pytest.mark.middle
@pytest.mark.api
def test_update_nonexistent_game(authenticated_client):
    data = {
        'ball_position': {'x': 1, 'y': 1},
        'ball_velocity': {'x': 2, 'y': 2},
        'paddle_positions': {'left': 1, 'right': 1},
    }
    response = authenticated_client.patch(
        '/api/game/9999/update/', 
        data=json.dumps(data), 
        content_type='application/json'
    )
    assert response.status_code == 404

@pytest.mark.middle
@pytest.mark.api
def test_game_state_transition(authenticated_client, game):
    game.game_state = "ongoing"
    game.save()
    
    data = {
        'ball_position': {'x': 5, 'y': 5},
        'ball_velocity': {'x': 1, 'y': 1},
        'paddle_positions': {'left': 2, 'right': 2},
    }
    response = authenticated_client.patch(
        f'/api/game/{game.id}/update/',
        data=json.dumps(data),
        content_type='application/json'
    )
    assert response.status_code == 200
    assert json.loads(response.content) == {'message': 'Game state updated'}
    
    game.game_state = "finished"
    game.save()
    response = authenticated_client.get(f'/api/game/{game.id}/')
    response_data = json.loads(response.content)
    assert response_data['game_state'] == 'finished'

@pytest.mark.middle
@pytest.mark.api
def test_game_result_consistency(authenticated_client, game, test_user1, test_user2):
    game.game_state = "ongoing"
    game.save()
    
    Player.objects.filter(user=test_user1, game=game).update(score=12)
    Player.objects.filter(user=test_user2, game=game).update(score=10)
    game.game_state = "finished"
    game.save()
    
    response = authenticated_client.get(f'/api/game/{game.id}/result/')
    assert response.status_code == 200
    result = json.loads(response.content)
    assert result['winner'] == test_user1.username
    assert result['loser'] == test_user2.username
    assert result['scores'][test_user1.username] == 12
    assert result['scores'][test_user2.username] == 10

@pytest.mark.edge
@pytest.mark.api
@pytest.mark.django_db
def test_player_quick_disconnect_reconnect(authenticated_client, game):
    """
    Test what happens when a player disconnects and then quickly reconnects.
    """

    # Simulate a player disconnecting
    game.remove_player(player=game.players.first())
    assert game.players.count() == 1, "Player was not removed correctly."

    # Simulate the player quickly reconnecting
    game.add_player(player=game.players.first())
    assert game.players.count() == 2, "Player was not re-added correctly."

    # Further assertions can be added to validate the state of the game
    # and ensure that it has handled the reconnect as expected.

@pytest.mark.edge
@pytest.mark.api
def test_action_during_high_latency(authenticated_client, game, monkeypatch):
    # Simulate high network latency
    def simulated_latency(*args, **kwargs):
        sleep(2)  # Simulate a 2-second network delay

    monkeypatch.setattr('path.to.your.network.request.function', simulated_latency)

    game_id = game.id
    response = move_paddle(authenticated_client, game_id, {'left': 30})
    
    assert response.status_code == 200, "Action was lost or not processed correctly during high latency."

    # Check the game state to ensure consistency
    response = authenticated_client.get(f'/api/game/{game_id}/')
    game_state = response.json()
    
    assert game_state['paddle_positions']['left'] == 30, "Game state is not consistent for all players after high latency action."

@pytest.mark.edge
@pytest.mark.api
def test_simultaneous_score_and_collision(setup_game):
    game = setup_game
    # Set the ball's position and velocity to simulate a scenario where it might collide and score simultaneously
    game.ball.position = (190, 50)  # Near the right edge, close to the right paddle
    game.ball.velocity = (10, 0)  # Moving towards the right edge/paddle
    
    # Assume a method to update game state; this will need to check for collisions and scoring
    game.update_game_state()
    
    # Depending on your game's rules, you need to define what the expected outcome is.
    # Here, we assert that a collision takes precedence over scoring, but your game might differ.
    assert game.ball.velocity == (-10, 0), "Ball did not bounce back; collision not detected."
    assert game.scores == (0, 0), "Score was incorrectly registered."

@pytest.mark.middle
@pytest.mark.api
def test_boundary_conditions(setup_game):
    game = setup_game
    # Test ball at boundary
    game.ball.position = (0, 50)  # Exactly at the left edge
    game.ball.velocity = (-10, 0)  # Moving towards the edge
    
    game.update_game_state()
    
    # Check for correct handling (e.g., ball bounces back or game resets)
    # This assertion depends on your game logic; adjust as needed.
    assert game.ball.velocity == (10, 0), "Ball did not handle boundary condition correctly."
    
    # Test paddle at boundary
    game.paddles['left'].position = (0, 50)  # Exactly at the left edge
    # Assume a method that moves the paddle; simulate an attempt to move beyond the boundary
    game.paddles['left'].move(-10)
    
    # Check that the paddle did not move beyond the boundary
    assert game.paddles['left'].position == (0, 50), "Paddle moved beyond the boundary."

@pytest.mark.middle
@pytest.mark.api
def test_unexpected_user_disconnection(setup_game):
    game = setup_game
    # Simulate a user about to win
    game.scores = (10, 9)  # Assuming a score of 11 is needed to win
    
    # Simulate user disconnection at this critical moment
    # Assuming 'disconnect_player' is a method that handles player disconnection
    game.disconnect_player('left')
    
    # The test expectations might vary based on your game logic
    # Here we assume the game pauses and waits for reconnection
    assert game.state == "paused", "Game did not pause upon user disconnection."
    
    # Optionally, test reconnection logic
    game.reconnect_player('left')
    assert game.state == "active", "Game did not resume correctly after player reconnected."
    
    # Depending on game rules, check if the game correctly handles potential scoring or loss due to disconnection
    # For example, does the game award a point to the other player, or does it wait for reconnection?


@pytest.mark.middle
@pytest.mark.api
def test_maximum_score_limit(setup_game):
    game = setup_game
    # Assuming 10 is the maximum score limit for the game
    max_score_limit = 10
    game.scores = (9, 9)  # Set both players just below the max score limit

    # Simulate a scenario where both players might score simultaneously
    # Depending on your game logic, you might need to simulate this differently
    game.score('left')
    game.score('right')

    assert game.state == "ended", "Game did not end when maximum score limit was reached."
    # This assertion depends on how your game is supposed to handle simultaneous final points
    assert game.scores == (10, 10) or (max_score_limit in game.scores), "Scores did not update correctly at maximum score limit."
    # Further, assert on what your game logic dictates should happen in this scenario (who wins, or if it's a draw, etc.)

@pytest.mark.edge
@pytest.mark.api
def test_long_duration_game_behavior(setup_game):
    game = setup_game
    # Simulate a long game duration
    # Note: This is a basic simulation; consider using tools or mocks for time acceleration in actual tests
    for _ in range(10000):  # Simulate a large number of game cycles/actions
        game.update()  # Assuming `update` is a method that advances game state

    # Assertions to check for memory leaks, performance degradation, or state management issues
    # These are more complex to assert in a unit test and might require profiling or specific checks
    assert True  # Placeholder for actual performance/memory checks

    # Ensure game state remains consistent and no unexpected behaviors occur
    # This might include checking that scores haven't unexpectedly reset, game hasn't frozen, etc.
    assert game.state not in ["ended", "error"], "Game entered an unexpected state during long-duration play."

