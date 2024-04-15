from back_game.game_entities.ball import Ball
from back_game.game_entities.paddle import Paddle
from back_game.game_arena.map import Map
from back_game.game_arena.player import Player
from back_game.game_settings.game_constants import *

class Arena:
   def __init__(self, playerSpecs):
      self.__fillPlayerSpecs(playerSpecs)
      self.id = str(id(self))
      self.status = WAITING
      self.players = []
      self.paddles = {}
      self.ball = Ball()
      self.map = Map() # depends on the number of players

   def __fillPlayerSpecs(self, playerSpecs):
      self.nbPlayers = playerSpecs['nbPlayers']
      if self.nbPlayers not in range (MIN_PLAYER, MAX_PLAYER):
         raise ValueError("The number of players is out of allowed range.")
      self.mode = playerSpecs['mode']
      if self.mode not in (LOCAL_MODE, ONLINE_MODE):
         raise ValueError("The mode is invalid.")

   def __register_player(self, username):
      player = Player(username)
      self.players.append(player)
      self.paddles[username] = Paddle(len(self.players), self.nbPlayers)
      if self.isFull():
         self.status = STARTED

   def toDict(self):
      return {
         "id": self.id,
         "status": self.status,
         "players": [player.username for player in self.players],
         "scores": [player.score for player in self.players],
         "ball": self.ball.toDict(),
         "paddles": [paddle.toDict() for paddle in self.paddles.values()],
         "map": self.map.toDict()
      }

   def isEmpty(self):
      return len(self.players) == 0

   def isFull(self):
      return len(self.players) >= self.nbPlayers

   def enter_arena(self, username):
      if (self.mode == LOCAL_MODE):
         self.__register_player("Player1")
         self.__register_player("Player2")
      else:
         self.__register_player(username)

   def removePlayer(self, username):
      if (self.mode == LOCAL_MODE):
         self.players.clear()
         self.paddles.clear()
      else:
         self.players.remove(username)
         self.paddles.pop(username)

   def endOfGame(self):
      self.status = OVER

   def get_winner(self):
      winner = max(self.players, key=lambda player: player.score)
      return winner.username

   def move_paddle(self, username, rate):
      paddle = self.paddles[username]
      paddle.move(rate)
      return paddle.toDict()
