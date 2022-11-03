from django.contrib.auth.tokens import PasswordResetTokenGenerator


class ResetTokenException(Exception):
    """Класс обработки исключений при валидации токена сброса пароля"""


class ResetTokenGenerator(PasswordResetTokenGenerator):
    """
    Переопределяет метод класса PasswordResetTokenGenerator
    Вместо False возвращает ошибку валидации токена
    """

    def check_token(self, user, token):
        result = super().check_token(user, token)
        if not result:
            raise ResetTokenException("Received token is invalid or has expired")
        else:
            return True
