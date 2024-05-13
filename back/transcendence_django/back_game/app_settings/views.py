import json
import logging
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from ..monitor.monitor import monitor

logger = logging.getLogger(__name__)


@require_http_methods(["POST"])
async def get_channel_id(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        user_id = data["user_id"]
        players_pecs = data["players_pecs"]
        channel = await monitor.getChannel(user_id, players_pecs)
        return JsonResponse(channel, status=200)
    except Exception as e:
        logger.error(e)
        return JsonResponse({"error": str(e)}, status=400)
