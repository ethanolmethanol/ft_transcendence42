import json
import logging

from back_game.game_settings.game_constants import (
    INVALID_ARENA,
    INVALID_CHANNEL,
    NOT_ENTERED,
    NOT_JOINED,
    UNKNOWN_CHANNEL_ID,
    UNKNOWN_ARENA_ID,
)
from back_game.game_settings.dict_keys import (
    CHANNEL_ERROR_CODE,
    MESSAGE,
    TYPE,
    MOVE_PADDLE,
    JOIN,
    LEAVE,
    GIVE_UP,
    REMATCH,
    USER_ID,
    ARENA_ID,
    ARENA,
    PLAYER,
    DIRECTION,
    PADDLE,
    GAME_OVER,
    WINNER,
    TIME,
    GAME_MESSAGE,
    ERROR,
    GAME_ERROR,
    GAME_UPDATE,
    UPDATE,
)
from back_game.monitor.monitor import monitor
from back_game.game_arena.arena import Arena
from channels.generic.websocket import AsyncJsonWebsocketConsumer

log = logging.getLogger(__name__)


class ChannelError(Exception):

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message


class PlayerConsumer(AsyncJsonWebsocketConsumer):

    def __init__(self, *args: tuple, **kwargs: dict[str, any]):
        super().__init__(*args, **kwargs)
        self.channel_id: int | None = None
        self.arena: Arena | None = None
        self.room_group_name: str | None = None
        self.joined: bool = False
        self.user_id: int | None = None

    async def connect(self):
        self.channel_id = self.scope["url_route"]["kwargs"]["channel_id"]
        await self.accept()
        if monitor.channels.get(self.channel_id) is None:
            await self.send_error(
                {CHANNEL_ERROR_CODE: INVALID_CHANNEL, MESSAGE: UNKNOWN_CHANNEL_ID}
            )
        else:
            await self.add_user_to_channel_group()

    async def add_user_to_channel_group(self):
        self.room_group_name = f"game_{self.channel_id}"
        log.info("User Connected to %s", self.room_group_name)
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
        log.info("Disconnect with code: %s", close_code)

    async def receive(self, text_data:json = None):
        content = json.loads(text_data)
        message_type, message = content[TYPE], content[MESSAGE]
        message_binding = {
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

    async def join(self, message: dict):
        self.user_id = message[USER_ID]
        arena_id: int = message[ARENA_ID]
        try:
            self.arena = monitor.channels[self.channel_id][arena_id]
            self.arena.game_update_callback = self.send_update
            self.arena.game_over_callback = self.send_game_over
        except KeyError as e:
            raise ChannelError(INVALID_ARENA, UNKNOWN_ARENA_ID) from e
        try:
            self.arena.enter_arena(self.user_id)
            if not monitor.is_user_in_game(self.user_id, self.channel_id, arena_id):
                monitor.add_user(self.user_id, self.channel_id, arena_id)
        except (KeyError, ValueError) as e:
            log.error("Error: %s", e)
            raise ChannelError(NOT_ENTERED, "User cannot join this arena.") from e
        self.joined = True
        await self.send_message(f"{self.user_id} has joined the game.")
        await self.send_update({ARENA: self.arena.to_dict()})

    async def leave(self, _):
        if not self.joined:
            raise ChannelError(NOT_JOINED, "Attempt to leave without joining.")
        self.arena.disable_player(self.user_id)
        self.joined = False
        await self.send_message(f"{self.user_id} has left the game.")

    async def give_up(self, _):
        if not self.joined:
            raise ChannelError(NOT_JOINED, "Attempt to give up without joining.")
        self.arena.player_gave_up(self.user_id)
        monitor.delete_user(self.user_id)
        self.joined = False
        await self.send_message(f"{self.user_id} has given up.")
        await self.send_update({GIVE_UP: self.user_id})

    async def rematch(self, _):
        if not self.joined:
            raise ChannelError(NOT_JOINED, "Attempt to rematch without joining.")
        arena_data: dict | None = self.arena.rematch(self.user_id)
        if arena_data is None:
            await self.send_message(f"{self.user_id} asked for a rematch.")
        else:
            await self.send_update({ARENA: arena_data})

    async def move_paddle(self, message: dict):
        if not self.joined:
            raise ChannelError(NOT_JOINED, "Attempt to move paddle without joining.")
        player_name: str = message[PLAYER]
        direction: str = message[DIRECTION]
        paddle_data: dict = self.arena.move_paddle(player_name, direction)
        await self.send_update({PADDLE: paddle_data})

    async def send_game_over(self, game_over_message: str, time: float):
        log.info("Game over: %s wins. %s seconds left.", self.arena.get_winner(), time)
        await self.send_update(
            {
                GAME_OVER: {
                    WINNER: f"{self.arena.get_winner()}",
                    TIME: time,
                    MESSAGE: game_over_message,
                }
            }
        )

    async def game_message(self, event: dict):
        message = event[MESSAGE]
        await self.send(text_data=json.dumps({TYPE: GAME_MESSAGE, MESSAGE: message}))

    async def game_error(self, event: dict):
        error = event[ERROR]
        await self.send(text_data=json.dumps({TYPE: GAME_ERROR, ERROR: error}))

    async def game_update(self, event: dict):
        message = event[UPDATE]
        await self.send(text_data=json.dumps({TYPE: GAME_UPDATE, UPDATE: message}))

    async def send_error(self, error: dict):
        log.info("Sending error: %s: %s", error[CHANNEL_ERROR_CODE], error[MESSAGE])
        await self.send(text_data=json.dumps({TYPE: GAME_ERROR, ERROR: error}))

    async def send_update(self, update: dict):
        log.info("Sending update: %s", update)
        await self.send_data({TYPE: GAME_UPDATE, UPDATE: update})

    async def send_message(self, message: str):
        log.info("Sending message: %s", message)
        await self.send_data({TYPE: GAME_MESSAGE, MESSAGE: message})

    async def send_data(self, data: dict):
        await self.channel_layer.group_send(self.room_group_name, data)
