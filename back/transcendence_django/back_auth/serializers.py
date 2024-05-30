# from .models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer[AbstractUser]):
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=get_user_model().objects.all(),
                message="This email is already in use. Please choose another one.",
            )
        ]
    )

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data: dict[str, str]) -> AbstractUser:
        user = get_user_model().objects.create_user(**validated_data)
        return user
