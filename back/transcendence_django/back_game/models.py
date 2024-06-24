from django.db import models

class GameSummary(models.Model):
    channel_id = models.CharField(max_length=255)
    arena_id = models.CharField(max_length=255)
    winner = models.CharField(max_length=255)
    players = models.JSONField()
    end_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "game summaries"
