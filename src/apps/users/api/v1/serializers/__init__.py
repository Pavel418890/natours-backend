from datetime import datetime
from typing import Optional, TypedDict

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
