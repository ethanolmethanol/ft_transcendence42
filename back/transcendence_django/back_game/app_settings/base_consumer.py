from abc import ABC, abstractmethod
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from typing import Any, Callable
import logging
import json
import asyncio
import autobahn


from back_game.app_settings.channel_error import ChannelError
from back_game.game_settings.game_constants import INVALID_CHANNEL, UNKNOWN_CHANNEL_ID
from back_game.monitor.monitor import get_monitor
from transcendence_django.dict_keys import (
    ARENA,
    ARENA_ID,
    ASSIGNATIONS,
    CAPACITY,
    CHANNEL_ERROR_CODE,
    CHANNEL_PLAYERS,
    DIRECTION,
    ERROR,
    GAME_MESSAGE,
    GAME_ERROR,
    GAME_OVER,
    GAME_REDIRECT,
    GAME_UPDATE,
    GIVE_UP,
    JOIN,
    LEAVE,
    MESSAGE,
    MOVE_PADDLE,
    OVER_CALLBACK,
    PADDLE,
    PLAYER,
    PLAYERS,
    PLAYER_NAME,
    REDIRECT,
    REMATCH,
    START_TIMER,
    START_TIMER_CALLBACK,
    TYPE,
    TIME,
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
        self.is_connected = False

    @abstractmethod
    def get_game_logic_interface(self):
        pass

    def get_monitor(self):
        return get_monitor()

    async def connect(self):
        self.game.init_channel(self.scope["url_route"]["kwargs"]["channel_id"])
        await self.accept()
        if self.game.channel is None:
            await self.send_error(
                {CHANNEL_ERROR_CODE: INVALID_CHANNEL, MESSAGE: UNKNOWN_CHANNEL_ID}
            )
        else:
            await self.add_user_to_channel_group()

    async def add_user_to_channel_group(self):
        self.room_group_name = f"game_{self.game.channel.id}"
        logger.info("User Connected to %s", self.room_group_name)
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        self.is_connected = True

    async def disconnect(self, close_code: int):
        try:
            await self.leave(None)
        except ChannelError:
            pass
        if self.room_group_name is not None:
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )
        self.is_connected = False
        logger.info("Disconnect with code: %s", close_code)

    async def receive(self, text_data: str):
        if not self.is_connected:
            logger.error("User not connected.")
            return
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

    async def join(self, message: dict[str, Any]):
        user_id = message[USER_ID]
        player_name = message[PLAYER]
        arena_id: str = message[ARENA_ID]
        callbacks: dict[str, Optional[Callable[[Any], Coroutine[Any, Any, None]]]] = {
            UPDATE_CALLBACK: self.send_update,
            OVER_CALLBACK: self.send_game_over,
            START_TIMER_CALLBACK: self.send_start_timer,
        }
        self.game.join(user_id, player_name, arena_id, callbacks)
        await self.send_message(f"{self.game.user_id} has joined the game.")
        await self.send_players()
        await self.send_arena_data()
        if self.game.is_channel_full():
            assignations: dict[str, Any] = self.game.get_assignations()
            await self.send_redirect({ASSIGNATIONS: assignations})

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

    async def send_players(self):
        players = self.monitor.get_users_from_channel(self.game.channel.id)
        await self.send_update({CHANNEL_PLAYERS: {USER_ID: players, CAPACITY: self.game.channel.user_count}})

    async def send_arena_data(self):
        if self.game.arena_id is None:
            return
        arena: Arena = self.monitor.get_arena(self.game.channel.id, self.game.arena_id)
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
            self.game.channel.id, self.game.arena_id
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

    async def game_redirect(self, event: dict[str, str]):
        message = event[REDIRECT]
        await self.safe_send({TYPE: GAME_REDIRECT, REDIRECT: message})

    async def send_error(self, error: dict[str, Any]):
        logger.info("Sending error: %s: %s", error[CHANNEL_ERROR_CODE], error[MESSAGE])
        await self.safe_send({TYPE: GAME_ERROR, ERROR: error})

    async def send_redirect(self, redirect: dict[str, Any]):
        logger.info("Sending assignations: %s", redirect)
        await self.send_data({TYPE: GAME_REDIRECT, REDIRECT: redirect})

    async def send_update(self, update: dict[str, Any]):
        update = {**{ARENA_ID: self.game.arena_id}, **update}
#         logger.info("Sending update: %s", update)
        await self.send_data({TYPE: GAME_UPDATE, UPDATE: update})

    async def send_message(self, message: str):
        logger.info("Sending message: %s", message)
        await self.send_data({TYPE: GAME_MESSAGE, MESSAGE: message})

    async def send_data(self, data: dict[str, Any]):
        try:
            await self.channel_layer.group_send(self.room_group_name, data)
        except asyncio.CancelledError:
            logger.error("WebSocket connection closed while trying to send a message.")