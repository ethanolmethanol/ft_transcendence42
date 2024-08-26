from .channel import Channel
from typing import Any, Dict
from back_game.game_arena.arena import Arena
from back_game.game_settings.game_constants import TOURNAMENT_ARENA_COUNT
from transcendence_django.dict_keys import NB_PLAYERS

class TournamentChannel(Channel):

    def __init__(self, players_specs: dict[str, int]):
        super().__init__(players_specs)
        arenas = {}
        for _ in range(TOURNAMENT_ARENA_COUNT):
            new_arena: Arena = Arena(players_specs)
            arenas[new_arena.id] = new_arena
        self.arenas = arenas
        self.user_count = players_specs[NB_PLAYERS] * len(arenas)

    def is_tournament(self) -> bool:
        return True