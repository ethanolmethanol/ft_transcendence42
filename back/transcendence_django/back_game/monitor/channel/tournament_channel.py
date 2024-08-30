from .channel import Channel
import asyncio
from typing import Any, Dict
from back_game.game_arena.arena import Arena
from back_game.game_arena.game import GameStatus
from back_game.game_settings.game_constants import (
    CREATED,
    DEAD,
    DYING,
    TOURNAMENT_ARENA_COUNT,
    TOURNAMENT_MAX_ROUND,
    WAITING,
)
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
        self.assignation_sender = None
        self.is_active = True

    def is_tournament(self) -> bool:
        return True

    def disable(self):
        self.is_active = False

    async def add_user_into_arena(self, user_id: int, arena_id: str):
        if user_id in self.users:
            return
        if len(self.users) < self.user_count:
            arena: Arena = self.arenas[arena_id]
            self.users[user_id] = arena
            logger.info("User %s added to channel %s", user_id, self.id)
            if self.is_full():
                logger.info("Channel %s is full!", self.id)
                asyncio.create_task(self.next_round_loop())
                await self.assignation_sender()
        else:
            logger.error("%s cannot be added in the arena %s: Channel %s is full!", user_id, arena_id, self.id)

    def is_ready_to_start(self) -> bool:
        return self.is_full() and (
                self.round == 0 or self.are_all_arenas_in_status_list([GameStatus(DEAD), GameStatus(DYING)])
        )

    def can_be_deleted(self) -> bool:
        if len(self.users) == 0:
            return True
        return self.are_all_arenas_in_status_list([GameStatus(DEAD)]) and self.round == TOURNAMENT_MAX_ROUND + 1

    def set_next_round(self):
        self.round += 1
        logger.info("Tournament round %s", self.round)

    async def arena_loop(self, arena: Arena):
        while self.round <= TOURNAMENT_MAX_ROUND and self.is_active:
            logger.info("Arena %s loop", arena.id)
            await super().arena_loop(arena)
            await asyncio.sleep(0.1)

    async def next_round_loop(self):
        while self.round <= TOURNAMENT_MAX_ROUND:
            while not self.can_round_be_set():
                if not self.is_active:
                    return
                logger.info("Waiting for next round")
                await asyncio.sleep(0.1)
            self.set_next_round()
            self.__reset_arenas()
            if self.assignation_sender is not None:
                await self.assignation_sender()

    def can_round_be_set(self):
        return self.is_ready_to_start()

    def __reset_arenas(self):
        for arena in self.arenas.values():
            # TODO: set winners as next round players
            logger.info("Reset arena %s", arena.id)
            arena.reset()
            logger.info("Set arena %s status to CREATED", arena.id)
            arena.set_status(GameStatus(CREATED))
