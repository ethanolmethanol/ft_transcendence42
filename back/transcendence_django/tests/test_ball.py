import pytest

from back_game.game_entities.ball import Ball
from back_game.game_settings.game_constants import *

@pytest.mark.middle
@pytest.mark.ball
def test_ball_initialization():
    ball = Ball([])
    assert isinstance(ball, Ball), "Ball instance should be created"
    assert hasattr(ball, 'position'), "Ball instance should have a 'position' attribute"
    assert hasattr(ball, 'speed'), "Ball instance should have a 'speed' attribute"
    assert ball.position.to_dict() == {'x': round(GAME_WIDTH / 2), 'y': round(GAME_HEIGHT / 2)}, "Ball position should be initialized to the default value"
    assert ball.speed.to_dict() == {'x': INITIAL_SPEEDX, 'y': INITIAL_SPEEDY}, "Ball speed should be initialized to the default value"
