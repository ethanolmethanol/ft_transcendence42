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
      return len(self.players) == 0 or not any(player.status != LEFT for player in self.players)

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
      self.__change_player_status(username, DISABLED)

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
      logger.info("Game started.")

   def end_of_game(self):
      self.status = OVER

   def rematch(self, username):
      if username not in self.players:
         raise KeyError("This user is unknown")
      if self.status == OVER:
         self.status = WAITING
         for player in self.players:
            player.score = 0
            # status should be already set to DISABLED at this step
      self.players[username].status = ENABLED
      if self.is_full():
         self.start_game()

   def ball_hit_wall(self, which):
      logger.info(f"hello")

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
      logger.info(f"Out of {len(self.players)} players, the winner?")
      for player in self.players.values():
         logger.info(f"Username {player.username}, score {player.score}")
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
      return self.ball.move()
