# import pytest
# import json
# from django.contrib.auth.models import User
# from rest_framework.test import APIClient
# from game.models import Game, Player

# @pytest.mark.soft
# @pytest.mark.scoring
# @pytest.mark.parametrize("ball_position, expected_scores", [
#     ((-10, 50), (1, 0)),  # Ball passes left paddle
#     ((210, 50), (0, 1)),  # Ball passes right paddle, assuming game width is 200
# ])
# def test_score_increment(ball_position, expected_scores):
#     game = Game()
#     ball = Ball(position=ball_position)
#     game.check_score(ball)
#     assert game.scores == expected_scores, "Scores did not update correctly after the ball passed a paddle."

# @pytest.mark.middle
# @pytest.mark.scoring
# def test_ball_reset_after_scoring():
#     game = Game()
#     ball = Ball(position=(210, 50))  # Ball beyond the right boundary, indicating a score
#     game.reset_ball_after_score(ball)
#     assert ball.position == (100, 50), "Ball did not

# @pytest.mark.middle
# @pytest.mark.scoring
# @pytest.mark.parametrize("scores, expected_game_over", [
#     ((0, 10), True),  # Right player wins
#     ((10, 0), True),  # Left player wins
#     ((5, 3), False),  # Game still ongoing
# ])
# def test_game_over_condition(scores, expected_game_over):
#     game = Game()
#     game.scores = scores
#     assert game.check_game_over() == expected_game_over, "Game over
