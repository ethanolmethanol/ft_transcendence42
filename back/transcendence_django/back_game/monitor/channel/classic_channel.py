from .channel import Channel
from typing import Any, Dict
from back_game.game_arena.arena import Arena

class ClassicChannel(Channel):

    def __init__(self, players_specs: dict[str, int]):
        super().__init__(players_specs)
        arena = Arena(players_specs)
        self.arenas: Dict[str, Arena] = {arena.id: arena}
        self.user_count = 2

    def to_dict(self) -> Dict[str, Any]:
        return {
            "channel_id": self.id,
            "arenas": [arena.to_dict() for arena in self.arenas.values()],
            "is_tournament": False,
        }

    def is_tournament(self) -> bool:
        return False