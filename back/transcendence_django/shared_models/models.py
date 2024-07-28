from django.db import models
from typing import Any, List

from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

class GameSummary(models.Model):
    arena_id = models.CharField(max_length=255)
    winner = models.JSONField(null=True)
    players = models.JSONField()
    end_time = models.DateTimeField(auto_now=True)

    # class Meta:
#         verbose_name_plural = "game summaries"
        # app_label = "transcendence_django"
#         db_table = "game_summaries"

class Profile(models.Model):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)  # type: ignore
    color_config: List[str] = ArrayField(
        models.CharField(max_length=20), default=list
    )  # type: ignore
    game_settings: List[int] = ArrayField(
        models.IntegerField(), default=list
    )  # type: ignore

    def save(self, *args: Any, **kwargs: Any) -> None:
        if self.pk is not None:
            orig: Profile = Profile.objects.get(pk=self.pk)  # pylint: disable=no-member
            if orig.user != self.user:
                raise ValueError("User can only update their color configuration.")
        super().save(*args, **kwargs)

    # class Meta:
        # app_label = "sh"
