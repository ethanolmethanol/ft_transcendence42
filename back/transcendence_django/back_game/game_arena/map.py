from back_game.game_settings.game_constants import GAME_HEIGHT, GAME_WIDTH


class Map:
    def __init__(self):  # TO DO Map size and shape depends on number of player
        self.width: int = GAME_WIDTH
        self.height: int = GAME_HEIGHT

    def update(self, new_width: int, new_height: int):
        self.width = new_width
        self.height = new_height

