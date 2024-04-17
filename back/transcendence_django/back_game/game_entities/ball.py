#from game.game_settings.game_constants import *

from back_game.game_settings.game_constants import  GAME_WIDTH, GAME_HEIGHT, BALL_RADIUS, INITIAL_SPEEDX, INITIAL_SPEEDY


# class Ball:
#     def __init__(self, position=BALL_INITIAL_POSITION, velocity=BALL_INITIAL_VELOCITY):
#         self.MAX_VELOCITY = None
#         self.MIN_VELOCITY = None
#         self._position = position
#         self._velocity = velocity

#     @property
#     def position(self):
#         return self._position

#     @position.setter
#     def position(self, value):
#         raise ValueError("Use update_position() to set position")


#     @property
#     def velocity(self):
#         return self._velocity

#     @velocity.setter
#     def velocity(self, value):
#         raise ValueError("Use update_velocity() to set velocity")

#     def update_position(self, new_position):

#     def update_velocity(self, new_velocity):
#         if (self.MIN_VELOCITY <= new_velocity['x'] <= self.MAX_VELOCITY and
#                 self.MIN_VELOCITY <= new_velocity['y'] <= self.MAX_VELOCITY):
#             self._velocity = new_velocity
#         else:
#             raise ValueError("Velocity exceeds allowed range")

#     # def reset_ball():
#     #     raise ValueError("reset_ball not implemented")

#     def check_collision_with_edges(self):
#         # Check collision with top and bottom edges
#         if not (0 <= self._position['y'] + self._velocity['y'] - BALL_RADIUS
#                 and self.position['y'] + self._velocity['y'] + BALL_RADIUS <= GAME_HEIGHT):
#             self._velocity['y'] *= -1  # Reverse the y-velocity
#             print(f"Y velocity changed!")

#         # Check collision with left and right edges
#         if not (0 <= self._position['x'] + self._velocity['x'] - BALL_RADIUS
#                 and self.position['x'] + self._velocity['x'] + BALL_RADIUS <= GAME_WIDTH):
#             self._velocity['x'] *= -1  # Reverse the x-velocity
#             print(f"X velocity changed!")
#         print(f"After collision checks: position = {self._position}, velocity = {self._velocity}")

from back_game.game_physics.position import Position
from back_game.game_physics.vector import Vector

class Ball:
   def __init__(self, paddles):
      self.position = Position(GAME_WIDTH / 2, GAME_HEIGHT / 2)
      self.speed = Vector(INITIAL_SPEEDX, INITIAL_SPEEDY)
      self.radius = BALL_RADIUS
      self.paddles = paddles
      self.hasCollided = {paddle.slot : False for paddle in paddles}

   def update(self, newPosition, newSpeed, newRadius):
      self.position.setCoordinates(newPosition.x, newPosition.y)
      self.speed.setCoordinates(newSpeed.x, newSpeed.y)
      self.radius = newRadius

   def to_dict(self):
      return {
         'position': self.position.to_dict(),
         'speed': self.speed.to_dict(),
         'radius': self.radius
      }

   def move(self):
      new_position = Position(
         self.position.x + self.speed.x,
         self.position.y + self.speed.y)
      self.update_position(new_position)

   def update_collision(self, paddle):
      if self.is_paddle_collision(self.position, paddle):
         self.move()

   def update_position(self, new_position):
      self.__update_paddle_collision(new_position, self.paddles)
      self.__update_wall_collision(new_position)

   def is_paddle_collision(self, new_position, paddle):
      return (paddle.position.x - paddle.width / 2 - self.radius <= new_position.x <= paddle.position.x + paddle.width / 2 + self.radius) and \
         (paddle.position.y - paddle.height / 2 - self.radius <= new_position.y <= paddle.position.y + paddle.height / 2 + self.radius)

   def __update_paddle_collision(self, new_position, paddles):
      for paddle in paddles:
         collide_position = None
         if self.is_paddle_collision(self.position, paddle):
            collide_position = self.position
         elif self.is_paddle_collision(new_position, paddle):
            collide_position = new_position
         if collide_position is not None:
            if not self.hasCollided[paddle.slot]:
               self.__set_speed_collision(collide_position, paddle)
               self.hasCollided[paddle.slot] = True
               break
         else:
            self.hasCollided[paddle.slot] = False

   def __set_speed_collision(self, collide_position, paddle):
      collision_sides = self.__get_paddle_collision_side(collide_position, paddle)
      if ('top' in collision_sides or 'bottom' in collision_sides):
         # coeff = abs(collide_position.y - paddle.position.y)
         # sign = self.speed.y / abs(self.speed.y)
         # self.speed.y = -sign * INITIAL_SPEEDY * (1 + coeff) * 0.1
         self.speed.y = -self.speed.y
      elif ('left' in collision_sides or 'right' in collision_sides):
         # coeff = abs(collide_position.x - paddle.position.x)
         # sign = self.speed.x / abs(self.speed.x)
         # self.speed.x = -sign * INITIAL_SPEEDX * (1 + coeff) * 0.1
         self.speed.x = -self.speed.x

   def __update_wall_collision(self, new_position):
      if new_position.x <= self.radius or new_position.x >= GAME_WIDTH - self.radius:
         self.speed.x *= -1
      if new_position.y <= self.radius or new_position.y >= GAME_HEIGHT - self.radius:
         self.speed.y *= -1
      else:
         self.position = new_position

   def __get_paddle_collision_side(self, new_position, paddle):
      sides = []
      if new_position.x < paddle.position.x - paddle.width / 2:
         sides.append('left')
      if new_position.x > paddle.position.x + paddle.width / 2:
         sides.append('right')
      if new_position.y < paddle.position.y - paddle.height / 2:
         sides.append('top')
      if new_position.y > paddle.position.y + paddle.height / 2:
         sides.append('bottom')
      return sides

   def reset(self):
      self.position = Position(GAME_WIDTH / 2, GAME_HEIGHT / 2)
      self.speed = Vector(5, 5)
