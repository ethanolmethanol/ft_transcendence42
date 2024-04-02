from django.db import models
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

class Game(models.Model):
    game_state = models.CharField(max_length=255, default='ongoing')

class PongRoom(models.Model):
    room_id = models.CharField(max_length=255, unique=True)
    max_players = models.IntegerField(default=2)
    game_started = models.BooleanField(default=False)

    def __str__(self):
        return f"Room {self.room_id} (Max Players: {self.max_players})"
    
    def is_full(self):
        is_full = self.players.count() >= self.max_players

class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='players')
    score = models.IntegerField(default=0)
    slot = models.CharField(max_length=1, choices=(('1', 'Player 1'), ('2', 'Player 2')))
    room = models.ForeignKey(PongRoom, related_name='players', on_delete=models.CASCADE)
