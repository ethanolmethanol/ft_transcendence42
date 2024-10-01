import json
import logging
from http import HTTPStatus
from json import JSONDecodeError
from typing import Any

from back_game.monitor.monitor import get_monitor
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from transcendence_django.dict_keys import (
    ARENA,
    ERROR,
    IS_REMOTE,
    LOBBY_ID,
    PLAYER_SPECS,
    USER_ID,
)

logger = logging.getLogger(__name__)
MONITOR = get_monitor()


@require_http_methods(["POST"])
async def create_lobby(request) -> JsonResponse:
    try:
        data = json.loads(request.body.decode("utf-8"))
        user_id = data[USER_ID]
        players_specs = data[PLAYER_SPECS]
        if MONITOR.is_user_in_lobby(user_id):
            raise ValueError("User is already in a lobby.")
        lobby = await MONITOR.create_new_lobby(user_id, players_specs)
        logger.info(
            "User %s created a new lobby and got the lobby dict: %s",
            user_id,
            lobby,
        )
        return JsonResponse(lobby, status=HTTPStatus.OK)
    except (JSONDecodeError, TypeError, KeyError, ValueError) as e:
        logger.error(e)
        return JsonResponse({ERROR: str(e)}, status=HTTPStatus.BAD_REQUEST)


@require_http_methods(["POST"])
async def join_lobby(request) -> JsonResponse:
    try:
        data = json.loads(request.body.decode("utf-8"))
        user_id = data[USER_ID]
        request_player_specs = data[PLAYER_SPECS]
        asked_mode = request_player_specs[IS_REMOTE]
        lobby: dict[str, Any] | None = None
        if LOBBY_ID not in data:
            logger.info("Joining already created lobby.")
            lobby = MONITOR.join_already_created_lobby(user_id, asked_mode)
            if lobby is None:
                raise ValueError("No available lobby.")
        else:
            lobby_id: str = data[LOBBY_ID]
            logger.info("Joining lobby: %s", lobby_id)
            lobby = await MONITOR.join_lobby(user_id, lobby_id)
            if lobby is None:
                raise ValueError("The lobby does not exist.")
        mode = lobby[ARENA][PLAYER_SPECS][IS_REMOTE]
        if asked_mode != mode:
            if mode == "online":
                raise ValueError("User is already in a remote lobby.")
            raise ValueError("User is already in a local lobby.")
        return JsonResponse(lobby, status=HTTPStatus.OK)
    except (JSONDecodeError, TypeError, ValueError) as e:
        logger.error(e)
        return JsonResponse({ERROR: str(e)}, status=HTTPStatus.BAD_REQUEST)


@require_http_methods(["POST"])
async def join_specific_lobby(request) -> JsonResponse:
    try:
        data = json.loads(request.body.decode("utf-8"))
        user_id = data[USER_ID]
        lobby_id: str = data[LOBBY_ID]
        logger.info("Joining lobby: %s", lobby_id)
        if MONITOR.is_user_in_lobby(user_id):
            raise ValueError("User is already in a lobby.")
        lobby = await MONITOR.join_lobby(user_id, lobby_id)
        if lobby is None:
            raise ValueError("Lobby does not exist")
        return JsonResponse(lobby, status=HTTPStatus.OK)
    except (JSONDecodeError, TypeError, ValueError) as e:
        logger.error(e)
        return JsonResponse({ERROR: str(e)}, status=HTTPStatus.BAD_REQUEST)


@require_http_methods(["POST"])
async def join_tournament(request) -> JsonResponse:
    try:
        data = json.loads(request.body.decode("utf-8"))
        user_id = data[USER_ID]
        lobby = await MONITOR.join_tournament(user_id)
        logger.info(
            "User %s joined tournament and got the lobby dict: %s", user_id, lobby
        )
        return JsonResponse(lobby, status=HTTPStatus.OK, safe=False)
    except (JSONDecodeError, TypeError, ValueError) as e:
        logger.error(e)
        return JsonResponse({ERROR: str(e)}, status=HTTPStatus.BAD_REQUEST)


@require_http_methods(["POST"])
def is_user_in_lobby(request) -> JsonResponse:
    try:
        data = json.loads(request.body.decode("utf-8"))
        user_id = data[USER_ID]
        is_user_in_lobby_value: bool = MONITOR.is_user_in_lobby(user_id)
        return JsonResponse(
            {"isInLobby": is_user_in_lobby_value}, status=HTTPStatus.OK
        )
    except (JSONDecodeError, TypeError) as e:
        logger.error(e)
        return JsonResponse({ERROR: str(e)}, status=HTTPStatus.BAD_REQUEST)
