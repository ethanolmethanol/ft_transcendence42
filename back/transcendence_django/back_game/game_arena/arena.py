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
      self.last_kick_check = time.time()

   def to_dict(self):
      if self.players == {}:
         scores = [0 for _ in range(self.nbPlayers)]
      else:
         scores = [player.score for player in self.players.values()]
      return {
         "id": self.id,
         "status": self.status,
         "players": [player.player_name for player in self.players.values()],
         "scores": scores,
         "ball": self.ball.to_dict(),
         "paddles": [paddle.to_dict() for paddle in self.paddles.values()],
         "map": self.map.to_dict()
      }

   def is_empty(self):
      return all(player.status == GIVEN_UP for player in self.players.values())

   def is_full(self):
      return len(self.players) == self.nbPlayers

   def enter_arena(self, user_id):
      if self.did_player_give_up(user_id):
         raise ValueError("The player has given up.")
      elif not self.__is_player_in_game(user_id) and self.is_full():
         raise ValueError("The arena is full.")
      elif self.mode == LOCAL_MODE:
         self.__enter_local_mode(user_id)
      elif user_id in self.players:
         self.players[user_id].status = ENABLED
      else:
         self.__register_player(user_id, user_id)

   def disable_player(self, user_id):
      self.__change_player_status(user_id, DISABLED)

   def enable_player(self, user_id):
      self.__change_player_status(user_id, ENABLED)

   def player_gave_up(self, user_id):
      self.__change_player_status(user_id, GIVEN_UP)

   def start_game(self):
      self.__reset()
      self.status = STARTED
      logger.info(f"Game started. {self.id}")

   def conclude_game(self):
      self.status = OVER
      for player in self.players.values():
         self.disable_player(player.user_id)

   def rematch(self, user_id):
      if not self.__is_player_in_game(user_id):
         raise KeyError("This user is unknown")
      self.status = WAITING
      self.enable_player(user_id)
      if self.__are_all_players_ready():
         self.start_game()
         return self.to_dict()
      return None

   def did_player_give_up(self, user_id):
      try:
         if self.mode == LOCAL_MODE:
            return self.players and all(player.status == GIVEN_UP for player in self.players.values())
         return self.players[user_id].status == GIVEN_UP
      except KeyError:
         return False

# improve syntax
   def ball_hit_wall(self, player_slot):
      if self.mode == LOCAL_MODE:
         playername = "Player2" if player_slot else "Player1"
         logger.info(f"Point was scored for {playername}. slot: {player_slot}")
         player = self.players[playername]
         player.score += 1
         logger.info(f"Point was scored for {playername}. Their score is {player.score}")
         if player.score == MAXIMUM_SCORE:
            self.conclude_game()
         return {"score": {"playername": playername}}
      else:
         raise NotImplementedError() # TODO

   def get_winner(self):
      winner = max(self.players.values(), key=lambda player: player.score)
      return winner.player_name

   def move_paddle(self, player_name, direction):
      if (direction not in [-1, 1]):
         raise ValueError("Direction is invalid. It should be -1 or 1.")
      paddle = self.paddles[player_name]
      if paddle.status == LISTENING:
         paddle.status = PROCESSING
         player = self.players[player_name]
         player.update_activity_time()
         paddle.move(direction)
         try:
            self.ball.update_collision(paddle)
         except:
            logger.error("Paddle cannot move due to collision.")
            paddle.move(-direction)
      paddle.status = LISTENING
      return {"slot": paddle.slot, "position": paddle.position.to_dict()}

   def update_game(self):
      ball_update = self.ball.move()
      game_status = {"status": self.status}
      update_dict = {**ball_update, **game_status}
      if time.time() - self.last_kick_check >= 1:
        kicked_players = self.kick_afk_players()
        if kicked_players:
           update_dict["kicked_players"] = kicked_players
        self.last_kick_check = time.time()
      return update_dict

   def kick_afk_players(self):
      current_time = time.time()
      kicked_players = []
      for player in self.players.values():
         time_left = player.last_activity_time + AFK_TIMEOUT - current_time
         if time_left <= AFK_WARNING_THRESHOLD:
            kicked_players.append({"user_id": player.user_id, "time_left": round(time_left)})
            logger.info(f"Player {player.user_id} was kicked due to inactivity.")
         if time_left <= 0:
            self.player_gave_up(player.user_id)
      return kicked_players

   def __fill_player_specs(self, playerSpecs):
      self.nbPlayers = playerSpecs['nbPlayers']
      if self.nbPlayers not in range (MIN_PLAYER, MAX_PLAYER):
         raise ValueError("The number of players is out of allowed range.")
      self.mode = playerSpecs['mode']
      if self.mode not in (LOCAL_MODE, ONLINE_MODE):
         raise ValueError("The mode is invalid.")

   def __register_player(self, user_id, player_name):
      player = Player(user_id, player_name)
      self.players[player_name] = player
      self.paddles[player_name] = self.paddles.pop(f'{len(self.players)}')  # Update the key in the paddles dictionary
      if self.is_full():
         self.start_game()

   def __is_player_in_game(self, user_id):
      if self.mode == LOCAL_MODE:
         return self.players and any(player.user_id == user_id for player in self.players.values())
      else:
         return user_id in self.players and self.players[user_id].status != GIVEN_UP

   def __reset(self):
      for player in self.players.values():
         player.reset()
      for paddle in self.paddles.values():
         paddle.reset()
      self.ball.reset()

   def __change_player_status(self, user_id, status):
      if not self.did_player_give_up(user_id):
         if self.mode == LOCAL_MODE:
            for player in self.players.values():
               player.status = status
         else:
            self.players[user_id].status = status

   def __enter_local_mode(self, user_id):
      if self.is_empty():
         self.__register_player(user_id, "Player1")
         self.__register_player(user_id, "Player2")

   def __are_all_players_ready(self):
      return self.is_full and all(player.status == ENABLED for player in self.players.values())
