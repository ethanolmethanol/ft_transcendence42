from game.game_settings.game_constants import *

class Ball:
    def __init__(self, position=BALL_INITIAL_POSITION, velocity=BALL_INITIAL_VELOCITY):
        self._position = position
        self._velocity = velocity
    
    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, value):
        raise ValueError("Use update_position() to set position")
    
    @property
    def velocity(self):
        return self._velocity
    
    @velocity.setter
    def velocity(self, value):
        raise ValueError("Use update_velocity() to set velocity")
    
    def update_position(self, new_position):
        if 0 <= new_position['x'] <= GAME_WIDTH and 0 <= new_position['y'] <= GAME_HEIGHT:
            self._position = new_position
        else:
            raise ValueError("New position is out of bounds")
    
    def update_velocity(self, new_velocity):
        if (self.MIN_VELOCITY <= new_velocity['x'] <= self.MAX_VELOCITY and
                self.MIN_VELOCITY <= new_velocity['y'] <= self.MAX_VELOCITY):
            self._velocity = new_velocity
        else:
            raise ValueError("Velocity exceeds allowed range")

    def reset_ball():
        raise ValueError("reset_ball not implemented")
