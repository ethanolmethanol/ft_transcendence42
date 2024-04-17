from back_game.game_settings.game_constants import  GAME_WIDTH, GAME_HEIGHT, BALL_RADIUS, INITIAL_SPEEDX, INITIAL_SPEEDY
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

   def is_paddle_collision(self, position, paddle):
      return (paddle.position.x - paddle.width / 2 - self.radius <= position.x <= paddle.position.x + paddle.width / 2 + self.radius) and \
         (paddle.position.y - paddle.height / 2 - self.radius <= position.y <= paddle.position.y + paddle.height / 2 + self.radius)

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
      if (('top' in collision_sides) or ('bottom' in collision_sides)):
         self.speed.y = -self.speed.y
      elif ('left' in collision_sides or 'right' in collision_sides):
         self.speed.x = -self.speed.x

   def __update_wall_collision(self, new_position):
      if new_position.x <= self.radius or new_position.x >= GAME_WIDTH - self.radius:
         self.speed.x *= -1
      if new_position.y <= self.radius or new_position.y >= GAME_HEIGHT - self.radius:
         self.speed.y *= -1
      else:
         self.position = new_position

   def __get_paddle_collision_side(self, position, paddle):
      sides = []
      if position.x - self.radius < paddle.position.x - paddle.width / 2:
         sides.append('left')
      if position.x + self.radius > paddle.position.x + paddle.width / 2:
         sides.append('right')
      if position.y - self.radius < paddle.position.y - paddle.height / 2:
         sides.append('top')
      if position.y + self.radius > paddle.position.y + paddle.height / 2:
         sides.append('bottom')
      return sides

   def reset(self):
      self.position = Position(GAME_WIDTH / 2, GAME_HEIGHT / 2)
      self.speed = Vector(5, 5)
