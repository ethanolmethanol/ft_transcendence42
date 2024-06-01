# import pytest

# from back_game.game_entities.paddle import Paddle

# @pytest.mark.soft
# @pytest.mark.paddle
# @pytest.mark.parametrize("num_players, player_slot", [
#     (2, 1),
#     (2, 2),
#     (3, 1),
#     (3, 2),
#     (3, 3),
# ])
# def test_paddle_initialization(num_players, player_slot):
#     paddle = Paddle(slot=player_slot, num_players=num_players)
#     assert paddle.slot == player_slot
#     assert paddle.position.to_dict() == {
#         'x': round((paddle.axis['start'].x + paddle.axis['end'].x) / 2),
#         'y': round((paddle.axis['start'].y + paddle.axis['end'].y) / 2)
#     }

# # # @pytest.mark.middle
# # # @pytest.mark.paddle
# # # @pytest.mark.parametrize("initial_size, adjustment, expected_size", [
# # #     (10, 5, 15),  # Increase size
# # #     (15, -5, 10),  # Decrease size
# # #     (5, -10, 1),  # Attempt to decrease below minimum size, clamped to 1
# # # ])
# # # def test_paddle_size_adjustment(initial_size, adjustment, expected_size):
# # #     paddle = Paddle(size=initial_size)
# # #     paddle.adjust_size(adjustment)
# # #     assert paddle.size == expected_size
# # #
# # # @pytest.mark.edge
# # # @pytest.mark.paddle
# # # def test_rapid_sequential_actions(authenticated_clients, game):
# # #     client1, client2 = authenticated_clients  # Assuming this fixture provides two authenticated clients
# # #     game_id = game.id
# # #
# # #     # Move paddles in rapid succession on separate threads to simulate near-simultaneous actions
# # #     thread1 = Thread(target=move_paddle, args=(client1, game_id, {'left': 20}))
# # #     thread2 = Thread(target=move_paddle, args=(client2, game_id, {'right': 20}))
# # #
# # #     thread1.start()
# # #     thread2.start()
# # #     thread1.join()
# # #     thread2.join()
# # #
# # #     # Fetch the updated game state
# # #     response = client1.get(f'/api/game/{game_id}/')
# # #     game_state = response.json()
# # #
# # #     # Check that both paddle positions have been updated accurately
# # #     assert game_state['paddle_positions']['left'] == 20, "Left paddle did not update correctly."
# # #     assert game_state['paddle_positions']['right'] == 20, "Right paddle did not update correctly."


