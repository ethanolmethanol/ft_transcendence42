from back_game.game_settings.game_constants import INITIAL_SPEED_MAGNITUDE
import math
from back_game.game_physics.vector import Vector

class speedVectorCalculator:
    
    @staticmethod
    def calculate_speed_after_paddle_collision(paddle, collision_point, unexposed_paddle_point):
        radius = paddle.height / 2
        center = unexposed_paddle_point
        norm_speed_vector = radius - math.sqrt((collision_point.x - center.x)**2 + (collision_point.y - center.y)**2)
        speed_x_component = (norm_speed_vector * paddle.width) / (radius - paddle.width)
        speed_y_component = math.sqrt(norm_speed_vector - speed_x_component**2)
        speed_x = speed_x_component * INITIAL_SPEED_MAGNITUDE / norm_speed_vector
        speed_y = speed_y_component * INITIAL_SPEED_MAGNITUDE / norm_speed_vector
        return Vector(speed_x, speed_y)
