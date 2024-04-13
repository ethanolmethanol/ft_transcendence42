import copy as cp
from back_game.game_entities.ball import Ball
from back_game.game_entities.paddle import Paddle
from back_game.game_arena.map import Map
from back_game.game_arena.playerMode import PlayerMode
from back_game.game_settings.game_constants import *

class Arena:
   def __init__(self, gameConfig):
      self.id = id(self)
      self.status = WAITING
      self.players = []
      self.maxPlayers = gameConfig['playerMode'].to_dict()['nbPlayers']
      self.mode = gameConfig['playerMode'].to_dict()['mode']   
      self.__initPaddles(self.maxPlayers, gameConfig['paddle'])
      self.__initBall(gameConfig['ball'])
      self.__initMap(gameConfig['map'])
      self.__initPlayerMode(gameConfig['playerMode'])

   def __initPaddles(self, nbPlayers, paddleTemplate):
      self.paddles = []
      for slot in range(nbPlayers):
         paddle = cp.deepcopy(paddleTemplate)
         paddle.slot = slot
         self.paddles.append(paddle)

   def __initBall(self, ballTemplate):
      self.ball = cp.deepcopy(ballTemplate)

   def __initMap(self, mapTemplate):
      self.map = cp.deepcopy(mapTemplate)

   def __initPlayerMode(self, playerModeTemplate):
      self.playerMode = cp.deepcopy(playerModeTemplate)

   def addPlayer(self, username):
      if (self.mode == LOCAL_MODE):
         self.players = ["Player 1", "Player 2"]
      else:
         self.players.append(username)
      if self.isFull():
         self.status = STARTED

   def isFull(self):
      return len(self.players) >= self.maxPlayers

   def isEmpty(self):
      return len(self.players) == 0

   def removePlayer(self, username):
      if (self.mode == LOCAL_MODE):
         self.players.clear()
      else:
         self.players.remove(username)

   def endOfGame(self):
      self.players.clear() # needed ??
      self.status = OVER