from back_game.game_entities.ball import Ball
from back_game.game_entities.paddle import Paddle
from back_game.game_arena.map import Map
from back_game.game_arena.player import *
from back_game.game_settings.game_constants import *

import logging
logger = logging.getLogger(__name__)
class Arena:
   def __init__(self, playerSpecs):
      self.__fill_player_specs(playerSpecs)
      self.id = str(id(self))
      self.status = WAITING
      self.players = {}
      self.paddles = {f'{i + 1}': Paddle(i + 1, self.nbPlayers) for i in range(self.nbPlayers)}  # Initialize paddles dictionary
      self.ball = Ball(self.paddles.values(), self.ball_hit_wall)
      self.map = Map() # depends on the number of players

   def __fill_player_specs(self, playerSpecs):
      self.nbPlayers = playerSpecs['nbPlayers']
      if self.nbPlayers not in range (MIN_PLAYER, MAX_PLAYER):
         raise ValueError("The number of players is out of allowed range.")
      self.mode = playerSpecs['mode']
      if self.mode not in (LOCAL_MODE, ONLINE_MODE):
         raise ValueError("The mode is invalid.")

   def __register_player(self, owner_name, username):
      player = Player(owner_name, username)
      self.players[username] = player
      self.paddles[username] = self.paddles.pop(f'{len(self.players)}')  # Update the key in the paddles dictionary
      if self.is_full():
         self.start_game()

   def to_dict(self):
      if self.players == {}:
         scores = [0 for _ in range(self.nbPlayers)]
      else:
         scores = [player.score for player in self.players.values()]
      return {
         "id": self.id,
         "status": self.status,
         "players": [player.username for player in self.players.values()],
         "scores": scores,
         "ball": self.ball.to_dict(),
         "paddles": [paddle.to_dict() for paddle in self.paddles.values()],
         "map": self.map.to_dict()
      }

   def is_empty(self):
      return all(player.status == GIVEN_UP for player in self.players.values())

   def is_full(self):
      return len(self.players) == self.nbPlayers and all(player.status == ENABLED for player in self.players.values())

   def enter_arena(self, owner_name):
      if self.mode == LOCAL_MODE:
         self.__enter_local_mode(owner_name)
      elif owner_name in self.players:
         self.players[owner_name].status = ENABLED
      elif self.is_full():
         raise ValueError("The arena is full.")
      else:
         self.__register_player(owner_name, owner_name)

   def __enter_local_mode(self, owner_name):
      if self.is_empty():
         self.__register_player(owner_name, "Player1")
         self.__register_player(owner_name, "Player2")

   def disable_player(self, username):
      self.__change_player_status(username, DISABLED)

   def enable_player(self, username):
      self.__change_player_status(username, ENABLED)

   def player_gave_up(self, username):
      self.__change_player_status(username, GIVEN_UP)

   def __change_player_status(self, username, status):
      if self.mode == LOCAL_MODE:
         for player in self.players.values():
            player.status = status
      else:
         self.players[username].status = status

   def start_game(self):
      self.status = STARTED
      logger.info(f"Game started. {self.id}")

   def end_of_game(self):
      self.status = OVER
      for player in self.players.values():
         self.disable_player(player.username)

   def rematch(self, username):
      if not self.__is_player_in_game(username):
         raise KeyError("This user is unknown")
      self.status = WAITING
      self.enable_player(username)
      if self.is_full():
         self.__reset()
         self.start_game()
         return self.to_dict()
      return None

   def __reset(self):
      for player in self.players.values():
         player.reset()
      for paddle in self.paddles.values():
         paddle.reset()
      self.ball.reset()

   def __is_player_in_game(self, username):
      if self.mode == LOCAL_MODE:
         return True
      else:
         return username in self.players.keys()

   def ball_hit_wall(self, which):
      if self.mode == LOCAL_MODE:
         playername = "Player2" if which else "Player1"
         player = self.players[playername]
         player.score += 1
         logger.info(f"Point was scored for {playername}. Their score is {player.score}")
         if player.score == 10:
            self.end_of_game()
         return {"score": {"username": playername}}
      else:
         raise NotImplementedError() # TODO

   def get_winner(self):
      # for player in self.players.values():
      #    logger.info(f"Username {player.username}, player.score}")
      winner = max(self.players.values(), key=lambda player: player.score)
      return winner.username

   def move_paddle(self, username, direction):
      if (direction not in [-1, 1]):
         raise ValueError("Direction is invalid. It should be -1 or 1.")
      paddle = self.paddles[username]
      paddle.move(direction)
      self.ball.update_collision(paddle)
      return {"slot": paddle.slot, "position": paddle.position.to_dict()}

   def update_game(self):
      ball_update = self.ball.move()
      game_status = {"status": self.status}
      update_dict = {**ball_update, **game_status}
      return update_dict
