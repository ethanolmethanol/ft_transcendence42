from typing import Any, List, TypeVar

from asgiref.sync import sync_to_async
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.postgres.fields import ArrayField
from django.db import models
from sortedm2m.fields import SortedManyToManyField


class GameSummary(models.Model):
    arena_id = models.CharField(max_length=255)  # type: ignore
    winner = models.JSONField(null=True)
    players = models.JSONField()
    end_time = models.DateTimeField(auto_now=True)  # type: ignore


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


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)  # type: ignore
    email = models.EmailField(unique=True)  # type: ignore
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, null=True, blank=True
    )  # type: ignore
    game_summaries = SortedManyToManyField(GameSummary, blank=True)
    history_size = models.IntegerField(default=0)  # type: ignore

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # type: ignore

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return str(self.username)

    async def save_game_summary(self, game_summary: GameSummary) -> None:
        user_game_summaries = await sync_to_async(list)(self.game_summaries.all())
        await sync_to_async(self.game_summaries.set)(
            [game_summary] + user_game_summaries
        )
        self.history_size += 1
        await sync_to_async(self.save)()
