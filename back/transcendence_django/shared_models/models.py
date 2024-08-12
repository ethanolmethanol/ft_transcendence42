import logging
from datetime import datetime, timedelta
from typing import Any, List, TypeVar

import requests
from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from shared_models.constants import (
    DEFAULT_GAME_COUNTER,
    DEFAULT_TIME_PLAYED,
    DEFAULT_WIN_LOSS_TIE,
)
from sortedm2m.fields import SortedManyToManyField
from transcendence_django.dict_keys import LOCAL, LOSS, REMOTE, TIE, TOTAL, WIN

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


class OauthToken(models.Model):
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    token_expires_at = models.DateTimeField(default=timezone.now)

    def store_tokens(self, token_data):
        self.access_token = token_data["access_token"]
        self.refresh_token = token_data["refresh_token"]
        self.token_expires_at = (
            timezone.now()
            + timedelta(seconds=token_data["expires_in"])
            - timedelta(minutes=5)
        )
        self.save()

    def is_token_expired(self) -> bool:
        return timezone.now() > self.token_expires_at

    def refresh_tokens(self) -> str:
        if not self.is_token_expired():
            logger.info("Access token is still valid, no need to refresh.")
            return self.access_token

        data = {
            "grant_type": "refresh_token",
            "client_id": settings.OAUTH_CLIENT_UID,
            "client_secret": settings.OAUTH_CLIENT_SECRET,
            "refresh_token": self.refresh_token,
        }

        try:
            token_response = requests.post(
                settings.OAUTH_TOKEN_URL, data=data, timeout=5
            )
            token_response.raise_for_status()
            self.store_tokens(token_response.json())
        except requests.exceptions.RequestException as e:
            logger.error(e)
        return self.access_token


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


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)  # type: ignore
    username = models.CharField(max_length=150, unique=True)  # type: ignore
    login42 = models.CharField(max_length=150, unique=True)  # type: ignore
    email = models.EmailField(unique=True)  # type: ignore
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, null=True, blank=True
    )  # type: ignore
    oauth_token = models.OneToOneField(
        OauthToken, on_delete=models.CASCADE, null=True, blank=True
    )  # type: ignore
    game_summaries = SortedManyToManyField(GameSummary, blank=True)
    time_played = models.JSONField(default=DEFAULT_TIME_PLAYED)
    win_loss_tie = models.JSONField(default=DEFAULT_WIN_LOSS_TIE)
    game_counter = models.JSONField(default=DEFAULT_GAME_COUNTER)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # type: ignore

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return str(self.username)

    def store_tokens(self, token_data):
        if self.oauth_token is None:
            # pylint: disable=no-member
            self.oauth_token = OauthToken.objects.create()
        self.oauth_token.store_tokens(token_data)
        self.save()

    def clear_tokens(self):
        if self.oauth_token is not None:
            self.oauth_token = None
        self.save()

    async def save_game_summary(self, game_summary: GameSummary) -> None:
        await sync_to_async(self.game_summaries.add)(game_summary)
        self.__update_time_played(game_summary)
        self.__update_count(game_summary)
        if game_summary.is_remote:
            self.__update_win_dict(game_summary)
        await sync_to_async(self.save)()

    def __update_win_dict(self, game_summary) -> None:
        if str(game_summary.winner_user_id) == str(self.id):
            key = WIN
        elif game_summary.winner_user_id is None:
            key = TIE
        else:
            key = LOSS
        self.win_loss_tie[key] += 1
        self.win_loss_tie[TOTAL] += 1

    def __update_time_played(self, game_summary) -> None:
        start_time = game_summary.start_time or datetime.min
        end_time = game_summary.end_time or datetime.max
        game_duration: int = int((end_time - start_time).total_seconds())
        if game_summary.is_remote:
            self.time_played[REMOTE] += game_duration
        else:
            self.time_played[LOCAL] += game_duration
        self.time_played[TOTAL] += game_duration

    def __update_count(self, game_summary) -> None:
        if game_summary.is_remote:
            self.game_counter[REMOTE] += 1
        else:
            self.game_counter[LOCAL] += 1
        self.game_counter[TOTAL] += 1
