from back_game.game_settings.game_constants import  GAME_WIDTH, GAME_HEIGHT, BALL_RADIUS, INITIAL_SPEEDX, INITIAL_SPEEDY, RIGHT_SLOT, LEFT_SLOT
from back_game.game_physics.position import Position
from back_game.game_physics.vector import Vector
import math

import logging
logger = logging.getLogger(__name__)

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

   def set_position(self, position):
      x = position.x
      y = position.y
      if x < self.radius or x > GAME_WIDTH - self.radius:
         raise ValueError("Ball x-coordinate is out of bounds.")
      elif y < self.radius or y > GAME_HEIGHT - self.radius:
         raise ValueError("Ball y-coordinate is out of bounds.")
      self.position.setCoordinates(x, y)

   def move(self):
      new_position = Position(
         self.position.x + self.speed.x,
         self.position.y + self.speed.y)
      self.update_position(new_position)

   def update_collision(self, paddle):
      if self.is_paddle_collision(self.position, paddle):
         self.update_position(self.position)

   def update_position(self, new_position):
      for paddle in self.paddles:
         if self.is_paddle_collision(self.position, paddle):
            # side = self.get_collision_side(new_position, paddle)
            # self.__push_ball(side, paddle)
            # new_position = self.position
            self.__push_ball(paddle)
            new_position = self.position
            collision_point = self.get_collision_point(paddle)
            self.speed = paddle.calc_speed_after_collision(collision_point)
            logger.info(f"New speed is: ({self.speed.x}, {self.speed.y})")
            self.position = new_position
            break
            # return # Exit the function after handling the collision

      # If no collision with paddles, proceed with the normal update
      self.__update_wall_collision(new_position)
      # self.set_position(new_position)

   def get_collision_point(self, paddle):
      closest_x = max(min(self.position.x, paddle.right), paddle.left)
      closest_y = max(min(self.position.y, paddle.bottom), paddle.top)
      return Position(closest_x, closest_y)

   def __push_ball(self, paddle):
      side = self.get_collision_side(self.position, paddle)
      push_position = Position(self.position.x, self.position.y)
      if side == "top":
         push_position.y = paddle.top - self.radius
      elif side == "bottom":
         push_position.y = paddle.bottom + self.radius
      elif side == "left":
         push_position.x = paddle.left - self.radius
      elif side == "right":
         push_position.x = paddle.right + self.radius
      self.set_position(push_position)
      logger.info(f"Ball collided with paddle {paddle.slot} on the {side} side.")

   def is_paddle_collision(self, position, paddle):
      """
      Checks if the ball collides with a paddle.
      """
      # Calculate the distance from the ball's center to the closest point on the paddle
      closest_x = max(min(position.x, paddle.right), paddle.left)
      closest_y = max(min(position.y, paddle.bottom), paddle.top)
      distance_x = position.x - closest_x
      distance_y = position.y - closest_y
      distance = math.sqrt(distance_x**2 + distance_y**2)

      # Check if the distance is less than or equal to the ball's radius
      return distance < self.radius

   def get_collision_side(self, position, paddle):
      """
      Determines which side of the paddle the ball collides with, accurately considering the ball's radius.
      """
      closest_x = max(min(position.x, paddle.right), paddle.left)
      closest_y = max(min(position.y, paddle.bottom), paddle.top)
      distance_x = position.x - closest_x
      distance_y = position.y - closest_y

      return self.__get_side(distance_x, distance_y, position, paddle)

   def __get_side(self, distance_x, distance_y, position, paddle):
      if abs(distance_x) > abs(distance_y):
         if distance_x > paddle.position.x - position.x:
               return "right"
         else:
               return "left"
      else:
         if distance_y > paddle.position.y - position.y:
               return "bottom"
         else:
               return "top"

   def __update_wall_collision(self, new_position):
      if new_position.x <= self.radius or new_position.x >= GAME_WIDTH - self.radius:
         self.reset()
         # self.speed.x *= -1
      elif new_position.y <= self.radius or new_position.y >= GAME_HEIGHT - self.radius:
         self.speed.y *= -1
      else:
         self.position = new_position

   def reset(self):
      self.position = Position(GAME_WIDTH / 2, GAME_HEIGHT / 2)
      self.speed = Vector(INITIAL_SPEEDX, INITIAL_SPEEDY)
