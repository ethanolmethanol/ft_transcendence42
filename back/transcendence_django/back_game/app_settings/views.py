import json
import logging
from http import HTTPStatus
from json import JSONDecodeError

from back_game.game_settings.dict_keys import CHANNEL_ID, ERROR, PLAYER_SPECS, USER_ID
from back_game.monitor.monitor import monitor
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)


@require_http_methods(["POST"])
async def create_channel(request) -> JsonResponse:
    try:
        data = json.loads(request.body.decode("utf-8"))
        user_id = data[USER_ID]
        players_specs = data[PLAYER_SPECS]
        channel = await monitor.get_new_channel(user_id, players_specs)
        if channel is None:
            raise ValueError("A channel already exists")
        return JsonResponse(channel, status=HTTPStatus.OK)
    except (JSONDecodeError, TypeError, ValueError) as e:
        logger.error(e)
        return JsonResponse({ERROR: str(e)}, status=HTTPStatus.BAD_REQUEST)

@require_http_methods(["POST"])
async def join_channel(request) -> JsonResponse:
    try:
        data = json.loads(request.body.decode("utf-8"))
        user_id = data[USER_ID]
        request_player_specs = data[PLAYER_SPECS]
        if CHANNEL_ID not in data:
            channel = monitor.join_already_created_channel(user_id)
        else:
            channel_id = data[CHANNEL_ID]
            channel = await monitor.join_channel(user_id, channel_id)
        if channel is None:
            raise ValueError("Channel does not exist")
        channel_players_specs = channel['arena'][PLAYER_SPECS]
        if request_player_specs != channel_players_specs:
            raise ValueError("Channel has different player specs")
        return JsonResponse(channel, status=HTTPStatus.OK)
    except (JSONDecodeError, TypeError, ValueError) as e:
        logger.error(e)
        return JsonResponse({ERROR: str(e)}, status=HTTPStatus.BAD_REQUEST)

@require_http_methods(["POST"])
async def is_user_in_channel(request) -> JsonResponse:
    try:
        data = json.loads(request.body.decode("utf-8"))
        user_id = data[USER_ID]
        channel = monitor.get_channel_from_user_id(user_id)
        return JsonResponse({"isInChannel": channel is not None}, status=HTTPStatus.OK)
    except (JSONDecodeError, TypeError) as e:
        logger.error(e)
        return JsonResponse({ERROR: str(e)}, status=HTTPStatus.BAD_REQUEST)
