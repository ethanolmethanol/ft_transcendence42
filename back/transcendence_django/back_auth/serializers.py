import json
import os

from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from shared_models.models import CustomUser

# Load validation rules
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
validation_rules_path = os.path.join(base_dir, "shared_models", "validation-rules.json")

with open(validation_rules_path) as f:
    validation_rules = json.load(f)


class UserSerializer(serializers.ModelSerializer[CustomUser]):
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=CustomUser.objects.all(),
                message="This email is already in use. Please choose another one.",
            ),
            RegexValidator(
                regex=validation_rules["email"]["pattern"],
                message="Invalid email format.",
            ),
        ]
    )
    username = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=CustomUser.objects.all(),
                message="This username is already in use. Please choose another one.",
            ),
            RegexValidator(
                regex=validation_rules["username"]["pattern"],
                message="Invalid username format.",
            ),
        ]
    )
    password = serializers.CharField(
        write_only=True,
        validators=[
            RegexValidator(
                regex=f".{{{validation_rules['password']['minLength']},}}",
                message=f"Password must be at least {validation_rules['password']['minLength']} characters long.",
            )
        ],
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password")

    def create(self, validated_data: dict[str, str]) -> CustomUser:
        user = CustomUser.objects.create_user(**validated_data)
        return user
