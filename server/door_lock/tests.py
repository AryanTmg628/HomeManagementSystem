from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

# Create your tests here.


class DoorLockTest(APITestCase):

    client = APIClient

    def test_door_lock_creation(self):
        """
        Ensure we can create the doorlock account
        """

        url = reverse("door-lock-list")
        data = {
            "first_name": "Test",
            "last_name": "Test",
            "rfid": "testid1234",
            "password": 0000,
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["success"], True)

    def test_door_lock_list(self):
        """
        Ensure we can list all the doorlock account details
        """

        url = reverse("door-lock-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["success"], True)
