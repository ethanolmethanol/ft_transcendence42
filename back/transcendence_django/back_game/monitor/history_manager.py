from typing import Any

from asgiref.sync import sync_to_async
from django.apps import apps
from transcendence_django.dict_keys import (
    ARENA_ID,
    IS_REMOTE,
    PLAYERS,
    START_TIME,
    USER_ID,
    WINNER,
)


class HistoryManager:

    def __init__(self):
        self.game_summary_model = apps.get_model("shared_models", "GameSummary")
        self.custom_user_model = apps.get_model("shared_models", "CustomUser")

    async def save_game_summary(self, summary: dict[str, Any]):
        if summary[WINNER] is None:
            winner_user_id = None
        else:
            winner_user_id = summary[WINNER].get(USER_ID)
        game_summary = await sync_to_async(self.game_summary_model.objects.create)(
            arena_id=summary[ARENA_ID],
            winner_user_id=winner_user_id,
            players=summary[PLAYERS],
            is_remote=summary[IS_REMOTE],
            start_time=summary[START_TIME],
        )
        if summary[IS_REMOTE]:
            for player in summary[PLAYERS]:
                await self.__save_game_summary_for_player(player, game_summary)
        else:
            player = summary[PLAYERS][0]
            await self.__save_game_summary_for_player(player, game_summary)

    async def __save_game_summary_for_player(self, player, game_summary):
        user_id = player.get(USER_ID)
        if user_id:
            user = await sync_to_async(self.custom_user_model.objects.get)(pk=user_id)
            await user.save_game_summary(game_summary)
