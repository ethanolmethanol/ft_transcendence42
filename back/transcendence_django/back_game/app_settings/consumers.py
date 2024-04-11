import json
import logging
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from back_game.monitor.monitor import Monitor
from back_game.game_arena.arena import Arena


log = logging.getLogger(__name__)

class PlayerConsumer(AsyncJsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channelID = None
        self.room_group_name = None
        self.joined = False
        self.username = None

    async def connect(self):
        self.channelID = self.scope['url_route']['kwargs']['channelID']
        self.room_group_name = f'game_{self.channelID}'
        log.info(f"User Connected to {self.room_group_name}")
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        log.info(f"Disconnect with code: {close_code}")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        content = json.loads(text_data)
        message_type, message = content['type'], content['message']
        if message_type == 'move_paddle':
            await self.move_paddle(message)
        elif message_type == 'join':
            await self.join(message)
        elif message_type == 'leave':
            await self.leave(message)
        else:
            log.warning(f"Unknown message type: {message_type}")

    async def join(self, message: dict):
        arena = Monitor().arenas.get(self.channelID)
        self.username = message["username"]
        arena.join(self.username)
        log.info(f"{self.username} joined game")
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "game_message",
                'message': f"{self.username} has joined the game."
            }
        )
        self.joined = True

    async def leave(self, message: dict):
        if not self.joined:
            log.error("Attempt to leave without joining.")
            return
        arena = Monitor().arenas.get(self.channelID)
        arena.leave(self.username)
        log.info(f"{self.username} leaving game")
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "game_message",
                "message": f"{self.username} has left the game."
            },
        )
        self.joined = False

    async def move_paddle(self, message: dict):
        if not self.joined:
            log.error("Attempt to move paddle without joining.")
            return
        position = message['position']
        log.info(f"{self.username} moved paddle to {position}.")
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "game_message",
                "position": position,
                "message": f"{self.username} moved paddle to{position}."
            }
        )

    async def game_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
