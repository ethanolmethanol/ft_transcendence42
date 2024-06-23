import json
import logging
from http import HTTPStatus
from json import JSONDecodeError
from typing import Any

from back_game.game_settings.dict_keys import (
    ARENA,
    CHANNEL_ID,
    ERROR,
    IS_REMOTE,
    PLAYER_SPECS,
    USER_ID,
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
            raise ValueError("User is already in a channel.")
        channel = await monitor.create_new_channel(user_id, players_specs)
        return JsonResponse(channel, status=HTTPStatus.OK)
    except (JSONDecodeError, TypeError, KeyError, ValueError) as e:
        logger.error(e)
        return JsonResponse({ERROR: str(e)}, status=HTTPStatus.BAD_REQUEST)


@require_http_methods(["POST"])
async def join_channel(request) -> JsonResponse:
    try:
        data = json.loads(request.body.decode("utf-8"))
        user_id = data[USER_ID]
        request_player_specs = data[PLAYER_SPECS]
        asked_mode = request_player_specs[IS_REMOTE]
        channel: dict[str, Any] | None = None
        if CHANNEL_ID not in data:
            logger.info("Joining already created channel.")
            channel = monitor.join_already_created_channel(user_id, asked_mode)
            if channel is None:
                raise ValueError("No available channel.")
        else:
            channel_id: str = data[CHANNEL_ID]
            logger.info("Joining channel: %s", channel_id)
            channel = await monitor.join_channel(user_id, channel_id)
            if channel is None:
                raise ValueError("The channel does not exist.")
        mode = channel[ARENA][PLAYER_SPECS][IS_REMOTE]
        if asked_mode != mode:
            if mode == "online":
                raise ValueError("User is already in a remote channel.")
            raise ValueError("User is already in a local channel.")
        return JsonResponse(channel, status=HTTPStatus.OK)
    except (JSONDecodeError, TypeError, ValueError) as e:
        logger.error(e)
        return JsonResponse({ERROR: str(e)}, status=HTTPStatus.BAD_REQUEST)


@require_http_methods(["POST"])
async def join_specific_channel(request) -> JsonResponse:
    try:
        data = json.loads(request.body.decode("utf-8"))
        user_id = data[USER_ID]
        channel_id: str = data[CHANNEL_ID]
        logger.info("Joining channel: %s", channel_id)
        if monitor.is_user_in_channel(user_id):
            raise ValueError("User is already in a channel.")
        channel = await monitor.join_channel(user_id, channel_id)
        if channel is None:
            raise ValueError("Channel does not exist")
        return JsonResponse(channel, status=HTTPStatus.OK)
    except (JSONDecodeError, TypeError, ValueError) as e:
        logger.error(e)
        return JsonResponse({ERROR: str(e)}, status=HTTPStatus.BAD_REQUEST)


@require_http_methods(["POST"])
async def is_user_in_channel(request) -> JsonResponse:
    try:
        data = json.loads(request.body.decode("utf-8"))
        user_id = data[USER_ID]
        is_user_in_channel_value: bool = monitor.is_user_in_channel(user_id)
        return JsonResponse(
            {"isInChannel": is_user_in_channel_value}, status=HTTPStatus.OK
        )
    except (JSONDecodeError, TypeError) as e:
        logger.error(e)
        return JsonResponse({ERROR: str(e)}, status=HTTPStatus.BAD_REQUEST)
