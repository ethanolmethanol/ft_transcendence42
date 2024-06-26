import json
import logging
from http import HTTPStatus
from json import JSONDecodeError

from back_game.game_settings.dict_keys import ERROR, PLAYER_SPECS, USER_ID
from back_game.monitor.monitor import monitor
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)


@require_http_methods(["POST"])
async def get_channel_id(request) -> JsonResponse:
    try:
        data = json.loads(request.body.decode("utf-8"))
        user_id = data[USER_ID]
        players_specs = data[PLAYER_SPECS]
        channel = await monitor.get_channel(user_id, players_specs)
        return JsonResponse(channel, status=HTTPStatus.OK)
    except (JSONDecodeError, TypeError) as e:
        logger.error(e)
        return JsonResponse({ERROR: str(e)}, status=HTTPStatus.BAD_REQUEST)
