from abc import ABC, abstractmethod
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from typing import Any, Callable
import logging
import json
import asyncio
from autobahn.wamp.exception import ApplicationError as ChannelError
from back_game.game_settings.game_constants import INVALID_CHANNEL, UNKNOWN_CHANNEL_ID
from transcendence_django.dict_keys import (
    ARENA,
    ARENA_ID,
    CHANNEL_ERROR_CODE,
    DIRECTION,
    ERROR,
    GAME_MESSAGE,
    GAME_ERROR,
    GAME_OVER,
    GAME_UPDATE,
    GIVE_UP,
    JOIN,
    LEAVE,
    MESSAGE,
    MOVE_PADDLE,
    PADDLE,
    PLAYER,
    PLAYERS,
    PLAYER_NAME,
    REMATCH,
    START_TIMER,
    TYPE,
    TIME,
    UPDATE,
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

    @abstractmethod
    def get_monitor(self):
        pass

    async def connect(self):
        self.game.channel_id = self.scope["url_route"]["kwargs"]["channel_id"]
        await self.accept()
        if self.monitor.does_exist_channel(self.game.channel_id) is False:
            await self.send_error(
                {CHANNEL_ERROR_CODE: INVALID_CHANNEL, MESSAGE: UNKNOWN_CHANNEL_ID}
            )
        else:
            await self.add_user_to_channel_group()

    async def add_user_to_channel_group(self):
        self.room_group_name = f"game_{self.game.channel_id}"
        logger.info("User Connected to %s", self.room_group_name)
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

    async def disconnect(self, close_code: int):
        try:
            await self.leave(None)
        except ChannelError:
            pass
        if self.room_group_name is not None:
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )
        logger.info("Disconnect with code: %s", close_code)

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
        except ChannelError as e:
            await self.send_error({CHANNEL_ERROR_CODE: e.code, MESSAGE: e.message})

    @abstractmethod
    async def join(self, message: dict[str, Any]):
        pass

    @abstractmethod
    async def leave(self, _):
        pass

    @abstractmethod
    async def give_up(self, _):
        pass

    @abstractmethod
    async def rematch(self, _):
        pass

    async def move_paddle(self, message: dict[str, Any]):
        player_name: str = message[PLAYER]
        direction: int = message[DIRECTION]
        paddle_data = self.game.move_paddle(player_name, direction)
        await self.send_update({PADDLE: paddle_data})

    async def send_arena_data(self):
        arena: Arena = self.monitor.get_arena(self.game.channel_id, self.game.arena_id)
        await self.send_update({ARENA: arena.to_dict()})

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
        summary = self.monitor.get_game_summary(
            self.game.channel_id, self.game.arena_id
        )
        await self.send_update(
            {
                GAME_OVER: {
                    PLAYERS: summary[PLAYERS],
                    WINNER: summary[WINNER][PLAYER_NAME] if summary[WINNER] else None,
                    TIME: time,
                    MESSAGE: "Game over. Thanks for playing!",
                }
            }
        )

    async def safe_send(self, data: dict[str, Any]):
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
        await self.safe_send({TYPE: GAME_MESSAGE, MESSAGE: message})

    async def game_error(self, event: dict[str, str]):
        error = event[ERROR]
        await self.safe_send({TYPE: GAME_ERROR, ERROR: error})

    async def game_update(self, event: dict[str, str]):
        message = event[UPDATE]
        await self.safe_send({TYPE: GAME_UPDATE, UPDATE: message})

    async def send_error(self, error: dict[str, Any]):
        logger.info("Sending error: %s: %s", error[CHANNEL_ERROR_CODE], error[MESSAGE])
        await self.safe_send({TYPE: GAME_ERROR, ERROR: error})

    async def send_update(self, update: dict[str, Any]):
        update = {**{ARENA_ID: self.game.arena_id}, **update}
        logger.info("Sending update: %s", update)
        await self.send_data({TYPE: GAME_UPDATE, UPDATE: update})

    async def send_message(self, message: str):
        logger.info("Sending message: %s", message)
        await self.send_data({TYPE: GAME_MESSAGE, MESSAGE: message})

    async def send_data(self, data: dict[str, Any]):
        try:
            await self.channel_layer.group_send(self.room_group_name, data)
        except asyncio.CancelledError:
            logger.error("WebSocket connection closed while trying to send a message.")