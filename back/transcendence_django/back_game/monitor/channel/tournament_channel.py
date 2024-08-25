from .channel import Channel
from typing import Any, Dict
from back_game.game_arena.arena import Arena

class TournamentChannel(Channel):

    def __init__(self, players_specs: dict[str, int]):
        super().__init__(players_specs)
        arenas = {}
        for _ in range(2):
            new_arena: Arena = Arena(players_specs)
            arenas[new_arena.id] = new_arena
        self.arenas = arenas
        self.user_count = 4

    def is_tournament(self) -> bool:
        return True