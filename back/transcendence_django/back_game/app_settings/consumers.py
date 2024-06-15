import asyncio
import json
import logging
from typing import Any, Callable, Coroutine, Optional

from back_game.game_arena.arena import Arena
from back_game.game_settings.dict_keys import (
    ARENA,
    ARENA_ID,
    CHANNEL_ERROR_CODE,
    DIRECTION,
    ERROR,
    GAME_ERROR,
    GAME_MESSAGE,
    GAME_OVER,
    GAME_UPDATE,
    GIVE_UP,
    JOIN,
    LEAVE,
    MESSAGE,
    MOVE_PADDLE,
    OVER_CALLBACK,
    PADDLE,
    PLAYER,
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
from back_game.game_settings.game_constants import (
    INVALID_ARENA,
    INVALID_CHANNEL,
    NOT_ENTERED,
    NOT_JOINED,
    UNKNOWN_ARENA_ID,
    UNKNOWN_CHANNEL_ID,
)
from back_game.monitor.monitor import monitor
from channels.generic.websocket import AsyncJsonWebsocketConsumer

logger = logging.getLogger(__name__)


class ChannelError(Exception):

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message


class PlayerConsumer(AsyncJsonWebsocketConsumer):

    def __init__(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]):
        super().__init__(*args, **kwargs)
        self.channel_id: str = ""
        self.arena_id: str = ""
        self.room_group_name: str | None = None
        self.joined: bool = False
        self.user_id: int = -1

    async def connect(self):
        self.channel_id = self.scope["url_route"]["kwargs"]["channel_id"]
        await self.accept()
        if monitor.does_exist_channel(self.channel_id) is False:
            await self.send_error(
                {CHANNEL_ERROR_CODE: INVALID_CHANNEL, MESSAGE: UNKNOWN_CHANNEL_ID}
            )
        else:
            await self.add_user_to_channel_group()

    async def add_user_to_channel_group(self):
        self.room_group_name = f"game_{self.channel_id}"
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

    async def join(self, message: dict[str, Any]):
        self.user_id = message[USER_ID]
        player_name = message[PLAYER]
        arena_id: str = message[ARENA_ID]
        try:
            logger.info("Joining arena %s", arena_id)
            callbacks: dict[
                str, Optional[Callable[[str, Any], Coroutine[Any, Any, None]]]
            ] = {
                UPDATE_CALLBACK: self.send_update,
                OVER_CALLBACK: self.send_game_over,
                START_TIMER_CALLBACK: self.send_start_timer,
            }
            monitor.init_arena(
                self.channel_id,
                arena_id,
                callbacks,
            )
            self.arena_id = arena_id
        except KeyError as e:
            raise ChannelError(INVALID_ARENA, UNKNOWN_ARENA_ID) from e
        try:
            monitor.join_arena(self.user_id, player_name, self.channel_id, arena_id)
        except (KeyError, ValueError) as e:
            logger.error("Error: %s", e)
            raise ChannelError(NOT_ENTERED, "User cannot join this arena.") from e
        self.joined = True
        await self.send_message(f"{self.user_id} has joined the game.")
        await self.send_arena_data(self.channel_id, self.arena_id)

    async def leave(self, _):
        if not self.joined:
            raise ChannelError(NOT_JOINED, "Attempt to leave without joining.")
        monitor.leave_arena(self.user_id, self.channel_id, self.arena_id)
        self.joined = False
        await self.send_message(f"{self.user_id} has left the game.")

    async def give_up(self, _):
        if not self.joined:
            raise ChannelError(NOT_JOINED, "Attempt to give up without joining.")
        monitor.give_up(self.user_id, self.channel_id, self.arena_id)
        self.joined = False
        await self.send_message(f"{self.user_id} has given up.")
        await self.send_update({GIVE_UP: self.user_id})
        await self.send_arena_data(self.channel_id, self.arena_id)

    async def rematch(self, _):
        if not self.joined:
            raise ChannelError(NOT_JOINED, "Attempt to rematch without joining.")
        monitor.rematch(self.user_id, self.channel_id, self.arena_id)
        await self.send_message(f"{self.user_id} asked for a rematch.")
        await self.send_arena_data(self.channel_id, self.arena_id)

    async def move_paddle(self, message: dict[str, Any]):
        if not self.joined:
            raise ChannelError(NOT_JOINED, "Attempt to move paddle without joining.")
        player_name: str = message[PLAYER]
        direction: int = message[DIRECTION]
        paddle_data: dict[str, Any] = monitor.move_paddle(
            self.channel_id, self.arena_id, player_name, direction
        )
        await self.send_update({PADDLE: paddle_data})

    async def send_arena_data(self, channel_id: str, arena_id: str):
        arena: Arena = monitor.get_arena(channel_id, arena_id)
        await self.send_update({ARENA: arena.to_dict()})

    async def send_start_timer(self, start_timer_message: str, time: float):
        logger.info("Game will begin in %s seconds...", time)
        await self.send_update(
            {
                START_TIMER: {
                    TIME: time,
                    MESSAGE: start_timer_message,
                }
            }
        )

    async def send_game_over(self, game_over_message: str, time: float):
        winner = monitor.get_winner(self.channel_id, self.arena_id)
        logger.info("Game over: %s wins. %s seconds left.", winner, time)
        await self.send_update(
            {
                GAME_OVER: {
                    WINNER: winner,
                    TIME: time,
                    MESSAGE: game_over_message,
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
        except Exception as e:
            logger.error("Unexpected error: %s", e)


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
