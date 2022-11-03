from datetime import datetime
from typing import Optional, TypedDict

from rest_framework import serializers

from apps.users.api.v1.serializers.auth import *
from apps.users.api.v1.serializers.profile import *
from apps.users.api.v1.serializers.users import *
from apps.users.services import TokenPair


class UserProfile(TypedDict):
    first_name: Optional[str]
    last_name: Optional[str]
    photo: str
    id: int


class UserType(TypedDict):
    id: int
    email: str
    is_email_confirmed: bool
    password_changed_at: Optional[datetime]
    role: str
    profile: UserProfile
    last_login: Optional[str]


class SignedUser(TypedDict):
    user: UserType
    token: TokenPair


class BaseUserSerializer(serializers.Serializer):
    """
    класс представления пользователя
    """

    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True)
    role = serializers.CharField(read_only=True)
    profile = ProfileSerializer(read_only=True)
    is_email_confirmed = serializers.CharField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
