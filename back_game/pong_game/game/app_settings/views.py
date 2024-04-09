import json
import redis
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import connections
from django.db.utils import OperationalError
from game.monitor.monitor import Monitor
# from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)

def health(request):
    try:
        r = redis.Redis(host='redis', port=6379, db=0)
        r.ping()
        db_conn = connections['default']
        db_conn.cursor()
    except (redis.ConnectionError, OperationalError):
        return HttpResponse("Service Unhealthy", status=500, content_type="text/plain")
    return HttpResponse("OK", content_type="text/plain")


@require_http_methods(["POST"])
def join(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        monitor = Monitor(data['game_data'])
        return JsonResponse(monitor.game_config, status=200)
    except Exception as e:
        logger.error(e)
        return JsonResponse({'error': str(e)}, status=400)
