import copy as cp
from back_game.game_entities.ball import Ball
from back_game.game_entities.paddle import Paddle
from back_game.game_arena.map import Map
from back_game.game_arena.playerMode import PlayerMode

class Arena:
   def __init__(self, gameConfig):
      self.id = id(self)
      self.__initPaddles(gameConfig['playerMode'].to_dict()['nbPlayers'], gameConfig['paddle'])
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
