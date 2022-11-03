from rest_framework import serializers
from rest_framework_simplejwt.serializers import PasswordField

from apps.common.validators import FieldsPairEqualityValidator
from apps.users import services
from apps.users.models import User

from . import BaseUserSerializer, SignedUser

__all__ = [
    "GetAllUsersSerializer",
    "GetUserByIdSerializer",
    "UpdatePasswordSerializer",
    "ConfirmUserEmailSerializer",
    "ResetPasswordSerializer",
    "SignUpSerializer",
    "UpdateUserEmailSerializer",
]


class GetAllUsersSerializer(BaseUserSerializer):
    """
    Класс представления всех пользователей для администратора
    """


class GetUserByIdSerializer(BaseUserSerializer):
    id = serializers.IntegerField()
    password_reset_token = serializers.CharField(required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    password_changed_at = serializers.DateTimeField(required=False)

    def validate(self, data: dict[str, int]) -> User:
        user = services.user.get_user_by_id(data.pop("id"))
        return user


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = PasswordField()
    password_confirm = PasswordField()
    token = serializers.DictField(read_only=True)
    user = BaseUserSerializer(read_only=True)

    def validate(self, data: dict[str, str]) -> dict[str, str]:
        """
        Проверяет идентичность паролей
        """
        FieldsPairEqualityValidator(
            fields=[("password", "password_confirm")], message="Password do not match"
        )(data)
        return data

    def create(self, validated_data: dict[str, str]) -> SignedUser:
        """
        Вызывает методы создания пользователя и получения токена
        Передает полученую информацию для представления пользователю.
        """
        return services.user.create_new_user(validated_data)


class ConfirmUserEmailSerializer(serializers.Serializer):
    email_confirmation_token = serializers.CharField(write_only=True)

    def update(self, user: User, validated_data: dict[str, str]) -> User:
        """
        Вызывает метод подтверждения почты пользователя
        """
        email_confirmation_token = validated_data.pop("email_confirmation_token")
        return services.user.confirm_user_email(user, email_confirmation_token)


class ResetPasswordSerializer(serializers.Serializer):
    new_password = PasswordField()
    new_password_confirm = PasswordField()
    password_reset_token = serializers.CharField(write_only=True)

    def validate(self, data):
        FieldsPairEqualityValidator(
            fields=[("new_password", "new_password_confirm")],
            message="Password do not match.",
        )(data)
        return data

    def create(self, validated_data: dict[str, str]) -> User:
        """
        Вызывает обновление пароля согласно полученным данным от пользователя
        (токен сброса пароля, новый пароль)
        """
        token = validated_data.pop("password_reset_token")
        new_password = validated_data.pop("new_password")
        user = services.user.get_user_by_valid_password_reset_token(token)
        updated_user = services.user.reset_user_password(user, new_password)
        return updated_user


class UpdateUserEmailSerializer(BaseUserSerializer):
    email = serializers.EmailField()

    def update(self, user: User, validated_data: dict[str, str]) -> User:
        """
        Вызывает метод обновления email адреса пользователя
        Передает получившуюся информацию для представления пользователю
        """
        new_email = validated_data.pop("email")
        return services.user.update_user_email_address(user, new_email)


class UpdatePasswordSerializer(serializers.Serializer):
    existing_password = PasswordField()
    new_password = PasswordField()

    def update(self, user: User, validated_data: dict[str, str]) -> User:
        """
        Вызывает метод обновления пароля пользователя
        """
        existing_password = validated_data.pop("existing_password")
        new_password = validated_data.pop("new_password")

        return services.user.update_user_password(user, existing_password, new_password)
