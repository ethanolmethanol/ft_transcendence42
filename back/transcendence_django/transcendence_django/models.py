from django.db import models

class GameSummary(models.Model):
    arena_id = models.CharField(max_length=255)
    winner = models.JSONField()
    players = models.JSONField()
    end_time = models.DateTimeField(auto_now=True)

    class Meta:
#         verbose_name_plural = "game summaries"
        app_label = "transcendence_django"
#         db_table = "game_summaries"
