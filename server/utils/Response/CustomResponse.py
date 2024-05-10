from rest_framework import status
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


class CustomResponse:
    """
    Custom Response to maintain the integrity in every responses of this application
    Response can either be success or error

    """

    @staticmethod
    def success(data="", message="Successfull", status_code=HTTP_200_OK):
        """
        Returns success response in json with data, message and status_code
        """

        return Response(
            {
                "success": True,
                "data": data,
                "message": message,
            },
            status=status_code,
        )

    @staticmethod
    def error(data="", message="Unsuccessfull", status_code=HTTP_400_BAD_REQUEST):
        """
        Returns error response in json with data, message and status_code
        """

        return Response(
            {
                "success": False,
                "data": data,
                "message": message,
            },
            status=status_code,
        )
