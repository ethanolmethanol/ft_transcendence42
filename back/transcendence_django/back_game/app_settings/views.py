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
        logger.error(data['playerSpecs'])
        return JsonResponse(await monitor.getNewChannel(data['playerSpecs']), status=200)
    except Exception as e:
        logger.error(e)
        return JsonResponse({'error': str(e)}, status=400)
