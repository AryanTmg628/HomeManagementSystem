from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (
    CharField,
    EmailField,
    ModelSerializer,
    Serializer,
)

User = get_user_model()


class LoginSerializer(Serializer):
    email = EmailField()
    password = CharField(max_length=40)

    def validate(self, data):
        if "email" not in data:
            raise ValidationError("Email is required while logging in.")
        if "password" not in data:
            raise ValidationError("Password is required while logging in.")

        return data


class RegisterSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        ]

    def validate(self, data):
        if "first_name" not in data:
            raise ValidationError({"first_name": "First name is required."})
        if "last_name" not in data:
            raise ValidationError({"last_name": "Last name is required."})
        if "email" not in data:
            raise ValidationError({"email": "Email is required."})
        if "password" not in data:
            raise ValidationError({"password": "Password is required."})

        return data
