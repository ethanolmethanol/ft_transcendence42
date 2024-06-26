from django.contrib.auth.models import User
from django.db import models
from django.contrib.postgres.fields import ArrayField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    color_config = ArrayField(models.CharField(max_length=20), default=list)

    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = Profile.objects.get(pk=self.pk)
            if orig.user != self.user:
                raise ValueError("User can only update their color configuration.")
        super().save(*args, **kwargs)