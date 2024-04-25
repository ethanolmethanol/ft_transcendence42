import pytest
import back_game.monitor.monitor as monitor
from back_game.game_settings.game_constants import *

@pytest.mark.passed
@pytest.mark.monitor
async def test_addRemoveArena():
	request = {
		"username": "TestUser",
		"playerMode": {"nbPlayers": 2, "mode": 0}
	}
	channel = await monitor.getChannel(request)
	# logging.debug(monitor.arenas)
	assert(channel == monitor.channels[channel["channelID"]])
	monitor.deleteArena(channel["channelID"], channel["arena"]["id"])
	monitor.deleteChannel(channel)
	assert(0 == len(monitor.channels))

# @pytest.mark.passed
# @pytest.mark.asyncio
# @pytest.mark.monitor
# async def test_start():
# 	arena = Arena({
# 		"playerMode": PlayerMode(),
# 		"paddle": Paddle(),
# 		"ball": Ball(),
# 		"map": Map(),
# 	})
# 	SINGLE.addArena(arena)
# 	assert(not SINGLE.started)
# 	await SINGLE.start()
# 	assert(SINGLE.started)
# 	SINGLE.removeArena(arena)

# @pytest.mark.passed
# @pytest.mark.asyncio
# @pytest.mark.monitor
# async def test_run_game_loop():
# 	for i in range (0, 10):
# 		SINGLE.addArena(Arena({
# 			"playerMode": PlayerMode(),
# 			"paddle": Paddle(),
# 			"ball": Ball(),
# 			"map": Map(),
# 		}))
# 		SINGLE.arenas[-1].players.append("TestPlayer1")
# 		SINGLE.arenas[-1].players.append("TestPlayer2")
# 		SINGLE.arenas[-1].status = STARTED
# 	await SINGLE.start()
# 	assert(SINGLE.started)
# 	SINGLE.arenas[2].status = OVER
# 	await asyncio.sleep(2)
# 	assert(len(SINGLE.arenas) == 9)
# 	SINGLE.arenas
# 	SINGLE.arenas[2].players.remove("TestPlayer1")
# 	assert(len(SINGLE.arenas) == 9)
# 	SINGLE.arenas[2].players.remove("TestPlayer2")
# 	await asyncio.sleep(2)
# 	assert(len(SINGLE.arenas) == 8)
# 	SINGLE.arenas.clear()

