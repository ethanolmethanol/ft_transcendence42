from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from game.models import Game
from game.game_logic.game_logic import update_game_state
from .serializers import GameSerializer
from django.http import HttpResponse, JsonResponse
from django.db import connections
from django.db.utils import OperationalError
import redis
import requests
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json


def health(request):
    try:
        r = redis.Redis(host='redis', port=6379, db=0)
        r.ping()
    except redis.ConnectionError:
        return HttpResponse("Redis connection failed", status=500, content_type="text/plain")
    return HttpResponse("OK", content_type="text/plain")

def index(request):
    return render(request, "test-wss.html")

def start_game(request):
    game = Game.objects.create(game_state='ongoing')
    return JsonResponse({'game_id': game.id})

def update_game(request, game_id):
    game = Game.object.get(id=game_id)
    user_input = request.POST.get('user_input')
    game = update_game_state(game, user_input)
    return JsonResponse({'game_state': game.game_state})

def get_game_state(request, game_id):
    game = Game.objects.get(id=game_id)
    return JsonResponse({'game_state': game.game_state})

@method_decorator(login_required, name='dispatch')
class GameAPIView(APIView):
    def get(self, request, *args, **kwargs):
        #games = Game.objects.all()
        #serializer = Game.objects.all()
        #serializer = GameSerializer(games, many=True)
        return JsonResponse({'message': 'Game state'})
    
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        return JsonResponse({'message': 'Game state updated'})


##################### Exemple end points: ###########################
#       POST /api/game/start: Start a new game session.             #
#       POST /api/game/move: Update player movements.               #
#       GET /api/game/state: Get the current state of the game.     #
#####################################################################
