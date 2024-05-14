import json
import logging
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from back_game.monitor.monitor import monitor
from back_game.game_settings.game_constants import (
    INVALID_ARENA,
    INVALID_CHANNEL,
    NOT_ENTERED,
    NOT_JOINED,
)

log = logging.getLogger(__name__)


class ChannelError(Exception):

    def __init__(self, code, message):
        self.code = code
        self.message = message


class PlayerConsumer(AsyncJsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_id = None
        self.arena = None
        self.room_group_name = None
        self.joined = False
        self.user_id = None

    async def connect(self):
        self.channel_id = self.scope["url_route"]["kwargs"]["channel_id"]
        await self.accept()
        if monitor.channels.get(self.channel_id) is None:
            await self.send_error(
                {"code": INVALID_CHANNEL, "message": "Unknown channel_id"}
            )
        else:
            await self.add_user_to_channel_group()

    async def add_user_to_channel_group(self):
        self.room_group_name = f"game_{self.channel_id}"
        log.info("User Connected to %s", self.room_group_name)
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

    async def disconnect(self, close_code):
        try:
            await self.leave(None)
        except ChannelError:
            pass
        if self.room_group_name is not None:
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )
        log.info("Disconnect with code: %s", close_code)

    async def receive(self, text_data=None):
        content = json.loads(text_data)
        message_type, message = content["type"], content["message"]
        message_binding = {
            "move_paddle": self.move_paddle,
            "join": self.join,
            "leave": self.leave,
            "give_up": self.give_up,
            "rematch": self.rematch,
        }
        try:
            await message_binding[message_type](message)
        except ChannelError as e:
            await self.send_error({"code": e.code, "message": e.message})

    async def join(self, message: dict):
        self.user_id = message["user_id"]
        arena_id = message["arena_id"]
        try:
            self.arena = monitor.channels[self.channel_id][arena_id]
            self.arena.game_update_callback = self.send_update
            self.arena.game_over_callback = self.send_game_over
        except KeyError as e:
            raise ChannelError(INVALID_ARENA, "Unknown arena_id") from e
        try:
            self.arena.enter_arena(self.user_id)
            if not monitor.is_user_in_game(self.user_id, self.channel_id, arena_id):
                monitor.add_user(self.user_id, self.channel_id, arena_id)
        except (KeyError, ValueError) as e:
            log.error("Error: %s", e)
            raise ChannelError(NOT_ENTERED, "User cannot join this arena.") from e
        self.joined = True
        await self.send_message(f"{self.user_id} has joined the game.")
        await self.send_update({"arena": self.arena.to_dict()})

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
        await self.send_update({"give_up": self.user_id})

    async def rematch(self, _):
        if not self.joined:
            raise ChannelError(NOT_JOINED, "Attempt to rematch without joining.")
        arena_data = self.arena.rematch(self.user_id)
        if arena_data is None:
            await self.send_message(f"{self.user_id} asked for a rematch.")
        else:
            await self.send_update({"arena": arena_data})

    async def move_paddle(self, message: dict):
        if not self.joined:
            raise ChannelError(NOT_JOINED, "Attempt to move paddle without joining.")
        player_name = message["player"]
        direction = message["direction"]
        paddle_data = self.arena.move_paddle(player_name, direction)
        await self.send_update({"paddle": paddle_data})

    async def send_game_over(self, game_over_message, time):
        log.info("Game over: %s wins. %s seconds left.", self.arena.get_winner(), time)
        await self.send_update(
            {
            "game_over": {
                "winner": f"{self.arena.get_winner()}",
                "time": time,
                "message": game_over_message
                }
            }
        )

    async def game_message(self, event):
        message = event["message"]
        await self.send(
            text_data=json.dumps({"type": "game_message", "message": message})
        )

    async def game_error(self, event):
        error = event["error"]
        await self.send(
            text_data=json.dumps({"type": "game_error", "error": error})
        )

    async def game_update(self, event):
        message = event["update"]
        await self.send(
            text_data=json.dumps({"type": "game_update", "update": message})
        )

    async def send_error(self, error):
        log.info("Sending error: %s: %s", error["code"], error["message"])
        await self.send(
            text_data=json.dumps({"type": "game_error", "error": error})
        )

    async def send_update(self, update):
        log.info("Sending update: %s", update)
        await self.send_data({"type": "game_update", "update": update})

    async def send_message(self, message):
        log.info("Sending message: %s", message)
        await self.send_data({"type": "game_message", "message": message})

    async def send_data(self, data):
        await self.channel_layer.group_send(self.room_group_name, data)
