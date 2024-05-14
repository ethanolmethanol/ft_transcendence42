import json
import logging
from json import JSONDecodeError
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from back_game.monitor.monitor import monitor

logger = logging.getLogger(__name__)


@require_http_methods(["POST"])
async def get_channel_id(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        user_id = data["user_id"]
        players_specs = data["players_specs"]
        channel = await monitor.get_channel(user_id, players_specs)
        return JsonResponse(channel, status=200)
    except (JSONDecodeError, TypeError) as e:
        logger.error(e)
        return JsonResponse({"error": str(e)}, status=400)
