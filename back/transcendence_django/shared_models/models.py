from typing import Any, List, TypeVar
import logging

from asgiref.sync import sync_to_async
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.postgres.fields import ArrayField
from django.db import models
from sortedm2m.fields import SortedManyToManyField

logger = logging.getLogger(__name__)

class GameSummary(models.Model):
    arena_id = models.CharField(max_length=255)  # type: ignore
    winner_user_id = models.JSONField(null=True)
    players = models.JSONField()
    start_time = models.DateTimeField(null=True)  # type: ignore
    end_time = models.DateTimeField(auto_now=True)  # type: ignore
    is_remote = models.BooleanField(default=False)  # type: ignore


class Profile(models.Model):
    color_config: List[str] = ArrayField(
        models.CharField(max_length=20), default=list
    )  # type: ignore
    game_settings: List[int] = ArrayField(
        models.IntegerField(), default=list
    )  # type: ignore

    def save(self, *args: Any, **kwargs: Any) -> None:
        super().save(*args, **kwargs)


CustomUserType = TypeVar("CustomUserType", bound="CustomUser")


class CustomUserManager(BaseUserManager[CustomUserType]):
    def create_user(
        self, username, email, password=None, **extra_fields
    ) -> CustomUserType:
        if not email:
            raise ValueError("The Email field must be set")
        if not username:
            raise ValueError("The Username field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, username, email, password=None, **extra_fields
    ) -> CustomUserType:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)

def get_default_time_played() -> dict[str, int]:
    return {'local': 0, 'remote': 0}

def get_default_win_loss_tie() -> dict[str, int]:
    return {'win': 0, 'loss': 0, 'tie': 0}


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)  # type: ignore
    email = models.EmailField(unique=True)  # type: ignore
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, null=True, blank=True
    )  # type: ignore
    game_summaries = SortedManyToManyField(GameSummary, blank=True)
    time_played: dict[str, int] = models.JSONField(default=get_default_time_played)
    win_loss_tie: dict[str, int] = models.JSONField(default=get_default_win_loss_tie)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # type: ignore

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return str(self.username)

    async def save_game_summary(self, game_summary: GameSummary) -> None:
        await sync_to_async(self.game_summaries.add)(game_summary)
        self.__update_time_played(game_summary)
        if game_summary.is_remote:
            self.__update_win_dict(game_summary)
        await sync_to_async(self.save)()

    def __update_win_dict(self, game_summary) -> None:
        if str(game_summary.winner_user_id) == str(self.id):
            key = 'win'
        elif game_summary.winner_user_id is None:
            key = 'tie'
        else:
            key = 'loss'
        self.win_loss_tie[key] += 1

    def __update_time_played(self, game_summary) -> None:
        game_duration: int = int((game_summary.end_time - game_summary.start_time).total_seconds())
        if game_summary.is_remote:
            self.time_played['remote'] += game_duration
        else:
            self.time_played['local'] += game_duration
