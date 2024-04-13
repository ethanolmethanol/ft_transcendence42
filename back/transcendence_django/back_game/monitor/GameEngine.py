import asyncio
import logging
from back_game.game_settings.game_constants import *

log = logging.getLogger(__name__)

class GameEngine:
    def __init__(self):
        self.arenas = []
        self.game_loop_task = None
        self.started = False

    def addArena(self, arena):
        self.arenas.append(arena)

    def removeArena(self, arena):
        self.arenas.remove(arena)

    async def start(self):
        if not self.started:
            self.game_loop_task = asyncio.create_task(self.run_game_loop())
            self.started = True

    async def run_game_loop(self):
        while any(arena.status != OVER for arena in self.arenas):
            await self.update_game_states()
            await asyncio.sleep(1)
        self.started = False

    async def update_game_states(self):
        for arena in self.arenas:
            if (arena.status == STARTED and len(arena.players) == 1):
                # make the only one player win and set the status to over
                pass
            if (arena.status == STARTED and arena.isEmpty())\
                or arena.status == OVER:
                await self.gameOver(arena)
            
    async def gameOver(self, arena):
        arena.status = OVER
        if hasattr(arena, 'game_over_callback'):
            await arena.game_over_callback('Game Over! Thank you for playing.')
        # self.removeArena(arena)


#   TODO - NEXT STEPS (before the game physics)
#       -> envoyer stats de fin de jeux / finir implementation sendGameOver
#       -> implementer test pour la ws, le monitor et l'arene
#       -> connecter avec le front