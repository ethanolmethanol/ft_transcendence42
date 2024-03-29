from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    ball_position = models.JSONField()
    ball_velocity = models.JSONField()
    paddle_positions = models.JSONField()
    game_state = models.CharField(max_length=255)

    def update(self):
        # update the game state
        raise ValueError("Game.update() not implemented yet.")

class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    paddle_position = models.JSONField()
    side = models.CharField(max_length=255)
