import json
import logging
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
# from .engine import Position, GameEngine

log = logging.getLogger(__name__)

class PlayerConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = None
        self.joined = False
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'game_{self.room_name}'

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

    async def join(self, message: dict):
        username = message["username"]
        await self.save_username_in_session(username)

        self.username = self.scope["session"]["username"]

        log.info(f"{self.username} joining game")
        await self.channel_layer.send(
            "game_engine", {
                "type": "player.new", 
                "player": self.username, 
                "channel": self.channel_name
                },
        )

        await self.send_json({
            "type": "user_joined",
            "username": self.username
        })

        self.joined = True
    
    @database_sync_to_async
    def save_username_in_session(self, username):
        self.scope["session"].setdefault("username", username)
        self.scope["session"].save()

    async def move_paddle(self, message: dict):
        if not self.joined:
            log.error("Attempt to move paddle without joining.")
            return

        log.info(f"{self.username} is moving paddle")
        await self.channel_layer.send(
            "game_engine", {
                "type": "player.position", 
                "player": self.username, 
                "position": message["position"]}
        )

        await self.send_json({
            "type": "paddle_moved",
            "username": self.username
        })

    async def leave(self, message: dict):
        if not self.joined:
            log.error("Attempt to leave without joining.")
            return
        
        log.info(f"{self.username} leaving game")
        await self.channel_layer.send(
            "game_engine", {
                "type": "player.leave",
                "player": self.username,
                "channel": self.channel_name
            },
        )

        await self.send_json({
            "type": "user_left",
            "username": self.username
        })

        self.joined = False

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

    # async def game_update(self, event):
    #     log.info("Game update received")
    #     await self.send(text_data=json.dumps(event["state"]))

# class GameConsumer(SyncConsumer):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.engine = GameEngine("pong_game")
#         self.engine.start()

#     def player_new(self, event):
#         log.info(f"New player: {event['player']}")
#         self.engine.join_queue(event["player"])

#     def paddle_position(self, event):
#         try:
#             position = Position[event["position"]]
#             self.engine.set_player_direction(event["player"], position)
#         except KeyError:
#             log.error(f"Invalid position: {event['position']}")
