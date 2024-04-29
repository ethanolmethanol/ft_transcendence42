from back_game.game_settings.game_constants import  GAME_WIDTH, GAME_HEIGHT, BALL_RADIUS, INITIAL_SPEEDX, INITIAL_SPEEDY, RIGHT_SLOT, LEFT_SLOT
from back_game.game_physics.position import Position
from back_game.game_physics.vector import Vector
import math

import logging
logger = logging.getLogger(__name__)

class Ball:
   def __init__(self, paddles, hit_wall_func):
      self.position = Position(GAME_WIDTH / 2, GAME_HEIGHT / 2)
      self.speed = Vector(INITIAL_SPEEDX, INITIAL_SPEEDY)
      self.radius = BALL_RADIUS
      self.paddles = paddles
      self.hit_wall = hit_wall_func

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
      update = self.update_position(new_position)
      return update if update is not None else {"ball": {"position": self.position.to_dict()}}

   def update_collision(self, paddle):
      if self.is_paddle_collision(self.position, paddle):
         self.update_position(self.position)

   def update_position(self, new_position):
      for paddle in self.paddles:
         if self.is_paddle_collision(self.position, paddle):
            self.__push_ball(paddle)
            collision_point = self.get_collision_point(paddle)
            self.speed = paddle.get_speed_after_collision(collision_point)
            logger.info(f"New speed is: ({self.speed.x}, {self.speed.y})")
            break
            # return # Exit the function after handling the collision

      # If no collision with paddles, proceed with the normal update
      score = self.__update_wall_collision(new_position)
      self.set_position(new_position)
      return score

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
      closest_x = max(min(position.x, paddle.right), paddle.left)
      closest_y = max(min(position.y, paddle.bottom), paddle.top)
      distance_x = position.x - closest_x
      distance_y = position.y - closest_y
      distance = math.sqrt(distance_x**2 + distance_y**2)

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
      if len(self.paddles) == 2:
         if new_position.y <= self.radius or new_position.y >= GAME_HEIGHT - self.radius:
            self.speed.y *= -1
         if new_position.x <= self.radius or new_position.x >= GAME_WIDTH - self.radius:
            self.speed.x *= -1
            which = new_position.x <= self.radius
            logger.info(f"Ball collided with wall {which}.")
            self.position.setCoordinates(GAME_WIDTH / 2, GAME_HEIGHT / 2)
            new_position.x = GAME_WIDTH / 2
            new_position.y = GAME_HEIGHT / 2
            return self.hit_wall(which)
         return None
      raise NotImplementedError()
         # else: # useless
         #    self.position = new_position

   def reset(self):
      self.position = Position(GAME_WIDTH / 2, GAME_HEIGHT / 2)
      self.speed = Vector(INITIAL_SPEEDX, INITIAL_SPEEDY)
