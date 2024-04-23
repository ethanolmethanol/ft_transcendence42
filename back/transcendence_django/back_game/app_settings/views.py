import json
from django.http import  JsonResponse
from django.views.decorators.http import require_http_methods
from ..monitor.monitor import monitor
import logging

logger = logging.getLogger(__name__)

@require_http_methods(["POST"])
async def get_channelID(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data['username']
        playerSpecs = data['playerSpecs']
        channel = await monitor.get_channel(username, playerSpecs)
        return JsonResponse(channel, status=200)
    except Exception as e:
        logger.error(e)
        return JsonResponse({'error': str(e)}, status=400)
