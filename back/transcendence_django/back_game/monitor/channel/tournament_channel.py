from .channel import Channel
import asyncio
from typing import Any, Dict
from back_game.game_arena.arena import Arena
from back_game.game_arena.game import GameStatus
from back_game.game_arena.player import Player
from back_game.game_settings.game_constants import (
    ARENA_LOOP_INTERVAL,
    CREATED,
    DEAD,
    DYING,
    NEXT_ROUND_LOOP_INTERVAL,
    TOURNAMENT_ARENA_COUNT,
    TOURNAMENT_MAX_ROUND,
    WAITING,
    WAIT_NEXT_ROUND_INTERVAL,
)
from transcendence_django.dict_keys import (
    ASSIGNATIONS,
    NB_PLAYERS,
    ROUNDS_MAP,
    TOURNAMENT_WINNER,
)

import logging

logger = logging.getLogger(__name__)


class TournamentChannel(Channel):

    def __init__(self, players_specs: dict[str, int]):
        super().__init__(players_specs)
        logger.info("Tournament channel created: %s", TOURNAMENT_MAX_ROUND)
        for _ in range(TOURNAMENT_ARENA_COUNT):
            self.add_arena()
        self.user_count: int = self.players_specs[NB_PLAYERS] * len(self.arenas)
        self.round: int = 0
        self.update_sender = None
        self.tournament_map_sender = None
        self.is_active = True
        self.rounds_map: Dict[str, Dict[str, list[dict[str, Any] | None]]] = (
            self.__get_initial_rounds_map()
        )
        self.winner = None

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
            self.__update_rounds_map()
            logger.info("User %s added to channel %s", user_id, self.id)
            if self.is_full():
                logger.info("Channel %s is full!", self.id)
                asyncio.create_task(self.next_round_loop())
        else:
            logger.error(
                "%s cannot be added in the arena %s: Channel %s is full!",
                user_id,
                arena_id,
                self.id,
            )

    def is_ready_to_start(self) -> bool:
        return (self.is_full() and self.round == 0) or (
            self.are_all_arenas_in_status_list([GameStatus(DEAD), GameStatus(DYING)])
        )

    def can_be_deleted(self) -> bool:
        if len(self.users) == 0:
            return True
        return (
            self.are_all_arenas_in_status_list([GameStatus(DEAD)])
            and self.round == TOURNAMENT_MAX_ROUND + 1
        )

    def set_next_round(self):
        if 1 <= self.round <= TOURNAMENT_MAX_ROUND:
            self.__set_next_round_arenas()
        self.round += 1
        logger.info("Tournament round %s", self.round)

    async def arena_loop(self, arena: Arena):
        while self.round <= TOURNAMENT_MAX_ROUND and self.is_active:
            logger.info("Arena %s loop", arena.id)
            await super().arena_loop(arena)
            await asyncio.sleep(ARENA_LOOP_INTERVAL)

    async def next_round_loop(self):
        while self.round <= TOURNAMENT_MAX_ROUND:
            self.set_next_round()
            await self.send_tournament_map()
            await asyncio.sleep(WAIT_NEXT_ROUND_INTERVAL)
            await self.send_assignations()
            while not self.can_round_be_set():
                if not self.is_active:
                    return
                logger.info("Waiting for next round")
                await asyncio.sleep(NEXT_ROUND_LOOP_INTERVAL)

    async def send_assignations(self):
        if self.update_sender is not None:
            assignations: dict[str, Any] = self.get_assignations()
            logger.info("Send assignations %s", assignations)
            await self.update_sender({ASSIGNATIONS: assignations})

    async def send_tournament_map(self):
        if self.tournament_map_sender is not None:
            await self.tournament_map_sender()

    def can_round_be_set(self):
        return self.is_ready_to_start()

    def get_tournament_map(self) -> Dict[str, Dict[str, list[int | None]]]:
        logger.info(
            "Tournament winner %s", self.winner.user_id if self.winner else None
        )
        return {
            ROUNDS_MAP: self.rounds_map,
            TOURNAMENT_WINNER: self.winner.user_id if self.winner else None,
        }

    async def __send_update(self, data: dict[str, Any]):
        if self.update_sender is not None:
            await self.update_sender(data)

    def __get_initial_rounds_map(self) -> Dict[str, Dict[str, list[None]]]:
        rounds_map = {}
        for i in range(TOURNAMENT_MAX_ROUND):
            round = {}
            arena_count = TOURNAMENT_ARENA_COUNT // 2**i
            for j in range(arena_count):
                round[str(j)] = [None for _ in range(self.players_specs[NB_PLAYERS])]
            rounds_map[str(i + 1)] = round
        return rounds_map

    def __get_current_round_arenas(self, round) -> Dict[str, list[int | None]]:
        arena_count = len(self.rounds_map[str(round)])
        round_arenas = {}
        user_ids = list(self.users.keys())
        user_index = 0
        for arena_id in range(arena_count):
            round_arenas[str(arena_id)] = []
            for _ in range(self.players_specs[NB_PLAYERS]):
                if user_index < len(user_ids):
                    round_arenas[str(arena_id)].append(user_ids[user_index])
                    user_index += 1
                else:
                    round_arenas[str(arena_id)].append(None)

        return round_arenas

    def __update_rounds_map(self):
        next_round = self.round + 1
        if next_round <= TOURNAMENT_MAX_ROUND:
            self.rounds_map[str(next_round)] = self.__get_current_round_arenas(
                next_round
            )

    def __set_next_round_arenas(self):
        winners: list[Player | None] = self.__get_winners()
        active_winners = [winner for winner in winners if winner.user_id in self.users]
        if len(active_winners) == 1 and self.round == TOURNAMENT_MAX_ROUND:
            self.winner = active_winners[0]
        self.arenas = {}
        for _ in range(len(active_winners) // 2):
            self.add_arena()
        self.__assign_users_to_arenas(active_winners)
        self.__update_rounds_map()

    def __get_winners(self) -> list[Player | None]:
        winners = []
        for arena in self.arenas.values():
            winner = arena.get_winner()
            if winner:
                logger.info("Arena %s winner: %s", arena.id, winner.player_name)
                winners.append(winner)
            else:
                logger.info(
                    "Arena %s has no winner and has %s status",
                    arena.id,
                    arena.get_status(),
                )
        return winners

    def __assign_users_to_arenas(self, winners: list[Player | None]):
        logger.info(
            "Assign users to arenas: winners (%s)",
            [winner.player_name for winner in winners],
        )
        for user_id in self.users.keys():
            if user_id in (winner.user_id for winner in winners):
                for new_arena in self.arenas.values():
                    if new_arena.is_full():
                        continue
                    self.users[user_id] = new_arena
                    break
            else:
                self.users[user_id] = None
