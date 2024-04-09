from game.game_settings.game_constants import *

from game.game_settings.game_constants import BALL_INITIAL_POSITION, BALL_INITIAL_VELOCITY, GAME_WIDTH, \
    GAME_HEIGHT, BALL_RADIUS


class Ball:
    def __init__(self, position=BALL_INITIAL_POSITION, velocity=BALL_INITIAL_VELOCITY):
        self.MAX_VELOCITY = None
        self.MIN_VELOCITY = None
        self._position = position
        self._velocity = velocity

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        raise ValueError("Use update_position() to set position")

    def move(self):
        new_position = {
            'x': self._position['x'] + self._velocity['x'],
            'y': self._position['y'] + self._velocity['y']
        }
        self.update_position(new_position)

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

    # def reset_ball():
    #     raise ValueError("reset_ball not implemented")

    def check_collision_with_edges(self):
        # Check collision with top and bottom edges
        if not (0 <= self._position['y'] + self._velocity['y'] - BALL_RADIUS
                and self.position['y'] + self._velocity['y'] + BALL_RADIUS <= GAME_HEIGHT):
            self._velocity['y'] *= -1  # Reverse the y-velocity
            print(f"Y velocity changed!")

        # Check collision with left and right edges
        if not (0 <= self._position['x'] + self._velocity['x'] - BALL_RADIUS
                and self.position['x'] + self._velocity['x'] + BALL_RADIUS <= GAME_WIDTH):
            self._velocity['x'] *= -1  # Reverse the x-velocity
            print(f"X velocity changed!")
        print(f"After collision checks: position = {self._position}, velocity = {self._velocity}")