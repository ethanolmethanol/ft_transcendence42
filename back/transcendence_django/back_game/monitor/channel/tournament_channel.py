from .channel import Channel
from typing import Any, Dict
from back_game.game_arena.arena import Arena
from back_game.game_settings.game_constants import TOURNAMENT_ARENA_COUNT, TOURNAMENT_MAX_ROUND
from transcendence_django.dict_keys import NB_PLAYERS

import logging

logger = logging.getLogger(__name__)

class TournamentChannel(Channel):

    def __init__(self, players_specs: dict[str, int]):
        super().__init__(players_specs)
        arenas = {}
        for _ in range(TOURNAMENT_ARENA_COUNT):
            new_arena: Arena = Arena(players_specs)
            arenas[new_arena.id] = new_arena
        self.arenas: Dict[str, Arena] = arenas
        self.user_count: int = players_specs[NB_PLAYERS] * len(arenas)
        self.round: int = 1
        self.has_increase_round: bool = False

    def is_tournament(self) -> bool:
        return True

    def is_ready_to_start(self) -> bool:
        return self.is_full() and (self.round == 1 or self.count_non_dead_arenas() == 0)

    def can_be_deleted(self) -> bool:
        if len(self.users) == 0:
            return True
        non_dead_arenas_count = self.count_non_dead_arenas()
        if non_dead_arenas_count == 0 and not self.has_increase_round:
            self.round += 1
            self.has_increase_round = True
            logger.info("Tournament round %s", self.round)
        else:
            self.has_increase_round = False
        return non_dead_arenas_count == 0 and self.round == TOURNAMENT_MAX_ROUND + 1