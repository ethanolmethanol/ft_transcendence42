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
      self.ball = Ball(self.paddles.values())
      self.map = Map() # depends on the number of players

   def __fill_player_specs(self, playerSpecs):
      self.nbPlayers = playerSpecs['nbPlayers']
      if self.nbPlayers not in range (MIN_PLAYER, MAX_PLAYER):
         raise ValueError("The number of players is out of allowed range.")
      self.mode = playerSpecs['mode']
      if self.mode not in (LOCAL_MODE, ONLINE_MODE):
         raise ValueError("The mode is invalid.")

   def __register_player(self, username):
      player = Player(username)
      self.players[username] = player
      self.paddles[username] = self.paddles.pop(f'{len(self.players)}')  # Update the key in the paddles dictionary
      if self.is_full():
         self.start_game()

   def to_dict(self):
      return {
         "id": self.id,
         "status": self.status,
         "players": [player.username for player in self.players.values()],
         "scores": [player.score for player in self.players.values()],
         "ball": self.ball.to_dict(),
         "paddles": [paddle.to_dict() for paddle in self.paddles.values()],
         "map": self.map.to_dict()
      }

   def is_empty(self):
      return len(self.players) == 0

   def is_full(self):
      return len(self.players) == self.nbPlayers

   def enter_arena(self, username):
      if self.mode == LOCAL_MODE:
         self.__enter_local_mode()
      elif username in self.players:
         self.players[username].status = ENABLED
      elif self.is_full():
         raise ValueError("The arena is full.")
      else:
         self.__register_player(username)

   def __enter_local_mode(self):
      if self.is_empty():
         self.__register_player("Player1")
         self.__register_player("Player2")

   def disable_player(self, username):
      if self.mode == LOCAL_MODE:
         for player in self.players.values():
            player.status = DISABLED
      else:
         self.players[username].status = DISABLED

   def start_game(self):
      self.status = STARTED
      logger.info("Game started.")

   def end_of_game(self):
      self.status = OVER

   def get_winner(self):
      winner = max(self.players, key=lambda player: player.score)
      return winner.username

   def move_paddle(self, username, direction):
      if (direction not in [-1, 1]):
         raise ValueError("Direction is invalid. It should be -1 or 1.")
      paddle = self.paddles[username]
      if paddle.status == LISTENING:
         paddle.status = PROCESSING
         paddle.move(direction)
         try:
            self.ball.update_collision(paddle)
         except:
            logger.error("Paddle cannot move due to collision.")
            paddle.move(-direction)
      paddle.status = LISTENING
      return {"slot": paddle.slot, "position": paddle.position.to_dict()}

   async def update_game(self):
      self.ball.move()
      return {"ball": {"position": self.ball.position.to_dict()}}
