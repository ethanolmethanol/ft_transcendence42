from typing import Any

from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Profile(models.Model):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)
    color_config: ArrayField[models.CharField] = ArrayField(models.CharField(max_length=20), default=list)

    def save(self, *args: Any, **kwargs: Any) -> None:
        if self.pk is not None:
            orig: Profile = Profile.objects.get(pk=self.pk)  # pylint: disable=no-member
            if orig.user != self.user:
                raise ValueError("User can only update their color configuration.")
        super().save(*args, **kwargs)
