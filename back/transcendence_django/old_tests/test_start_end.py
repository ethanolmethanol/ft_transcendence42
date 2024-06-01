# import pytest
# import json
# from django.contrib.auth.models import User
# from rest_framework.test import APIClient
# from game.models import Game, Player

# @pytest.mark.soft
# @pytest.mark.start_end
# def test_game_initialization():
#     game = Game()
#     assert game.ball.position == (100, 50), "Ball did not initialize to the correct position."
#     assert game.paddles['left'].position == (10, 50), "Left paddle did not initialize to the correct position."
#     assert game.paddles['right'].position == (190, 50), "Right paddle did not initialize to the correct position."
#     assert game.scores == (0, 0), "Scores did not initialize to zero."
#     assert game.state == "waiting", "Game did not initialize in a 'waiting' state."

# @pytest.mark.soft
# @pytest.mark.start_end
# def test_game_start():
#     game = Game()
#     game.start()
#     assert game.state == "active", "Game did not correctly transition to an 'active' state upon starting."
#     assert game.ball.velocity != (0, 0), "Ball did not start moving upon game start."

# @pytest.mark.middle
# @pytest.mark.start_end
# @pytest.mark.parametrize("final_scores, expected_winner", [
#     ((10, 8), "left"), 
#     ((7, 10), "right"),
# ])
# def test_game_end_by_score(final_scores, expected_winner):
#     game = Game()
#     game.scores = final_scores
#     game.check_game_over()
#     assert game.state == "ended", "Game did not end when a winning score was reached."
#     assert game.winner == expected_winner, "Incorrect winner when game ended by score."

# @pytest.mark.middle
# @pytest.mark.start_end
# def test_player_gives_up():
#     game = Game()
#     game.start()
#     # Simulate left player giving up
#     game.player_gives_up(player="left")
#     assert game.state == "ended", "Game did not end when a player gave up."
#     assert game.winner == "right", "Wrong winner when left player gave up."

#     # Reset game and simulate right player giving up
#     game.reset()
#     game.start()
#     game.player_gives_up(player="right")
#     assert game.state == "ended", "Game did not end when a player gave up."
#     assert game.winner == "left", "Wrong winner when right player gave up."

# @pytest.mark.middle
# @pytest.mark.start_end
# def test_player_loses_connection():
#     game = Game()
#     game.start()
#     # Simulate left player losing connection
#     game.player_loses_connection(player="left")
#     assert game.state == "ended", "Game did not end when a player lost connection."
#     assert game.winner == "right", "Wrong winner when left player lost connection."

#     # Reset game and simulate right player losing connection
#     game.reset()
#     game.start()
#     game.player_loses_connection(player="right")
#     assert game.state == "ended", "Game did not end when a player lost connection."
#     assert game.winner == "left", "Wrong winner when right player lost connection."

# @pytest.mark.middle
# @pytest.mark.start_end
# def test_player_closes_tab():
#     game = Game()
#     game.start()
#     # Simulate left player closing the tab
#     game.player_closes_tab(player="left")
#     assert game.state == "ended", "Game did not end when a player closed the tab."
#     assert game.winner == "right", "Wrong winner when left player closed the tab."

#     # Reset game and simulate right player closing the tab
#     game.reset()
#     game.start()
#     game.player_closes_tab(player="right")
#     assert game.state == "ended", "Game did not end when a player closed the tab."
#     assert game.winner == "left", "Wrong winner when right player closed the tab."

# @pytest.mark.middle
# @pytest.mark.start_end
# def test_game_reset():
#     game = Game()
#     game.start()
#     game.scores = (5, 7)  # Simulate a game in progress
#     game.reset()
#     assert game.ball.position == (100, 50) and game.ball.velocity == (0, 0), "Game did not reset correctly."
#     assert game.scores == (0, 0), "Scores did not reset."
#     assert game.state == "waiting", "Game state did not reset to 'waiting'."
