# from django.db import models

# # Create your models here.
# class User(models.Model):
#     username = models.CharField(max_length=100)
#     password = models.CharField(max_length=100)

# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# from django.db import models

# class CustomUserManager(BaseUserManager):
#     def get_by_natural_key(self, username):
#         return self.get(**{self.model.USERNAME_FIELD: username})

# class User(AbstractBaseUser):
#     objects = CustomUserManager()
#     last_login = models.DateTimeField(auto_now_add=True)
#     username = models.CharField(max_length=100, unique=True)
#     password = models.CharField(max_length=100)

#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = []

#     def __str__(self):
#         return self.username