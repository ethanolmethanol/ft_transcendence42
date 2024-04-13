from back_game.game_entities.ball import Ball
from back_game.game_entities.paddle import Paddle
from back_game.game_arena.map import Map
from back_game.game_settings.game_constants import *

class Arena:
   def __init__(self, playerSpecs):
      self.__fillPlayerSpecs(playerSpecs)
      self.id = id(self)
      self.status = WAITING
      self.players = []
      self.scores = []
      self.ball = Ball()
      self.paddles = [Paddle(slot) for slot in range(self.nbPlayers)]
      self.map = Map() # depends on the number of players

   def __fillPlayerSpecs(self, playerSpecs):
      self.nbPlayers = playerSpecs['nbPlayers']
      if self.nbPlayers not in range (MIN_PLAYER, MAX_PLAYER):
         raise ValueError("The number of players is out of allowed range.")
      self.mode = playerSpecs['mode']
      if self.mode not in (LOCAL_MODE, ONLINE_MODE):
         raise ValueError("The mode is invalid.")

   def isEmpty(self):
      return len(self.players) == 0
   
   def isFull(self):
      return len(self.players) >= self.maxPlayers
   
   def addPlayer(self, username):
      if (self.mode == LOCAL_MODE):
         self.players = ["Player 1", "Player 2"]
         self.scores = [0, 0]
      else:
         self.players.append(username)
         self.scores.append(0)
      if self.isFull():
         self.status = STARTED

   def removePlayer(self, username):
      if (self.mode == LOCAL_MODE):
         self.players.clear()
      else:
         self.players.remove(username)

   def endOfGame(self):
      self.status = OVER

   def getWinner(self):
      highestScore = self.scores[0]
      winner = self.players[0]
      nbPlayers = len(self.scores)
      for i in range (0, nbPlayers):
         if self.scores[i] > highestScore:
            highestScore, winner = self.scores, self.players[i]
      return winner