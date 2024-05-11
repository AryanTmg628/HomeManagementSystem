import json

from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from utils.Response.CustomResponse import CustomResponse as cr

from .models import DoorLock
from .serializers import DoorLockSerializer


# Create your views here.
class DoorLockViewSet(ViewSet):
    """
    DoorLockViewset for creating, listing and retrieveing data conceringin doorlock
    """

    serailizer = DoorLockSerializer

    def create(self, request: Request) -> Response:
        pass

    def list(self, request: Request) -> Response:
        """
        returns all doorlock informations
        """
        try:
            query_set = DoorLock.objects.all()
            serializer = self.serailizer(
                data=query_set, many=True, context={"action": "view"}
            )
            serializer.is_valid()
            return cr.success(
                message="Successfully fetched all doorlock users",
                data=json.loads(json.dumps(serializer.data)),
            )
        except AssertionError as e:
            print(f"Error while fetching door lock :-> {e}")
            return cr.error(message="Error while fetching the doorlock informations")

    def retrieve(self, request: Request) -> Response:
        pass
