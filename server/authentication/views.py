from django.contrib.auth import get_user_model
from django.core.exceptions import BadRequest
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from utils.Response.CustomResponse import CustomResponse as cr

from .serializers import LoginSerializer, RegisterSerializer
from .services import LoginServices as ls
from .services import RegisterServices as rs

# Create your views here.

User = get_user_model()


class RegisterAPIView(APIView):

    serializer_class = RegisterSerializer
    authentication_classes = []

    def post(self, request: Request) -> Response:

        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data["password"] = rs.hash_the_password(
                serializer.validated_data["password"]
            )

            # always storing the email in lowercase
            serializer.validated_data["email"] = serializer.validated_data[
                "email"
            ].lower()
            serializer.save()
            return cr.success(
                message="Successfully created an account.", status_code=HTTP_201_CREATED
            )
        except ValidationError:
            return cr.error(
                data=(serializer.errors),
                message="Validation Error",
                status_code=HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            raise Exception


class LoginAPIView(APIView):

    serializer_class = LoginSerializer
    authentication_classes = []

    def post(self, request: Request) -> Response:
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            if ls.check_the_credentials(serializer.validated_data):
                access_token = ls.generate_the_token(
                    User.objects.get(email=serializer.validated_data["email"].lower())
                )
                return cr.success(
                    message="Login successful",
                    data=access_token,
                    status_code=HTTP_200_OK,
                )

            return cr.error(
                message="Invalidn credentials.",
                data="Please check your email and password properly",
                status_code=HTTP_400_BAD_REQUEST,
            )

        except ValidationError:
            return cr.error(
                data=dict(serializer.errors),
                message="Validation Error",
                status_code=HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return cr.error(message="Error while logging up.")
