from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

# Create your tests here.


class AuthenticationTest(APITestCase):

    client = APIClient

    def test_create_account(self):
        url = reverse("user-register")
        data = {
            "first_name": "test",
            "last_name": "test",
            "email": "test@gmail.com",
            "password": "test",
            "username": "test",
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_account(self):
        url = reverse("user-login")
        data = {"email": "test@gmail.com", "password": "test"}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
