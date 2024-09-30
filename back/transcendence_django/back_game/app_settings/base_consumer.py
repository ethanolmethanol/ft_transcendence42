import asyncio
import json
import logging
from abc import ABC, abstractmethod
from typing import Any, Callable, Coroutine, Optional

import autobahn
from back_game.app_settings.lobby_error import LobbyError
from back_game.game_arena.arena import Arena
from back_game.game_settings.game_constants import INVALID_LOBBY, UNKNOWN_LOBBY_ID
from back_game.monitor.monitor import get_monitor
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from requests.exceptions import ConnectionError
from transcendence_django.dict_keys import (
    ARENA,
    ARENA_ID,
    CAPACITY,
    DIRECTION,
    ERROR,
    GAME_ERROR,
    GAME_MESSAGE,
    GAME_OVER,
    GAME_UPDATE,
    GIVE_UP,
    JOIN,
    LEAVE,
    LOBBY_ERROR_CODE,
    LOBBY_PLAYERS,
    MESSAGE,
    MOVE_PADDLE,
    OVER_CALLBACK,
    PADDLE,
    PLAYER,
    PLAYER_NAME,
    PLAYERS,
    REMATCH,
    START_TIMER,
    START_TIMER_CALLBACK,
    TIME,
    TYPE,
    UPDATE,
    UPDATE_CALLBACK,
    USER_ID,
    WINNER,
)

logger = logging.getLogger(__name__)


class BaseConsumer(AsyncJsonWebsocketConsumer, ABC):

    def __init__(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]):
        super().__init__(*args, **kwargs)
        self.room_group_name: str | None = None
        self.game = self.get_game_logic_interface()
        self.monitor = self.get_monitor()

    @abstractmethod
    def get_game_logic_interface(self):
        pass

    def get_monitor(self):
        return get_monitor()

    async def connect(self):
        logger.info("WebSocket connecting: %s", self.scope["path"])
        try:
            await self.accept()
            self.game.init_lobby(self.scope["url_route"]["kwargs"]["lobby_id"])
        except LobbyError as e:
            await self.send_error({LOBBY_ERROR_CODE: e.code, MESSAGE: e.message})
            await self.close()
            return
        if self.game.lobby is None:
            await self.send_error(
                {LOBBY_ERROR_CODE: INVALID_LOBBY, MESSAGE: UNKNOWN_LOBBY_ID}
            )
        else:
            await self.add_user_to_channel_group()
        logger.info("WebSocket connected: %s", self.scope["path"])

    async def disconnect(self, close_code: int):
        try:
            await self.leave(None)
        except LobbyError:
            pass
        if self.room_group_name is not None:
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )
        logger.info("Disconnect with code: %s", close_code)
        logger.info("WebSocket disconnected: %s", self.scope["path"])

    async def receive(self, text_data: str):
        content = json.loads(text_data)
        message_type, message = content[TYPE], content[MESSAGE]
        message_binding: dict[
            str, Callable[[dict[str, Any]], Coroutine[Any, Any, Any]]
        ] = {
            MOVE_PADDLE: self.move_paddle,
            JOIN: self.join,
            LEAVE: self.leave,
            GIVE_UP: self.give_up,
            REMATCH: self.rematch,
        }
        try:
            await message_binding[message_type](message)
        except LobbyError as e:
            await self.send_error({LOBBY_ERROR_CODE: e.code, MESSAGE: e.message})

    async def join(self, message: dict[str, Any]):
        user_id = message[USER_ID]
        player_name = message[PLAYER]
        arena_id: str = message[ARENA_ID]
        callbacks: dict[str, Optional[Callable[[Any], Coroutine[Any, Any, None]]]] = {
            UPDATE_CALLBACK: self.send_update,
            OVER_CALLBACK: self.send_game_over,
            START_TIMER_CALLBACK: self.send_start_timer,
        }
        logger.info(
            "Joining game with user_id: %s, player_name: %s, arena_id: %s",
            user_id,
            player_name,
            arena_id,
        )
        await self.game.join(user_id, player_name, arena_id, callbacks)
        await self.send_message(f"{self.game.user_id} has joined the game.")
        await self.send_players()
        await self.send_arena_data()

    async def leave(self, _):
        self.game.leave()
        await self.send_players()
        await self.send_message(f"{self.game.user_id} has left the game.")

    async def give_up(self, _):
        self.game.give_up()
        await self.send_message(f"{self.game.user_id} has given up.")
        await self.send_update({GIVE_UP: self.game.user_id})
        await self.send_players()
        await self.send_arena_data()

    async def rematch(self, _):
        self.game.rematch()
        await self.send_message(f"{self.game.user_id} asked for a rematch.")
        await self.send_arena_data()

    async def move_paddle(self, message: dict[str, Any]):
        player_name: str = message[PLAYER]
        direction: int = message[DIRECTION]
        paddle_data = self.game.move_paddle(player_name, direction)
        await self.send_update({PADDLE: paddle_data})

    async def send_arena_data(self):
        if self.game.arena_id is None:
            return
        try:
            arena: Arena = self.monitor.get_arena(
                self.game.lobby.id, self.game.arena_id
            )
            await self.send_update({ARENA: arena.to_dict()})
        except KeyError:
            pass  # Arena not found

    async def send_start_timer(self, time: float):
        logger.info("Game will begin in %s seconds...", time)
        await self.send_update(
            {
                START_TIMER: {
                    TIME: time,
                    MESSAGE: "Game will begin in ",
                }
            }
        )

    async def send_game_over(self, time: float):
        try:
            summary = self.monitor.get_game_summary(
                self.game.lobby.id, self.game.arena_id
            )
            await self.send_update(
                {
                    GAME_OVER: {
                        PLAYERS: summary[PLAYERS],
                        WINNER: (
                            summary[WINNER][PLAYER_NAME] if summary[WINNER] else None
                        ),
                        TIME: time,
                        MESSAGE: "Game over. Thanks for playing!",
                    }
                }
            )
        except KeyError:
            pass  # Arena not found

    async def send_players(self):
        players = self.monitor.get_users_from_lobby(self.game.lobby.id)
        await self.send_update(
            {
                LOBBY_PLAYERS: {
                    USER_ID: players,
                    CAPACITY: self.game.lobby.user_count,
                }
            }
        )

    async def add_user_to_channel_group(self):
        logger.info("Adding user to lobby group (Tournament)")
        self.room_group_name = f"game_{self.game.lobby.id}"
        logger.info("User Connected to %s", self.room_group_name)
        try:
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        except ConnectionError as e:
            logger.error("Connection error: %s", e)

    async def __safe_send(self, data: dict[str, Any]):
        try:
            await self.send(text_data=json.dumps(data))
        except ValueError as e:
            logger.error("Serialization value error: %s", e)
        except TypeError as e:
            logger.error("Serialization type error: %s", e)
        except ConnectionResetError as e:
            logger.error("Connection reset error: %s", e)
        except autobahn.exception.Disconnected as e:
            logger.error("Connection closed error: %s", e)

    async def game_message(self, event: dict[str, str]):
        message = event[MESSAGE]
        await self.__safe_send({TYPE: GAME_MESSAGE, MESSAGE: message})

    async def game_error(self, event: dict[str, str]):
        error = event[ERROR]
        await self.__safe_send({TYPE: GAME_ERROR, ERROR: error})

    async def game_update(self, event: dict[str, str]):
        message = event[UPDATE]
        await self.__safe_send({TYPE: GAME_UPDATE, UPDATE: message})

    async def send_error(self, error: dict[str, Any]):
        logger.info("Sending error: %s: %s", error[LOBBY_ERROR_CODE], error[MESSAGE])
        await self.__safe_send({TYPE: GAME_ERROR, ERROR: error})

    async def send_update(self, update: dict[str, Any]):
        update = {**{ARENA_ID: self.game.arena_id}, **update}
        # logger.info("Sending update: %s", update)
        await self.send_data({TYPE: GAME_UPDATE, UPDATE: update})

    async def send_message(self, message: str):
        logger.info("Sending message: %s", message)
        await self.send_data({TYPE: GAME_MESSAGE, MESSAGE: message})

    async def send_data(self, data: dict[str, Any]):
        try:
            await self.channel_layer.group_send(self.room_group_name, data)
        except asyncio.CancelledError:
            logger.error("WebSocket connection closed while trying to send a message.")
