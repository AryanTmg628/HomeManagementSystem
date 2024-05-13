from typing import Any

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request

User = get_user_model()


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request: Request) -> tuple[User, dict[str:Any]] | None:
        access_token = self.get_token(request)
        if not access_token:
            return None
        try:
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms="HS256")
            user = User.objects.get(email=payload["email"].lower())

        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed("Invalid access token")
        except User.DoesNotExist:
            raise AuthenticationFailed("User doesn't exists.")

        return user, payload

    def get_token(self, request: Request) -> str | None:

        try:
            token = request.headers["Authorization"]

            token_type, access_token = token.split()

            if token_type.lower() != "bearer":
                raise AuthenticationFailed(
                    "Bearer token authentication should be used."
                )

            return access_token
        except KeyError:
            raise AuthenticationFailed("Authorization is not provided.")
        except ValueError:
            raise AuthenticationFailed("Bearer is not provided.")

    @staticmethod
    def create_token(payload: dict[str:Any]) -> str:

        access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        return access_token
