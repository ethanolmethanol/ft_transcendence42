from .channel import Channel
from typing import Any, Dict
from back_game.game_arena.arena import Arena

class ClassicChannel(Channel):

    def __init__(self, players_specs: dict[str, int]):
        super().__init__(players_specs)
        arena = Arena(players_specs)
        self.arenas: Dict[str, Arena] = {arena.id: arena}
        self.user_count = 2

    def is_tournament(self) -> bool:
        return False

    def is_ready_to_start(self) -> bool:
        return self.is_full()

    def can_be_deleted(self) -> bool:
        if len(self.users) == 0:
            return True
        non_dead_arenas_count = self.count_non_dead_arenas()
        return non_dead_arenas_count == 0
