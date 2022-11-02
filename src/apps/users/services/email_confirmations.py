from django.core.signing import TimestampSigner, JSONSerializer, BadSignature
from django.core.exceptions import ValidationError

from apps.users.models import User
from apps.common.utils import Singleton
from ..tasks import send_email_address_confirmation


class EmailConfirmations(metaclass=Singleton):
    _salt = 'user.confirmation.token'

    def send_to_user_email_confirmation_token(self, user: User) -> None:
        """
        Отправляет пользователю на email письмо с токеном(с его помощью
        статус пользователя в системе изменяется на подтвержденный)
        """
        email_confirmation_token = \
            self._get_email_confirmation_token_for_user(user)

        send_email_address_confirmation.delay(
            recipient_list=[user.email],
            confirmation_token=email_confirmation_token
        )

    def _get_email_confirmation_token_for_user(self, user: User):
        """ Возвращает токен для подтверждения email аддреса пользователя"""
        return TimestampSigner(
            salt=self._salt).sign_object(
            user.email, JSONSerializer
        )

    def _validate_user_email_confirmation_token(self, user, token: str) -> bool:
        """
        Проверяет полученный от пользователя токен подтверждающий email аддрес
        """
        signer = TimestampSigner(salt=self._salt)

        try:
            email = signer.unsign_object(token)
            assert user.email == email and not user.is_email_confirmed
        except BadSignature:
            raise ValidationError('Email confirmation token is invalid')
        except AssertionError:
            raise ValidationError(
                'Email address is invalid or already confirmed'
            )
        else:
            return True
