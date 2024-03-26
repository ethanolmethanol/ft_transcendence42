import pytest
import json
from channels.testing import WebsocketCommunicator
from game.routing import application

@pytest.mark.asyncio
async def test_game_connection():
    communicator = WebsocketCommunicator(application, "/ws/game/room123")
    connected, subprotocol = await communicator.connect()
    assert connected
    await communicator.disconnect()

@pytest.mark.asyncio
async def test_join_game():
    communicator = WebsocketCommunicator(application, "/ws/game/room123/")
    await communicator.connect()
    await communicator.send_json_to({
        "type": "join",
        "message": {
            "username": "testuser"
        }
    })
    response = await communicator.receive_json_from()
    assert "user_joined" in response["type"]
    await communicator.disconnect()

@pytest.mark.asyncio
async def test_move_paddle():
    communicator = WebsocketCommunicator(application, "/ws/game/room123/")
    await communicator.connect()
    await communicator.send_json_to({
        "type": "move_paddle",
        "message": {
            "position": "up"
        }async de
    })
    response = await communicator.receive_json_from()
    assert "paddle_moved" in response["type"]
    await communicator.disconnect()