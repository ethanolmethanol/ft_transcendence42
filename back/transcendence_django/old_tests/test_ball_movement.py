# import pytest
# from game.game_logic.game_logic import *

# from game.game_entities.ball import Ball


# @pytest.mark.middle
# @pytest.mark.ball
# def test_ball_initialization(game_config):
#     ball = Ball()
#     assert isinstance(ball, Ball), "Ball instance should be created"
#     assert hasattr(ball, 'position'), "Ball instance should have a 'position' attribute"
#     assert hasattr(ball, 'velocity'), "Ball instance should have a 'velocity' attribute"
#     assert ball.position == game_config['BALL_INITIAL_POSITION'], "Ball position should be initialized to the default value"
#     assert ball.velocity == game_config['BALL_INITIAL_VELOCITY'], "Ball velocity should be initialized to the default value"


# @pytest.mark.middle
# @pytest.mark.ball
# @pytest.mark.parametrize("initial_position, initial_velocity, expected_position", [
#     ({'x': 50, 'y': 95}, {'x': 5, 'y': 5}, {'x': 55, 'y': 100}),
#     ({'x': 50, 'y': 5}, {'x': 5, 'y': -5}, {'x': 55, 'y': 0}),
# ])
# def test_ball_movement(initial_position, initial_velocity, expected_position):
#     ball = Ball(position=initial_position, velocity=initial_velocity)
#     ball.move()
#     assert ball.position == expected_position  # Expected position after one move


# @pytest.mark.middle
# @pytest.mark.ball
# @pytest.mark.parametrize("initial_position, initial_velocity, expected_velocity", [
#     ({'x': 50, 'y': 96}, {'x': 5, 'y': 5}, {'x': 5, 'y': -5}),
#     ({'x': 50, 'y': 3}, {'x': 5, 'y': -5}, {'x': 5, 'y': 5}),
# ])
# def test_ball_bounce_top_bottom_edges(initial_position, initial_velocity, expected_velocity):
#     ball = Ball(position=initial_position, velocity=initial_velocity)
#     ball.check_collision_with_edges()  # Check for collisions and update the velocity
#     assert ball.velocity == expected_velocity

# # @pytest.mark.middle
# # @pytest.mark.ball
# # @pytest.mark.parametrize("position_after_score", [
# #     {'x': -5, 'y': 50},  # Ball goes past left edge
# #     {'x': 105, 'y': 50},  # Ball goes past right edge
# # ])
# # def test_ball_reset_after_scoring(position_after_score):
# #     ball = Ball(position=position_after_score)
# #     ball.reset()
# #     assert ball.position == {'x': 50, 'y': 50}  # Reset position to center
# #     assert ball.velocity == {'x': 5, 'y': 5} or ball.velocity == {'x': -5,
# #                                                                   'y': 5}  # Reset to initial velocity or some other predefined velocity
