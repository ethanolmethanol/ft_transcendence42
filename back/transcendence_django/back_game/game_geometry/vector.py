import math

from back_game.game_geometry.position import Position


class Vector(Position):

    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y

    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def unit_vector(self) -> "Vector":
        magnitude_value = self.magnitude()
        return Vector(self.x / magnitude_value, self.y / magnitude_value)
