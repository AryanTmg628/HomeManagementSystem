import json

from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import ViewSet

from utils.Response.CustomResponse import CustomResponse as cr

from .models import DoorLock
from .serializers import DoorLockSerializer


# Create your views here.
class DoorLockViewSet(ViewSet):
    """
    DoorLockViewset for creating, listing and retrieveing data conceringin doorlock
    """

    query_set = DoorLock.objects.all()
    serializer = DoorLockSerializer

    def create(self, request: Request) -> Response:
        """
        create the door lock account
        """

        try:
            serializer = self.serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return cr.success(
                message="Successfully create door lock account.",
                status_code=HTTP_201_CREATED,
            )

        except ValidationError:
            return cr.error(
                message="Error while fetching the doorlock informations",
                data=serializer.errors,
            )

    def list(self, request: Request) -> Response:
        """
        returns all doorlock informations
        """
        try:
            serializer = self.serializer(
                data=self.query_set, many=True, context={"action": "view"}
            )
            serializer.is_valid()
            return cr.success(
                message="Successfully fetched all doorlock users",
                data=json.loads(json.dumps(serializer.data)),
            )
        except AssertionError as e:
            print(f"Error while fetching door lock :-> {e}")
            return cr.error(message="Error while fetching the doorlock informations")
