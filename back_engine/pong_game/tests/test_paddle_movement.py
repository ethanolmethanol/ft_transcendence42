import pytest
import json
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from game.models import Game, Player

@pytest.mark.soft
@pytest.mark.paddle
def test_paddle_initialization():
    paddle = Paddle(position=20)  # Assuming vertical position along Y-axis
    assert paddle.position == 20

@pytest.mark.soft
@pytest.mark.paddle
@pytest.mark.parametrize("initial_position, move_amount, expected_position", [
    (20, 5, 25),  # Move down
    (20, -10, 10),  # Move up
    (90, 10, 100),  # Attempt to move beyond the lower boundary, clamped to 100
    (10, -15, 0),  # Attempt to move beyond the upper boundary, clamped to 0
])
def test_paddle_movement(initial_position, move_amount, expected_position):
    paddle = Paddle(position=initial_position)
    paddle.move(move_amount)
    assert paddle.position == expected_position

@pytest.mark.soft
@pytest.mark.paddle
def test_paddle_boundaries():
    upper_boundary = 0
    lower_boundary = 100
    paddle = Paddle(position=50)

    paddle.move(-60)  # Attempt to move above the upper boundary
    assert paddle.position == upper_boundary

    paddle.position = 50  # Reset position
    paddle.move(60)  # Attempt to move below the lower boundary
    assert paddle.position == lower_boundary

@pytest.mark.middle
@pytest.mark.paddle
@pytest.mark.parametrize("initial_size, adjustment, expected_size", [
    (10, 5, 15),  # Increase size
    (15, -5, 10),  # Decrease size
    (5, -10, 1),  # Attempt to decrease below minimum size, clamped to 1
])
def test_paddle_size_adjustment(initial_size, adjustment, expected_size):
    paddle = Paddle(size=initial_size)
    paddle.adjust_size(adjustment)
    assert paddle.size == expected_size

@pytest.mark.edge
@pytest.mark.paddle
def test_rapid_sequential_actions(authenticated_clients, game):
    client1, client2 = authenticated_clients  # Assuming this fixture provides two authenticated clients
    game_id = game.id

    # Move paddles in rapid succession on separate threads to simulate near-simultaneous actions
    thread1 = Thread(target=move_paddle, args=(client1, game_id, {'left': 20}))
    thread2 = Thread(target=move_paddle, args=(client2, game_id, {'right': 20}))

    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    # Fetch the updated game state
    response = client1.get(f'/api/game/{game_id}/')
    game_state = response.json()

    # Check that both paddle positions have been updated accurately
    assert game_state['paddle_positions']['left'] == 20, "Left paddle did not update correctly."
    assert game_state['paddle_positions']['right'] == 20, "Right paddle did not update correctly."
