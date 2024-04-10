import json
from django.http import  JsonResponse
from django.views.decorators.http import require_http_methods
from ..monitor.monitor import Monitor
import logging

logger = logging.getLogger(__name__)

@require_http_methods(["POST"])
def join(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        logger.error(data['gameData'])
        monitor = Monitor(data['gameData'])
        return JsonResponse(monitor.getGameConfig(), status=200)
    except Exception as e:
        logger.error(e)
        return JsonResponse({'error': str(e)}, status=400)
