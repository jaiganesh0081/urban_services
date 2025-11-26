from rest_framework import status
from rest_framework.response import Response


def standard_message(message, data=None, errors=None, status_code=status.HTTP_200_OK):
    response = {
        "success": True if status_code < 400 else False,
        "message": message
    }
    if data is not None:
        response['data'] = data
    if errors is not None:
        response['errors'] = errors

    return Response(response, status=status_code)
