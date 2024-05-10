import json
import logging
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from back_game.monitor.monitor import monitor
from back_game.game_arena.arena import Arena
from back_game.game_settings.game_constants import *

log = logging.getLogger(__name__)

class ChannelError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

class PlayerConsumer(AsyncJsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channelID = None
        self.arena = None
        self.room_group_name = None
        self.joined = False
        self.username = None

    async def connect(self):
        self.channelID = self.scope['url_route']['kwargs']['channelID']
        # if monitor.channels.get([self.channelID]) == None:
        #     raise ChannelError(INVALID_CHANNEL, "Unknown channelID")
        # close the connection on the consumer side
        self.room_group_name = f'game_{self.channelID}'
        log.info(f"User Connected to {self.room_group_name}")
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        try:
            await self.leave(None)
        except:
            pass
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        log.info(f"Disconnect with code: {close_code}")

    async def receive(self, text_data=None, bytes_data=None):
        content = json.loads(text_data)
        message_type, message = content['type'], content['message']
        message_binding = {
            'move_paddle': self.move_paddle,
            'join': self.join,
            'leave': self.leave,
            'give_up': self.give_up,
            'rematch': self.rematch
        }
        try:
            await message_binding[message_type](message)
        except ChannelError as e:
            await self.send_error({"code": e.code, "message": e.message})

    async def join(self, message: dict):
        self.username = message["username"]
        arenaID = message["arenaID"]
        try:
            self.arena = monitor.channels[self.channelID][arenaID]
            self.arena.game_update_callback = self.send_update
            self.arena.game_over_callback = self.send_game_over
        except KeyError:
            raise ChannelError(INVALID_ARENA, "Unknown arenaID")
        try:
            self.arena.enter_arena(self.username)
            if not monitor.is_user_in_game(self.username, self.channelID, arenaID):
                monitor.addUser(self.username, self.channelID, arenaID)
        except (KeyError, ValueError) as e:
            log.error(f"Error: {e}")
            raise ChannelError(NOT_ENTERED, "User cannot join this arena.")
        self.joined = True
        await self.send_message(f"{self.username} has joined the game.")
        await self.send_update({"arena": self.arena.to_dict()})

    async def leave(self, _):
        if not self.joined:
            raise ChannelError(NOT_JOINED, "Attempt to leave without joining.")
        self.arena.disable_player(self.username)
        self.joined = False
        await self.send_message(f"{self.username} has left the game.")

    async def give_up(self, _):
        if not self.joined:
            raise ChannelError(NOT_JOINED, "Attempt to give up without joining.")
        self.arena.player_gave_up(self.username)
        monitor.deleteUser(self.username)
        self.joined = False
        await self.send_message(f"{self.username} has given up.")
        await self.send_update({"give_up": self.username})

    async def rematch(self, _):
        if not self.joined:
            raise ChannelError(NOT_JOINED, "Attempt to rematch without joining.")
        arena_data = self.arena.rematch(self.username)
        if arena_data is None:
            await self.send_message(f"{self.username} asked for a rematch.")
        else:
            await self.send_update({"arena": arena_data})

    async def move_paddle(self, message: dict):
        if not self.joined:
            raise ChannelError(NOT_JOINED, "Attempt to move paddle without joining.")
        player_name = message['player']
        direction = message['direction']
        paddle_data = self.arena.move_paddle(player_name, direction)
        await self.send_update({"paddle": paddle_data})

    async def send_game_over(self, game_over_message, time):
        log.info(f"Game over: {self.arena.get_winner()} wins. {time} seconds left.")
        await self.send_update({
            "gameover": {
                'winner': f'{self.arena.get_winner()}',
                'time': time,
                'message': game_over_message
                }
            })

    async def game_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'type': "game_message",
            'message': message
        }))

    async def game_error(self, event):
        error = event['error']
        await self.send(text_data=json.dumps({
            'type': "game_error",
            'error': error
        }))

    async def game_update(self, event):
        message = event['update']
        await self.send(text_data=json.dumps({
            'type': "game_update",
            'update': message
        }))

    # async def send_error(self, error):
    #     log.info(f"Sending error: {error["code"]}: {error["message"]}")
    #     await self.send_data({
    #         "type": "game_error",
    #         "error": error
    #     })

    async def send_error(self, error):
        log.info(f"Sending error: {error['code']}: {error['message']}")
        await self.send(text_data=json.dumps({
            "type": "game_error",
            "error": error
        }))

    async def send_update(self, update):
        log.info(f"Sending update: {update}")
        await self.send_data({
            "type": "game_update",
            'update': update
        })

    async def send_message(self, message):
        log.info(f"Sending message: {message}")
        await self.send_data({
            "type": "game_message",
            'message': message
        })

    async def send_data(self, data):
        await self.channel_layer.group_send(
            self.room_group_name, data
        )

