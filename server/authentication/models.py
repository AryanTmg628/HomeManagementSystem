from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    """
    User entity fields
    """

    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.email
