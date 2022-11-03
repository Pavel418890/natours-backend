from typing import TypedDict

from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from ..models import User


class CustomTokenObject(TypedDict):
    token: str
    expires_at: int


class TokenPair(TypedDict):
    access: dict[str, CustomTokenObject]
    refresh: dict[str, CustomTokenObject]


class AuthenticationService:
    """
    Возвращает пользователя согласно переданным реквизитам
    По-умолчанию Django возвращает AnonymousUser(None), если пользователь
    не найден.
    """

    def get_user_by_given_credentials(self, credentials: dict[str, str]) -> User:
        try:

            auth_user = User.objects.select_related("profile").get(
                email=credentials["email"]
            )
            if auth_user.check_password(credentials["password"]):
                auth_user.last_login = timezone.now()
                auth_user.save()

        except AttributeError:
            raise ValidationError(
                {
                    "detail": "You shall not past!(with provided credentials)",
                    "status": HTTP_400_BAD_REQUEST,
                }
            )
        else:
            return auth_user

    @transaction.atomic
    def get_user_with_json_web_token_by_given_credentials(
        self, credentials: dict[str, str]
    ) -> dict[str, User | TokenPair]:
        """
        Возвращает пользователя с токеном
        """
        user = self.get_user_by_given_credentials(credentials)
        token = self.get_json_web_token_for_user(user)
        return {"user": user, "token": token}

    def get_user_from_json_web_token(self, token: RefreshToken) -> TokenPair:
        """Возвращает пользователя если получен валидый JWT токен"""
        return JWTTokenUserAuthentication().get_user(token)

    def get_access_token_by_given_refresh_token(
        self, refresh_token: str
    ) -> dict[str, CustomTokenObject]:
        """
        Возвращает access JWT  со сроком валидности,
        если передан валидный  refresh JWT
        """
        valid_refresh_token = RefreshToken(refresh_token)
        access = valid_refresh_token.access_token
        access_expires_at = access.payload.get("exp")
        return {"access": {"token": str(access), "expires_at": access_expires_at}}

    def get_json_web_token_for_user(self, user: User) -> TokenPair:
        """
        Возвращает для текущего пользователя JWT
        токен со сроком валидности
        """
        jwt = RefreshToken.for_user(user)
        access_token = jwt.access_token
        refresh_token = jwt
        access_expires_at = access_token.payload.get("exp")
        refresh_expires_at = refresh_token.payload.get("exp")

        return {
            "access": {"token": str(access_token), "expires_at": access_expires_at},
            "refresh": {"token": str(refresh_token), "expires_at": refresh_expires_at},
        }


auth = AuthenticationService()
