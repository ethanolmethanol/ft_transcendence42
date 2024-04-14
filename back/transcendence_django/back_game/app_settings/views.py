import json
from django.http import  JsonResponse
from django.views.decorators.http import require_http_methods
from ..monitor.monitor import monitor
import logging
import asyncio

logger = logging.getLogger(__name__)

@require_http_methods(["POST"])
async def getChannelID(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data['username']
        playerSpecs = data['playerSpecs']
        channel = await monitor.getChannel(username, playerSpecs)
        return JsonResponse(await monitor.getChannel(username, playerSpecs), status=200)
    except Exception as e:
        logger.error(e)
        return JsonResponse({'error': str(e)}, status=400)
