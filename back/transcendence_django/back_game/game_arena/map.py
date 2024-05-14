from back_game.game_settings.game_constants import GAME_HEIGHT, GAME_WIDTH


class Map:
    def __init__(self):  # TO DO Map size and shape depends on number of player
        self.width = GAME_WIDTH
        self.height = GAME_HEIGHT

    def update(self, new_width, new_height):
        self.width = new_width
        self.height = new_height

    def to_dict(self):
        return {"width": self.width, "height": self.height}
