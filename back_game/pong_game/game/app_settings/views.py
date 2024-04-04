import json
import redis
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import connections, IntegrityError
from django.db.utils import OperationalError
from django.db.models import Count, F
from game.models import PongRoom, Player, Game
from django.views.decorators.csrf import csrf_exempt
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

@require_http_methods(["GET"])
def list_rooms(request):
    rooms = PongRoom.objects.filter(game_started=False)
    if not rooms.exists():
        return JsonResponse([], safe=False)
    rooms_data = [{
        'id': room.id,
        'room_id': room.room_id,
        'max_players': room.max_players,
        'is_full': room.is_full(),
    } for room in rooms if not room.is_full()]
    return JsonResponse(rooms_data, safe=False)

@csrf_exempt
@require_http_methods(["POST"])
def create_room(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        room_id = data.get('room_id')
        max_players = data.get('max_players')

        if not room_id:
            return JsonResponse({'error': 'Room ID must be provided.'}, status=400)

        room, created = PongRoom.objects.get_or_create(
            room_id = room_id,
            defaults = {'max_players': max_players, 'game_started': False})
        if created:
            return JsonResponse({'message': f'Room {room.room_id} created successfully.', 'room_id': room.room_id}, status=201)
        else:
            return JsonResponse({'error': 'Room already exists.'}, status=400)
    except IntegrityError as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_http_methods(["GET"])
def check_room_exists(request, room_id):
    exists = PongRoom.objects.filter(room_id=room_id).exists()
    if exists:
        return JsonResponse({'message': 'Room exists.', 'room_id': room_id}, status=200)
    else:
        return JsonResponse({'error': 'Room does not exist.'}, status=404)