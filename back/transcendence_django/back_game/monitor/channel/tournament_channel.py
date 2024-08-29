from .channel import Channel
import asyncio
from typing import Any, Dict
from back_game.game_arena.arena import Arena
from back_game.game_settings.game_constants import CREATED, DEAD, DYING, TOURNAMENT_ARENA_COUNT, TOURNAMENT_MAX_ROUND
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
        self.assignation_sender = None

    def is_tournament(self) -> bool:
        return True

    def is_ready_to_start(self) -> bool:
        return self.is_full() and (
                self.round == 1 or len(self.arenas) == self.count_arenas(DEAD) + self.count_arenas(DYING)
        )

    def can_be_deleted(self) -> bool:
        if len(self.users) == 0:
            return True
        return len(self.arenas) == self.count_arenas(DEAD) and self.round == TOURNAMENT_MAX_ROUND + 1

    async def set_next_round(self):
        self.round += 1
        logger.info("Tournament round %s", self.round)
        for arena in self.arenas.values():
            # TODO: set winners as next round players
            logger.info("Reset arena %s", arena.id)
            arena.reset()
            logger.info("Set arena %s status to CREATED", arena.id)
            arena.set_status(CREATED)
        if self.assignation_sender is not None:
            await self.assignation_sender()

    def can_round_be_set(self):
        return self.is_ready_to_start()
