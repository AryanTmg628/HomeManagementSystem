from datetime import datetime, timedelta
from typing import Any

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ObjectDoesNotExist

from .authentication import JWTAuthentication as jwt

login_credentials = {
    "email": "",
    "password": "",
}

User = get_user_model()


class RegisterServices:

    @staticmethod
    def hash_the_password(password: str) -> str:
        return make_password(password=password)


class LoginServices:

    @staticmethod
    def check_the_credentials(data: login_credentials) -> bool:

        try:
            user = User.objects.get(email=data["email"].lower())
            return check_password(data["password"], user.password)
        except ObjectDoesNotExist:
            return False
        except Exception:
            return False

    @staticmethod
    def generate_the_token(user: User) -> str:

        expiration_date = int(
            (
                datetime.now()
                + timedelta(days=settings.JWT_CONF["ACCESS_TOKEN_EXPIRATION"])
            ).timestamp()
        )
        payload = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "username": user.username,
            "is_superuser": user.is_superuser,
            "exp": expiration_date,
            "iat": datetime.now().timestamp(),
        }

        return jwt.create_token(payload)
