from rest_framework import serializers
from rest_framework_simplejwt.serializers import PasswordField, TokenRefreshSerializer

from apps.users import services
from apps.users.api.v1.serializers.users import BaseUserSerializer

from . import UserType


class SignInSerializer(serializers.Serializer):
    token = serializers.DictField(read_only=True)
    email = serializers.EmailField(write_only=True)
    password = PasswordField()
    user = BaseUserSerializer(read_only=True)

    def create(self, validated_data: dict[str, str]) -> UserType:
        """
        Выполняет процесс аутентификации и возвращает объект пользователя
        для дальнейшего получения в контроллере
        """
        return services.auth.get_user_with_json_web_token_by_given_credentials(
            validated_data
        )


class RefreshJWTSerializer(TokenRefreshSerializer):
    def validate(
        self, request_data: dict[str, str]
    ) -> dict[str, services.CustomTokenObject]:
        """
        Возвращает access токен
        """
        return services.auth.get_access_token_by_given_refresh_token(
            request_data["refresh"]
        )


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)

    def create(self, validated_data: dict[str, str]) -> dict:
        """
        Отправляет запрос сброса пароля пользователя
        """
        email = validated_data.pop("email")
        services.user.set_password_reset_token_by_given_email(email)
        return {}
