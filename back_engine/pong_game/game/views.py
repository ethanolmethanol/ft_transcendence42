from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Game
from .serializers import GameSerializer
from django.http import HttpResponse
from django.db import connections
from django.db.utils import OperationalError
import redis
import requests

def health(request):
    # Redis check
    try:
        r = redis.Redis(host='redis', port=6379, db=0)
        r.ping()
    except redis.ConnectionError:
        return HttpResponse("Redis connection failed", status=500, content_type="text/plain")
    # External API check (example)
    # try:
    #     response = requests.get('https://api.example.com/health', timeout=5)  # Use the actual URL and proper timeout
    #     if response.status_code != 200:
    #         return HttpResponse("External API check failed", status=500, content_type="text/plain")
    # except requests.exceptions.RequestException:
    #     return HttpResponse("External API check failed", status=500, content_type="text/plain")
    return HttpResponse("OK", content_type="text/plain")

def index(request):
    return render(request, "test-wss.html")

class GameAPIView(APIView):
    def get(self, request):
        games = Game.objects.all()
        serializer = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)


##################### Exemple end points: ###########################
#       POST /api/game/start: Start a new game session.             #
#       POST /api/game/move: Update player movements.               #
#       GET /api/game/state: Get the current state of the game.     #
#####################################################################
