from .channel import Channel
from typing import Any, Dict
from back_game.game_arena.arena import Arena
from back_game.game_settings.game_constants import DEAD, DYING, TOURNAMENT_ARENA_COUNT, TOURNAMENT_MAX_ROUND
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
        self.round: int = 0
        self.has_increase_round: bool = False

    def is_tournament(self) -> bool:
        return True

    def is_ready_to_start(self) -> bool:
        logger.info("Tournament is ready to start?")
        logger.info("Is full? %s", self.is_full())
        logger.info("Round: %s", self.round)
        logger.info("Count non dead arenas: %s", len(self.arenas) - self.count_arenas(DEAD) - self.count_arenas(DYING))
        return self.is_full() and (self.round == 0 or len(self.arenas) - (self.count_arenas(DEAD) + self.count_arenas(DYING)) == 0)

    def can_be_deleted(self) -> bool:
        if len(self.users) == 0:
            return True
        return len(self.arenas) == self.count_arenas(DEAD) and self.round == TOURNAMENT_MAX_ROUND + 1

    def set_next_round(self):
        if len(self.arenas) == self.count_arenas(DEAD) + self.count_arenas(DYING) and not self.has_increase_round:
            self.round += 1
            logger.info("Tournament round %s", self.round)
            self.has_increase_round = True
            for arena in self.arenas.values():
                # set winners as next round players
                arena.reset()
        else:
            self.has_increase_round = False