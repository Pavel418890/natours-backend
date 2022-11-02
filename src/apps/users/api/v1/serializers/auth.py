from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    PasswordField,
    TokenRefreshSerializer
)


from . import UserType, BaseUserSerializer
from apps.users.services.authentication import (
    AuthenticationService,
    CustomTokenObject,
)
from apps.users.services.users_crud import UserCRUDService


class SignInSerializer(serializers.Serializer):
    token = serializers.DictField(read_only=True)
    email = serializers.EmailField(write_only=True)
    password = PasswordField()
    user = BaseUserSerializer(read_only=True)

    auth_service = AuthenticationService()

    def create(self, validated_data: dict[str, str]) -> UserType:
        """
        Выполняет процесс аутентификации и возвращает объект пользователя
        для дальнейшего получения в контроллере
        """
        auth_user_with_json_web_token = self.auth_service. \
            get_user_with_json_web_token_by_given_credentials(validated_data)

        return auth_user_with_json_web_token


class RefreshJWTSerializer(TokenRefreshSerializer):
    def validate(
            self, request_data: dict[str, str]
    ) -> dict[str, CustomTokenObject]:
        """
        Возвращает access токен
        """
        return AuthenticationService().get_access_token_by_given_refresh_token(
            request_data['refresh']
        )


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    users_crud = UserCRUDService()

    def create(self, validated_data: dict[str, str]) -> dict:
        """
        Отправляет запрос сброса пароля пользователя 
        """
        email = validated_data.pop('email')
        self.users_crud.set_password_reset_token_by_given_email(email)
        return {}
