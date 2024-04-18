from back_game.game_physics.position import Position
import math

class Vector(Position):

   def __init__(self, x=0, y=0):
      super().__init__(x, y)

   def magnitude(vector):
    return math.sqrt(vector.x**2 + vector.y**2)
