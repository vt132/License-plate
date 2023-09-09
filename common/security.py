from common.exceptions import (
    InvalidEmailOrPasswordException,
    InvalidCredentialsException
)
from datetime import datetime, timedelta

from fastapi import Request
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer

from django.conf import settings
from passlib.handlers.django import django_pbkdf2_sha256

from jose import jwt

from django.contrib.auth import get_user_model

User = get_user_model()


def create_access_token_response(data, expires_delta=None):
    """Return a HTTP response with jwt token and expiriation time (in utc)."""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            seconds=settings.JWT_EXPIRATION_MINUTES,
        )
    data.update({"exp": expire})
    return {
        "access_token": jwt.encode(
            data, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        ),
        "exp": expire,
    }


def verify_password(plain_password, hashed_password):
    """Check if password is match."""
    return django_pbkdf2_sha256.verify(plain_password, hashed_password)


class AuthAPI:
    """Class for user authentication API."""
    @classmethod
    async def login(
        cls, request: Request, form_data: OAuth2PasswordRequestForm
    ) -> dict[str, str]:
        credentials = {"username": form_data.username,
                       "password": form_data.password}
        if all(credentials.values()):
            user = await cls()._authenticate_user(**credentials)
        else:
            raise InvalidCredentialsException()
        return create_access_token_response({"sub": str(user.uuid)})

    async def _authenticate_user(self, username: str, password: str) -> User:
        user = await User.objects.filter(username=username).afirst()
        if not user:
            raise InvalidEmailOrPasswordException()
        if not verify_password(password, user.password) or not user.is_active:
            raise InvalidEmailOrPasswordException()
        return user


reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)
