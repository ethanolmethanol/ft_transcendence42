from back_game.game_physics.position import Position

class Edges:
    def __init__(self, position: Position, width: int, height: int):
        self.update(position, width, height)

    def update(self, position: Position, width: int, height: int):
        self.bottom = position.y + height / 2
        self.top = position.y - height / 2
        self.left = position.x - width / 2
        self.right = position.x + width / 2