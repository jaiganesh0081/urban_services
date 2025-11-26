from rest_framework import status
from rest_framework.views import APIView

from .serializer import RegisterSerializer
from .swagger_schema import registerswaggerschema
from urban_services.utils import standard_message


# Create your views here.

class RegisterAPIView(APIView):
    @registerswaggerschema
    def post(self, request):
        serializer_class = RegisterSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return standard_message(message="User successfully Registered", status_code=status.HTTP_201_CREATED)
        return standard_message(message="User is not registered", errors=serializer_class.errors,
                                status_code=status.HTTP_400_BAD_REQUEST)
