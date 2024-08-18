from back_game.app_settings.base_consumer import BaseConsumer
from back_game.app_settings.game_logic_interface import GameLogicInterface
from back_game.monitor.monitor import get_monitor
from transcendence_django.dict_keys import USER_ID, PLAYER, ARENA_ID, UPDATE_CALLBACK, OVER_CALLBACK, START_TIMER_CALLBACK, GIVE_UP
from typing import Any, Callable, Coroutine, Optional

class TournamentConsumer(BaseConsumer):

    def get_game_logic_interface(self):
        return GameLogicInterface(is_tournament=True)

    def get_monitor(self):
        return get_monitor()

    async def join(self, message: dict[str, Any]):
        user_id = message[USER_ID]
        player_name = message[PLAYER]
        arena_id: str = message[ARENA_ID]
        callbacks: dict[str, Optional[Callable[[Any], Coroutine[Any, Any, None]]]] = {
            UPDATE_CALLBACK: self.send_update,
            OVER_CALLBACK: self.send_game_over,
            START_TIMER_CALLBACK: self.send_start_timer,
        }
        self.game.join(user_id, player_name, arena_id, callbacks)
        await self.send_message(f"{self.game.user_id} has joined the game.")
        await self.send_arena_data()

    async def leave(self, _):
        self.game.leave()
        await self.send_message(f"{self.game.user_id} has left the game.")

    async def give_up(self, _):
        self.game.give_up()
        await self.send_message(f"{self.game.user_id} has given up.")
        await self.send_update({GIVE_UP: self.game.user_id})
#         await self.send_arena_data()

    async def rematch(self, _):
        self.game.rematch()
        await self.send_message(f"{self.game.user_id} asked for a rematch.")
#         await self.send_arena_data()
