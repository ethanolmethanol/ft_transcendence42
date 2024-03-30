from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    game_state = models.CharField(max_length=255, default='ongoing')

class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='players')
    score = models.IntegerField(default=0)
    slot = models.CharField(max_length=1, choices=(('1', 'Player 1'), ('2', 'Player 2')))
