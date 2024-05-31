# import pytest

# from back_game.game_entities.ball import Ball
# from back_game.game_geometry.position import Position
# from back_game.game_geometry.vector import Vector
# from back_game.game_settings.game_constants import *

# @pytest.mark.passed
# @pytest.mark.ball
# def test_ball_initialization():
#     ball = Ball([])
#     assert isinstance(ball, Ball), "Ball instance should be created"
#     assert hasattr(ball, 'position'), "Ball instance should have a 'position' attribute"
#     assert hasattr(ball, 'speed'), "Ball instance should have a 'speed' attribute"
#     assert ball.position.to_dict() == {'x': round(GAME_WIDTH / 2), 'y': round(GAME_HEIGHT / 2)}, "Ball position should be initialized to the default value"
#     assert ball.speed.to_dict() == {'x': INITIAL_SPEED_X, 'y': INITIAL_SPEED_Y}, "Ball speed should be initialized to the default value"

# @pytest.mark.passed
# @pytest.mark.ball
# def test_update():
#     ball = Ball([])
#     ball.update(Position(10, 20), Vector(30, 40), BALL_RADIUS)
#     assert ball.position.to_dict() == {'x': 10, 'y': 20}
#     assert ball.speed.to_dict() == {'x': 30, 'y': 40}
#     assert ball.radius == BALL_RADIUS

# @pytest.mark.passed
# @pytest.mark.ball
# def test_to_dict():
#     ball = Ball([])
#     assert ball.to_dict() == {
#         'position': {'x': round(GAME_WIDTH / 2), 'y': round(GAME_HEIGHT / 2)},
#         'speed': {'x': INITIAL_SPEED_X, 'y': INITIAL_SPEED_Y},
#         'radius': BALL_RADIUS
#     }

# @pytest.mark.passed
# @pytest.mark.ball
# def test_set_position():
#     ball = Ball([])
#     with pytest.raises(ValueError):
#         ball.set_position(Position(-10, 20))
#     with pytest.raises(ValueError):
#         ball.set_position(Position(10, GAME_HEIGHT + 10))

# @pytest.mark.passed
# @pytest.mark.ball
# def test_move():
#     ball = Ball([])
#     initial_position = ball.position.to_dict()
#     ball.move()
#     assert ball.position.to_dict() == {
#         'x': initial_position['x'] + INITIAL_SPEED_X,
#         'y': initial_position['y'] + INITIAL_SPEED_Y
#     }
