# import pytest
# from game.game_entities.paddle import Paddle
# from game.game_settings.game_constants import LEFT, RIGHT


# @pytest.mark.soft
# @pytest.mark.paddle
# @pytest.mark.parametrize("num_players, player_slot", [
#     (2, 0,),
#     (2, 1),
#     (3, 0),
#     (3, 1),
#     (3, 2),
# ])
# def test_paddle_initialization(num_players, player_slot):
#     paddle = Paddle(num_players=num_players, player_slot=player_slot)
#     assert paddle._num_players == num_players
#     assert paddle._player_slot == player_slot
#     assert paddle._position == {
#         'x': (paddle._axis[0]['x'] + paddle._axis[1]['x']) / 2,
#         'y': (paddle._axis[0]['y'] + paddle._axis[1]['y']) / 2
#     }

# @pytest.mark.soft
# @pytest.mark.paddle
# @pytest.mark.parametrize("num_players, player_slot", [
#     (2, 0),
#     (2, 1),
#     (3, 1),
#     (3, 2),
#     (3, 3),
# ])
# def test_paddle_movement(num_players, player_slot):
#     paddle = Paddle(num_players=num_players, player_slot=player_slot)
#     paddle.move(100)
#     assert paddle._position == {
#         'x': round(paddle._axis[1]['x']),
#         'y': round(paddle._axis[1]['y'])
#     }
#     paddle.move(50)
#     assert paddle._position == {
#         'x': round((paddle._axis[0]['x'] + paddle._axis[1]['x']) / 2),
#         'y': round((paddle._axis[0]['y'] + paddle._axis[1]['y']) / 2)
#     }
#     paddle.move(0)
#     assert paddle._position == {
#         'x': round(paddle._axis[0]['x']),
#         'y': round(paddle._axis[0]['y'])
#     }


# @pytest.mark.soft
# @pytest.mark.paddle
# @pytest.mark.parametrize("num_players, player_slot", [
#     (2, 0),
#     (2, 1),
#     (3, 1),
#     (3, 2),
#     (3, 3),
# ])
# def test_something_that_should_fail(num_players, player_slot):
#     paddle = Paddle(num_players=num_players, player_slot=player_slot)
#     with pytest.raises(ValueError, match="Percentage must be between 0 and 100"):
#         paddle.move(-3)

# # @pytest.mark.soft
# # @pytest.mark.paddle
# # def test_paddle_boundaries():
# #     upper_boundary = 0
# #     lower_boundary = 100
# #     paddle = Paddle(position=50)
# #
# #     paddle.move(-60)  # Attempt to move above the upper boundary
# #     assert paddle.position == upper_boundary
# #
# #     paddle.position = 50  # Reset position
# #     paddle.move(60)  # Attempt to move below the lower boundary
# #     assert paddle.position == lower_boundary
# #
# # @pytest.mark.middle
# # @pytest.mark.paddle
# # @pytest.mark.parametrize("initial_size, adjustment, expected_size", [
# #     (10, 5, 15),  # Increase size
# #     (15, -5, 10),  # Decrease size
# #     (5, -10, 1),  # Attempt to decrease below minimum size, clamped to 1
# # ])
# # def test_paddle_size_adjustment(initial_size, adjustment, expected_size):
# #     paddle = Paddle(size=initial_size)
# #     paddle.adjust_size(adjustment)
# #     assert paddle.size == expected_size
# #
# # @pytest.mark.edge
# # @pytest.mark.paddle
# # def test_rapid_sequential_actions(authenticated_clients, game):
# #     client1, client2 = authenticated_clients  # Assuming this fixture provides two authenticated clients
# #     game_id = game.id
# #
# #     # Move paddles in rapid succession on separate threads to simulate near-simultaneous actions
# #     thread1 = Thread(target=move_paddle, args=(client1, game_id, {'left': 20}))
# #     thread2 = Thread(target=move_paddle, args=(client2, game_id, {'right': 20}))
# #
# #     thread1.start()
# #     thread2.start()
# #     thread1.join()
# #     thread2.join()
# #
# #     # Fetch the updated game state
# #     response = client1.get(f'/api/game/{game_id}/')
# #     game_state = response.json()
# #
# #     # Check that both paddle positions have been updated accurately
# #     assert game_state['paddle_positions']['left'] == 20, "Left paddle did not update correctly."
# #     assert game_state['paddle_positions']['right'] == 20, "Right paddle did not update correctly."
