import logging
from typing import Any, Callable, Coroutine, Optional

from back_game.game_arena.game import Game, GameStatus
from back_game.game_arena.player import ENABLED, Player, PlayerStatus
from back_game.game_arena.player_manager import PlayerManager
from back_game.game_settings.dict_keys import (
    ARENA,
    BALL,
    COLLIDED_SLOT,
    ID,
    KICKED_PLAYERS,
    MAP,
    MODE,
    NB_PLAYERS,
    PADDLES,
    PLAYER1,
    PLAYER2,
    PLAYER_NAME,
    PLAYER_SPECS,
    PLAYERS,
    SCORE,
    SCORES,
    STATUS,
)
from back_game.game_settings.game_constants import MAXIMUM_SCORE, CREATED, STARTED, WAITING

logger = logging.getLogger(__name__)


class Arena:

    def __init__(self, players_specs: dict[str, int]):
        self.id: str = str(id(self))
        self.player_manager: PlayerManager = PlayerManager(players_specs)
        self.game: Game = Game(self.player_manager.nb_players)
        self.game_update_callback: Optional[
            Callable[[dict[str, Any]], Coroutine[Any, Any, None]]
        ] = None
        self.game_over_callback: Optional[
            Callable[[str, float], Coroutine[Any, Any, None]]
        ] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            ID: self.id,
            STATUS: self.game.status,
            PLAYERS: [
                player.player_name for player in self.player_manager.players.values() if player.status == PlayerStatus(ENABLED)
            ],
            SCORES: self.player_manager.get_scores(),
            BALL: self.game.ball.to_dict(),
            PADDLES: [paddle.to_dict() for paddle in self.game.paddles.values()],
            MAP: self.game.map.__dict__,
            PLAYER_SPECS: {NB_PLAYERS: self.player_manager.nb_players, MODE: self.player_manager.is_remote},
        }

    def is_remote(self) -> bool:
        return self.player_manager.is_remote

    def is_empty(self) -> bool:
        return self.player_manager.is_empty()

    def is_full(self) -> bool:
        return self.player_manager.is_full()

    def is_user_active_in_game(self, user_id: int) -> bool:
        if self.game.status == GameStatus(WAITING):
            return False
        return any(
            player.user_id == user_id
            and player.status == PlayerStatus(ENABLED)
            for player in self.player_manager.players.values()
        )

    def get_winner(self) -> str:
        return self.player_manager.get_winner()

    def get_players(self) -> dict[str, Player]:
        return self.player_manager.players

    def get_status(self) -> GameStatus:
        return self.game.status

    async def enter_arena(self, user_id: int, player_name: str) -> None:
        self.player_manager.allow_player_enter_arena(user_id)
        if self.get_status() == GameStatus(CREATED):
            self.game.set_status(WAITING)
        if self.get_status() != GameStatus(WAITING):
            return
        logger.info("Player %s entered the arena %s", user_id, self.id)
        if self.player_manager.is_remote:
            await self.__enter_remote_mode(user_id, player_name)
        else:
            await self.__enter_local_mode(user_id)

    async def start_game(self):
        self.__reset()
        self.game.start()
        await self.game_update_callback({ARENA: self.to_dict()})
        logger.info("Game started. %s", self.id)

    def conclude_game(self):
        self.player_manager.finish_active_players()
        self.game.conclude()
        logger.info("Game is over. %s", self.id)

    async def rematch(self, user_id: int):
        self.player_manager.finish_given_up_players()
        self.player_manager.rematch(user_id)
        self.game.set_status(WAITING)
        if self.player_manager.are_all_players_ready():
            await self.start_game()

    def player_leave(self, user_id: int):
        if self.game.status == GameStatus(WAITING):
            player_name = self.player_manager.get_player_name(user_id)
            self.player_manager.remove_player(player_name)
            self.game.remove_paddle(player_name)
        else:
            self.disable_player(user_id)

    def disable_player(self, user_id: int):
        self.player_manager.disable_player(user_id)

    def player_gave_up(self, user_id: int):
        self.player_manager.player_gave_up(user_id)

    def move_paddle(self, player_name: str, direction: int) -> dict[str, Any]:
        if self.game.status != GameStatus(STARTED):
            return {}
        paddle_dict: dict[str, Any] = self.game.move_paddle(player_name, direction)
        self.player_manager.update_activity_time(player_name)
        return paddle_dict

    def update_game(self) -> dict[str, Any]:
        update_dict: dict[str, Any] = self.game.update()
        collided_slot: int | None = update_dict.get(COLLIDED_SLOT)
        if collided_slot is not None:
            update_dict[SCORE] = self.__update_scores(collided_slot)
        kicked_players = self.player_manager.kick_afk_players()
        if kicked_players:
            update_dict[KICKED_PLAYERS] = kicked_players
        return update_dict

    def set_status(self, status: GameStatus):
        self.game.set_status(status)

    def has_enough_players(self) -> bool:
        logger.info("Checking if there are enough players in the arena %s", self.id)
        return self.player_manager.has_enough_players()

    def did_player_give_up(self, user_id: int) -> bool:
        return self.player_manager.did_player_give_up(user_id)

    def __update_scores(self, player_slot: int) -> dict[str, str]:
        player_name = self.__get_player_name_by_paddle_slot(player_slot)
        logger.info("Point was scored for %s. slot: %s", player_name, player_slot)
        player = self.player_manager.players[player_name]
        player.score += 1
        logger.info(
            "Point was scored for %s. Their score is %s", player_name, player.score
        )
        if player.score == MAXIMUM_SCORE:
            self.conclude_game()
        return {PLAYER_NAME: player_name}

    def __get_player_name_by_paddle_slot(self, paddle_slot: int) -> str | None:
        for paddle in self.game.paddles.values():
            if paddle.slot == paddle_slot:
                return paddle.player_name
        return None

    def __reset(self):
        self.player_manager.reset()
        self.game.reset()

    async def __enter_local_mode(self, user_id: int):
        if not self.is_full():
            await self.__register_player(user_id, PLAYER1)
            await self.__register_player(user_id, PLAYER2)

    async def __enter_remote_mode(self, user_id: int, player_name: str):
        if self.player_manager.is_player_in_game(user_id):
            self.player_manager.change_player_status(user_id, PlayerStatus(ENABLED))
        else:
            await self.__register_player(user_id, player_name)

    async def __register_player(self, user_id: int, player_name: str):
        self.player_manager.add_player(user_id, player_name)
        self.game.add_paddle(player_name)
        if self.is_full():
            await self.start_game()
