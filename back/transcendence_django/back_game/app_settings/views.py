import json
import logging
from http import HTTPStatus
from json import JSONDecodeError

from back_game.game_settings.dict_keys import (
    ARENA,
    CHANNEL_ID,
    ERROR,
    MODE,
    PLAYER_SPECS,
    USER_ID
)
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
        if monitor.is_user_in_channel(user_id):
            raise ValueError("User is already in a channel")
        channel = await monitor.create_new_channel(user_id, players_specs)
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
        is_remote = request_player_specs[MODE]
        if CHANNEL_ID not in data:
            logger.info("Joining already created channel")
            channel = monitor.join_already_created_channel(user_id, is_remote)
            if channel is None:
                raise ValueError("No available channel")
        else:
            channel_id = data[CHANNEL_ID]
            logger.info("Joining channel: %s", channel_id)
            channel = await monitor.join_channel(user_id, channel_id)
            if channel is None:
                raise ValueError("Channel does not exist")
        channel_players_specs = channel[ARENA][PLAYER_SPECS]
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
        is_user_in_channel: bool = monitor.is_user_in_channel(user_id)
        return JsonResponse({"isInChannel": is_user_in_channel}, status=HTTPStatus.OK)
    except (JSONDecodeError, TypeError) as e:
        logger.error(e)
        return JsonResponse({ERROR: str(e)}, status=HTTPStatus.BAD_REQUEST)
