import logging

from back_game.game_settings.game_constants import GameStatus
from back_game.monitor.lobby.lobby import Lobby

logger = logging.getLogger(__name__)


class ClassicLobby(Lobby):

    def __init__(self, players_specs: dict[str, int]):
        super().__init__(players_specs)
        self.add_arena()
        self.user_count = 2

    def is_tournament(self) -> bool:
        return False

    def on_user_added(self):
        pass

    async def on_lobby_full(self):
        pass

    def is_ready_to_start(self) -> bool:
        return self.is_full()

    def set_next_round(self):
        pass

    def disable(self):
        pass

    def can_round_be_set(self) -> bool:
        return False

    def can_be_deleted(self) -> bool:
        if len(self.users) == 0:
            return True
        return self.are_all_arenas_in_status_list([GameStatus.DEAD])
