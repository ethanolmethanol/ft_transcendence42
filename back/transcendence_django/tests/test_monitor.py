import pytest
from unittest.mock import patch, AsyncMock
from back_game.monitor.monitor import monitor
from back_game.game_arena.arena import Arena 
from back_game.game_entities.ball import Ball
from back_game.game_entities.paddle import Paddle
from back_game.game_arena.map import Map
from back_game.game_settings.game_constants import *

@pytest.mark.passed
@pytest.mark.monitor
@pytest.mark.asyncio
async def test_get_channel():
	username = "testuser"
	playerSpecs = {"nbPlayers": 2, "mode": 0}
	channel = await monitor.get_channel(username, playerSpecs)
	assert channel is not None
	assert "channelID" in channel
	assert "arena" in channel

@pytest.mark.passed
@pytest.mark.monitor
@pytest.mark.asyncio
async def test_get_channel_from_username():
	username = "existing_user"
	playerSpecs = {"nbPlayers": 2, "mode": 0}
	channel = await monitor.get_channel(username, playerSpecs)
	channel = monitor.get_channel_from_username(username)
	assert "channelID" in channel
	assert "arena" in channel

@pytest.mark.passed
@pytest.mark.monitor
def test_delete_arena():
	playerSpecs = {"nbPlayers": 2, "mode": 0}
	monitor.channels = {
		"channel_to_remove": {
			"arena_to_delete": Arena(playerSpecs)
		}
	}
	monitor.deleteArena("channel_to_remove", "arena_to_delete")
	assert "arena_to_delete" not in monitor.channels["channel_to_remove"]

@pytest.mark.monitor
@pytest.mark.asyncio
@pytest.mark.passed
async def test_game_loop():
    playerSpecs = {"nbPlayers": 2, "mode": 0}
    arena = Arena(playerSpecs)
    monitor.channels = {
        "channel_to_remove": {
            "arena_to_delete": arena
        }
    }
    arena.status = DEAD
    with patch('asyncio.sleep', new_callable=AsyncMock):
        await monitor.monitor_arenas_loop("channel_to_remove", monitor.channels["channel_to_remove"].values())
    assert "channel_to_remove" not in monitor.channels
