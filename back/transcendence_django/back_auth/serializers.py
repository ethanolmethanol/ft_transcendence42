from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from shared_models.models import CustomUser


class UserSerializer(serializers.ModelSerializer[CustomUser]):
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=CustomUser.objects.all(),
                message="This email is already in use. Please choose another one.",
            )
        ]
    )
    username = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data: dict[str, str]) -> CustomUser:
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def validate_username(self, value: str) -> str:
        if self.instance is None and CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "This username is already in use. Please choose another one."
            )
        return value

