from back_game.game_geometry.vector import Vector


class Speed(Vector):

    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.absolute_velocity = self.magnitude()

    def update(self, new_speed: "Speed"):
        self.x = new_speed.x
        self.y = new_speed.y
        self.absolute_velocity = new_speed.absolute_velocity

    def reverse_y_direction(self):
        self.y *= -1

    def multiply_by_scalar(self, scalar: float):
        norm = self.magnitude()
        if norm == 0:
            return
        self.x = (self.x / norm) * scalar
        self.y = (self.y / norm) * scalar
        self.absolute_velocity = self.magnitude()
