from django.db import models

# This model represent a game instance
# ball position
# velocity
# paddle's position
# game state (ongoing, paused, ended)

class Game(models.Model):
    #player1_score = models.IntegerField(default=0)
    #player2_score = models.IntegerField(default=0)
    ball_position = models.JSONField()
    ball_velocity = models.JSONField()
    paddle_positions = models.JSONField()
    game_state = models.JSONField()
