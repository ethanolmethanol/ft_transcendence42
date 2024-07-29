from django.db import models
from typing import Any, List

from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

class GameSummary(models.Model):
    arena_id = models.CharField(max_length=255)
    winner = models.JSONField(null=True)
    players = models.JSONField()
    end_time = models.DateTimeField(auto_now=True)

class Profile(models.Model):
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

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, blank=True)
    game_summaries = models.ManyToManyField(GameSummary, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        app_label = 'shared_models'