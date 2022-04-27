from django.utils import timezone
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import transaction

from apps.common.utils import ResetTokenGenerator, Singleton
from .authentication import AuthenticationService, TokenPair
from .email_confirmations import EmailConfirmations
from ..models import Profile, User
from ..tasks import send_reset_password


class UserCRUDService(metaclass=Singleton):
    user_manager = User.objects
    auth_service = AuthenticationService()
    email_confirmations = EmailConfirmations()
    _reset_token_generator = ResetTokenGenerator()

    @transaction.atomic
    def create_new_user(
            self,
            validated_data: dict[str, str]
    ) -> dict[str, User | TokenPair]:
        """
        Создает нового пользователя.
        Возвращает нового пользователя с json web token
        """
        received_email = validated_data.pop('email')
        received_password = validated_data.pop('password')
        email = self.user_manager.normalize_email(received_email)
        new_user = self.user_manager.model(email=email)
        new_user.set_password(received_password)
        new_user.save()

        # Для каждого нового пользователя создается Profile модель
        Profile.objects.create(user=new_user)

        # Получает токен для подтверждения email адреса и отправляет на почту
        self.email_confirmations.send_to_user_email_confirmation_token(new_user)

        # Выдача токена для нового пользователя
        json_web_token = self.auth_service.get_json_web_token_for_user(new_user)

        return {'user': new_user, 'token': json_web_token}

    @transaction.atomic
    def update_user_email_address(
            self, user: User, new_email_address: str
    ) -> User:
        """
        Обновляет email адресс пользователя
        Отправляет на почту письмо подтверждения нового email адреса
        """

        validate_email(new_email_address)
        user.email = self.user_manager.normalize_email(new_email_address)
        user.is_email_confirmed = False
        user.save()

        self.email_confirmations.send_to_user_email_confirmation_token(user)
        return user

    @transaction.atomic
    def set_password_reset_token_by_given_email(self, email: str) -> None:
        """
        Создает токен для сборса пароля и отправляет на почту пользователю
        """

        user = self.user_manager.get(email=email)
        token = self._reset_token_generator.make_token(user)
        user.password_reset_token = token
        send_reset_password.delay(recipient_list=[user.email],
                                  reset_token=token)
        user.save()

    @transaction.atomic
    def update_user_password(
            self, user: User, existing_password: str, new_password: str
    ) -> None:
        """
        Обновляет пароль пользователя, если старый пароль валидный и
        новый пароль не является дубликатом старого пароля
        """
        message = None
        try:
            message = 'Your old and new password are the same. '
            assert existing_password != new_password
            message = 'Your password is invalid.'
            assert user.check_password(existing_password)
        except AssertionError:
            raise ValidationError(message)
        else:
            self._reset_user_password(user, new_password)

    @transaction.atomic
    def pseudo_delete_user(self, user: User) -> None:
        """
        Присваивает пользователю статус - Неактивый
        Обнуляет пароль для исключения возможности
        входа под данной учетной записью
        """
        user.is_active = False
        user.set_unusable_password()
        user.save()

    def get_all_users(self, active_only: bool = True) -> tuple[list[User], int]:
        """
        Возвращает данные и количество всех активных пользователей
        Если параметр-флаг выставлен False возвращает количество и данные
        всех пользоватей
        """
        users = self.user_manager.select_related('profile')
        if active_only:
            filtered_users = users.filter(is_active=True)
            return filtered_users, filtered_users.count()
        return users, users.count()

    def get_user_by_id(self, id: int) -> User:
        """
        Возвращает объект пользователя согласно полученному индентификатору
        """
        return self.user_manager.select_related('profile').get(id=id)

    def get_user_by_email(self, email: str) -> User:
        """
        Возвращает объект пользователя согласно полученому email адресу
        """
        return self.user_manager.select_related('profile').get(email=email)

    def _get_user_by_valid_password_reset_token(self, token: str) -> User:
        """
        Возвращает пользователя,если передан валидный токен для сброса пароля
        (срок действия токена 10 минут)
        """
        user = self.user_manager.select_related(
            'profile'
        ).get(password_reset_token=token)
        self._reset_token_generator.check_token(user, token)
        return user

    def _reset_user_password(self, user: User, password: str) -> None:
        """ Обновляет пароль пользователя, изменяет время его обновления """
        user.set_password(password)
        user.password_reset_token = None
        user.password_changed_at = timezone.now()
        user.save()

    def _confirm_user_email(self, user: User, token: str) -> None:
        """
        Меняет статус подтверждения email адреса на положительный
        """
        self.email_confirmations._validate_user_email_confirmation_token(
            user, token
        )
        user.is_email_confirmed = True
        user.save()
