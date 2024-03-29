from game.game_settings.game_constants import *

class Paddle:
    def __init__(self, player_slot):
        self.player_slot = player_slot
        self._position = self.calculate_initial_position()

    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, value):
        raise AttributeError("Use update_position() to set position")
    
    def calculate_initial_position(self):
        if self.player_slot == LEFT:
            x = PADDLE_WIDTH
            y = (GAME_HEIGHT - PADDLE_HEIGHT) / 2
        elif self.player_slot == RIGHT:
            x = GAME_WIDTH - PADDLE_WIDTH * 2
            y = (GAME_HEIGHT - PADDLE_HEIGHT) / 2
        else:
            raise ValueError("Invalid player slot. Must be LEFT or RIGHT.")
        return {'x': x, 'y': y}
    
    def update_position_with_delta(self, delta_y):
        new_y = self._position['y'] + delta_y
        new_y = max(0, min(GAME_HEIGHT - PADDLE_HEIGHT, new_y))
        self._position['y'] = new_y
