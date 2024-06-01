# import pytest
# import json
# from django.contrib.auth.models import User
# # from rest_framework.test import stateClient
# #from game.models import Game, Player
# from django.urls import reverse
# # from rest_framework import status

# @pytest.mark.soft
# @pytest.mark.state
# def test_create_game(authenticated_client):
#     response = authenticated_client.post(reverse('game:create'))
#     assert response.status_code == status.HTTP_201_CREATED
#     assert Game.objects.exists()

# @pytest.mark.soft
# @pytest.mark.state
# def test_join_game(authenticated_client, game):
#     response = authenticated_client.post(reverse('game:join', kwargs={'pk': game.pk}))
#     assert response.status_code == status.HTTP_200_OK
#     response_data = json.loads(response.content)
#     assert response_data['message'] == 'Player joined game'

# @pytest.mark.soft
# @pytest.mark.state
# def test_update_game_state(authenticated_client, game):
#     update_data = {
#         'ball_position': {'x': 5, 'y': 5},
#         'paddle_positions': {'left': 2, 'right': 3},
#     }
#     response = authenticated_client.patch(reverse('game:update', kwargs={'pk': game.pk}), data=json.dumps(update_data), content_type='application/json')
#     assert response.status_code == status.HTTP_200_OK
#     game.refresh_from_db()
#     assert game.ball_position == update_data['ball_position']
#     assert game.paddle_positions == update_data['paddle_positions']

# @pytest.mark.middle
# @pytest.mark.state
# def test_game_result(authenticated_client, game, test_user1, test_user2):
#     response = authenticated_client.get(reverse('game:result', kwargs={'pk': game.pk}))
#     assert response.status_code == status.HTTP_200_OK
#     results = json.loads(response.content)
#     assert 'winner' in results
#     assert 'loser' in results

# # Testing game progression by updating game state
# @pytest.mark.middle
# @pytest.mark.state
# def test_game_progression(authenticated_client, game):
#     data = {
#         'ball_position': {'x': 1, 'y': 1},
#         'ball_velocity': {'x': 2, 'y': 2},
#         'paddle_positions': {'left': 1, 'right': 1},
#     }
#     url = reverse('game-update', kwargs={'pk': game.id})  # Adjust 'game-update' to your actual URL name
#     response = authenticated_client.patch(url, data=json.dumps(data), content_type='application/json')
#     assert response.status_code == status.HTTP_200_OK
#     assert json.loads(response.content) == {'message': 'Game state updated'}

# # Testing game termination by reaching a specific score
# @pytest.mark.middle
# @pytest.mark.state
# def test_game_termination_by_score(authenticated_client, game, test_user1, test_user2):
#     Player.objects.filter(user=test_user1, game=game).update(score=10)
#     game.game_state = "finished"
#     game.save()

#     url = reverse('game-result', kwargs={'pk': game.id})  # Adjust 'game-result' to your actual URL name
#     response = authenticated_client.get(url)
#     assert response.status_code == status.HTTP_200_OK
#     result = json.loads(response.content)
#     assert result['winner'] == test_user1.username
#     assert result['loser'] == test_user2.username

# # Testing attempt to update a nonexistent game
# @pytest.mark.middle
# @pytest.mark.state
# def test_update_nonexistent_game(authenticated_client):
#     data = {
#         'ball_position': {'x': 1, 'y': 1},
#         'ball_velocity': {'x': 2, 'y': 2},
#         'paddle_positions': {'left': 1, 'right': 1},
#     }
#     url = reverse('game-update', kwargs={'pk': 9999})  # Adjust 'game-update' to your actual URL name
#     response = authenticated_client.patch(url, data=json.dumps(data), content_type='application/json')
#     assert response.status_code == status.HTTP_404_NOT_FOUND

# # Testing game state transition from "ongoing" to "finished"
# @pytest.mark.middle
# @pytest.mark.state
# def test_game_state_transition(authenticated_client, game):
#     game.game_state = "ongoing"
#     game.save()
    
#     data = {
#         'ball_position': {'x': 5, 'y': 5},
#         'ball_velocity': {'x': 1, 'y': 1},
#         'paddle_positions': {'left': 2, 'right': 2},
#     }
#     url = reverse('game-update', kwargs={'pk': game.id})  # Adjust 'game-update' to your actual URL name
#     response = authenticated_client.patch(url, data=json.dumps(data), content_type='application/json')
#     assert response.status_code == status.HTTP_200_OK
#     assert json.loads(response.content) == {'message': 'Game state updated'}
    
#     game.game_state = "finished"
#     game.save()
#     url = reverse('game-detail', kwargs={'pk': game.id})  # Adjust 'game-detail' to your actual URL name
#     response = authenticated_client.get(url)
#     assert response.status_code == status.HTTP_200_OK
#     response_data = json.loads(response.content)
#     assert response_data['game_state'] == 'finished'

# # Testing consistency of game result
# @pytest.mark.middle
# @pytest.mark.state
# def test_game_result_consistency(authenticated_client, game, test_user1, test_user2):
#     game.game_state = "ongoing"
#     game.save()
    
#     Player.objects.filter(user=test_user1, game=game).update(score=12)
#     Player.objects.filter(user=test_user2, game=game).update(score=10)
#     game.game_state = "finished"
#     game.save()
    
#     url = reverse('game-result', kwargs={'pk': game.id})  # Adjust 'game-result' to your actual URL name
#     response = authenticated_client.get(url)
#     assert response.status_code == status.HTTP_200_OK
#     result = json.loads(response.content)
#     assert result['winner'] == test_user1.username
#     assert result['loser'] == test_user2.username
#     assert result['scores'][test_user1.username] == 12
#     assert result['scores'][test_user2.username] == 10


# @pytest.mark.edge
# @pytest.mark.state
# @pytest.mark.django_db
# def test_player_quick_disconnect_reconnect(authenticated_client, game):
#     """
#     Tests the game's behavior when a player disconnects and quickly reconnects.
#     """
#     # Assuming game.remove_player() and game.add_player() are defined
#     initial_player_count = game.players.count()

#     # Simulate a player disconnecting
#     disconnected_player = game.players.first()
#     game.remove_player(player=disconnected_player)
#     assert game.players.count() == initial_player_count - 1, "Failed to remove player."

#     # Simulate the player quickly reconnecting
#     game.add_player(player=disconnected_player)
#     assert game.players.count() == initial_player_count, "Failed to re-add player."

# @pytest.mark.edge
# @pytest.mark.state
# def test_action_during_high_latency(authenticated_client, game, monkeypatch):
#     """
#     Simulates an action (e.g., moving a paddle) during high network latency.
#     """
#     # Patching a hypothetical request method to simulate latency
#     def simulated_latency(*args, **kwargs):
#         time.sleep(2)  # Simulates a 2-second network delay

#     monkeypatch.setattr('your_module.your_network_request_function', simulated_latency)

#     # Assuming move_paddle() is defined and correctly patches network latency
#     response = move_paddle(authenticated_client, game.id, {'direction': 'left', 'distance': 30})
#     assert response.status_code == 200, "Failed to process action under high latency."

#     # Ensure game state is consistent post-latency
#     game.refresh_from_db()  # Assuming Django ORM usage for refreshing game instance
#     assert game.paddle_positions['left'] == 30, "Game state inconsistent after high latency action."

# @pytest.mark.edge
# @pytest.mark.state
# def test_simultaneous_score_and_collision(setup_game):
#     """
#     Tests game behavior when a score and a collision occur simultaneously.
#     """
#     game = setup_game
#     # Setting conditions for simultaneous score and collision
#     game.ball.position = (190, 50)  # Near the edge and a paddle
#     game.ball.velocity = (10, 0)  # Towards the edge/paddle

#     game.update_game_state()  # Assuming this checks collisions and scores

#     # Assert based on game's rules. Here, assuming collision takes precedence
#     assert game.ball.velocity == (-10, 0), "Collision not properly handled."
#     assert game.scores == (0, 0), "Score improperly registered."

# @pytest.mark.middle
# @pytest.mark.state
# def test_boundary_conditions(setup_game):
#     """
#     Tests handling of ball and paddle at game boundaries.
#     """
#     game = setup_game
#     # Ball at left edge, moving left
#     game.ball.position = (0, 50)
#     game.ball.velocity = (-10, 0)
#     game.update_game_state()
#     assert game.ball.velocity == (10, 0), "Ball boundary condition not handled correctly."

#     # Paddle at left edge, attempt to move left
#     game.paddles['left'].position = (0, 50)
#     game.paddles['left'].move(-10)
#     assert game.paddles['left'].position == (0, 50), "Paddle boundary condition not handled correctly."

# @pytest.mark.middle
# @pytest.mark.state
# def test_unexpected_user_disconnection(setup_game):
#     """
#     Tests game behavior upon unexpected user disconnection.
#     """
#     game = setup_game
#     game.scores = (10, 9)  # Critical moment before winning

#     game.disconnect_player('left')  # Simulate disconnection
#     assert game.state == "paused", "Game did not pause on disconnection."

#     game.reconnect_player('left')
#     assert game.state == "active", "Game did not resume after reconnection."

# @pytest.mark.middle
# @pytest.mark.state
# def test_maximum_score_limit(setup_game):
#     """
#     Ensures the game ends correctly when reaching the maximum score limit.
#     """
#     game = setup_game
#     max_score_limit = 10
#     game.scores = (9, 9)  # Both players close to winning

#     game.score('left')
#     game.score('right')
#     assert game.state == "ended", "Game did not end at max score limit."
#     assert game.scores in [(10, 10), (max_score_limit, max_score_limit)], "Incorrect scores at game end."

# @pytest.mark.edge
# @pytest.mark.state
# def test_long_duration_game_behavior(setup_game):
#     """
#     Checks for any issues in long-duration games, such as memory leaks or inconsistencies.
#     """
#     game = setup_game
#     for _ in range(10000):  # Simulate prolonged game play
#         game.update_game_state()  # Update game state

#     # Placeholder for performance or memory checks
#     assert True, "Placeholder for actual assertions."

#     assert game.state not in ["ended", "error"], "Unexpected game state after long-duration play."
