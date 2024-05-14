import math
from back_game.game_physics.position import Position


class Vector(Position):

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    def unit_vector(self):
        magnitude_value = self.magnitude()
        return Vector(self.x / magnitude_value, self.y / magnitude_value)
