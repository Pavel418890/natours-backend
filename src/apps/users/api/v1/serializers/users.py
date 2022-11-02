from rest_framework import serializers
from rest_framework_simplejwt.serializers import PasswordField

from . import SignedUser, BaseUserSerializer
from apps.common.validators import FieldsPairEqualityValidator
from apps.users.services.authentication import AuthenticationService
from apps.users.services.users_crud import UserCRUDService
from apps.users.models import User


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

    users_crud = UserCRUDService()

    def validate(self, data: dict[str, int]) -> User:
        user = self.users_crud.get_user_by_id(data.pop('id'))
        return user


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = PasswordField()
    password_confirm = PasswordField()
    token = serializers.DictField(read_only=True)
    user = BaseUserSerializer(read_only=True)

    user_crud_service = UserCRUDService()
    auth_service = AuthenticationService()

    def validate(self, data: dict[str, str]) -> dict[str, str]:
        """
        Проверяет идентичность паролей
        """
        FieldsPairEqualityValidator(
            fields=[('password', 'password_confirm')],
            message='Password do not match'
        )(data)
        return data

    def create(self, validated_data: dict[str, str]) -> SignedUser:
        """
        Вызывает методы создания пользователя и получения токена
        Передает полученую информацию для представления пользователю.
        """
        return self.user_crud_service.create_new_user(validated_data)


class ConfirmUserEmailSerializer(serializers.Serializer):
    email_confirmation_token = serializers.CharField(write_only=True)

    users_crud = UserCRUDService()

    def update(self, user: User, validated_data: dict[str, str]):
        """
        Вызывает метод подтверждения почты пользователя
        """
        email_confirmation_token = \
            validated_data.pop('email_confirmation_token')
        self.users_crud._confirm_user_email(user, email_confirmation_token)
        return {}


class ResetPasswordSerializer(serializers.Serializer):
    new_password = PasswordField()
    new_password_confirm = PasswordField()
    password_reset_token = serializers.CharField(write_only=True)

    users_crud = UserCRUDService()

    def validate(self, data):
        FieldsPairEqualityValidator(
            fields=[('new_password', 'new_password_confirm')],
            message='Password do not match.'
        )(data)
        return data

    def create(self, validated_data: dict[str, str]) -> dict:
        """
        Вызывает обновление пароля согласно полученным данным от пользователя
        (токен сброса пароля, новый пароль)
        """
        token = validated_data.pop('password_reset_token')
        new_password = validated_data.pop('new_password')
        user = self.users_crud._get_user_by_valid_password_reset_token(token)
        self.users_crud._reset_user_password(user, new_password)
        return {}


class UpdateUserEmailSerializer(BaseUserSerializer):
    email = serializers.EmailField()

    def update(self, user: User, validated_data: dict[str, str]) -> User:
        """
        Вызывает метод обновления email адреса пользователя
        Передает получившуюся информацию для представления пользователю
        """
        new_email = validated_data.pop('email')
        updated_user = UserCRUDService().update_user_email_address(
            user, new_email
        )
        return updated_user


class UpdatePasswordSerializer(serializers.Serializer):
    existing_password = PasswordField()
    new_password = PasswordField()

    users_crud = UserCRUDService()

    def update(self, user: User, validated_data: dict[str, str]) -> dict:
        """
        Вызывает метод обновления пароля пользователя
        """
        existing_password = validated_data.pop('existing_password')
        new_password = validated_data.pop('new_password')

        self.users_crud.update_user_password(
            user, existing_password, new_password
        )
        return {}
