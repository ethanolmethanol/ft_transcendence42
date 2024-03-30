import json
import redis
from django.http import HttpResponse
from django.db import connections
from django.db.utils import OperationalError

def health(request):
    try:
        r = redis.Redis(host='redis', port=6379, db=0)
        r.ping()
        db_conn = connections['default']
        db_conn.cursor()
    except (redis.ConnectionError, OperationalError):
        return HttpResponse("Service Unhealthy", status=500, content_type="text/plain")
    return HttpResponse("OK", content_type="text/plain")
