import pytest
import logging
import asyncio
import back_game.monitor.GameEngine as GE
from back_game.monitor.game_engine_singleton import gameEngine as SINGLE
from back_game.game_arena.arena import Arena 
from back_game.game_entities.ball import Ball
from back_game.game_entities.paddle import Paddle
from back_game.game_arena.map import Map
from back_game.game_arena.playerMode import PlayerMode
from back_game.game_settings.game_constants import *

@pytest.mark.passed
@pytest.mark.game_engine
def test_addRemoveArena():
	arena = Arena({
		"playerMode": PlayerMode(),
		"paddle": Paddle(),
		"ball": Ball(),
		"map": Map(),
	})
	SINGLE.addArena(arena)
	logging.debug(SINGLE.arenas)
	assert(arena == SINGLE.arenas[-1])
	SINGLE.removeArena(arena)
	assert(0 == len(SINGLE.arenas))

@pytest.mark.passed
@pytest.mark.asyncio
@pytest.mark.game_engine
async def test_start():
	arena = Arena({
		"playerMode": PlayerMode(),
		"paddle": Paddle(),
		"ball": Ball(),
		"map": Map(),
	})
	SINGLE.addArena(arena)
	assert(not SINGLE.started)
	await SINGLE.start()
	assert(SINGLE.started)
	SINGLE.removeArena(arena)

@pytest.mark.passed
@pytest.mark.asyncio
@pytest.mark.game_engine
async def test_run_game_loop():
	for i in range (0, 10):
		SINGLE.addArena(Arena({
			"playerMode": PlayerMode(),
			"paddle": Paddle(),
			"ball": Ball(),
			"map": Map(),
		}))
		SINGLE.arenas[-1].players.append("TestPlayer1")
		SINGLE.arenas[-1].players.append("TestPlayer2")
		SINGLE.arenas[-1].status = STARTED
	await SINGLE.start()
	assert(SINGLE.started)
	SINGLE.arenas[2].status = OVER
	await asyncio.sleep(2)
	assert(len(SINGLE.arenas) == 9)
	SINGLE.arenas
	SINGLE.arenas[2].players.remove("TestPlayer1")
	assert(len(SINGLE.arenas) == 9)
	SINGLE.arenas[2].players.remove("TestPlayer2")
	await asyncio.sleep(2)
	assert(len(SINGLE.arenas) == 8)
	SINGLE.arenas.clear()
	
