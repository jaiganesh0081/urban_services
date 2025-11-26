from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from providers.models import Category
from accounts.permissions import IsProvider
from bookings.models import Booking
from urban_services.utils import standard_message
from .serializer import ProviderProfileSerializer, ProviderSlotSerializer, CategorySerializer
from .swagger_schema import providerprofileschema, availableslotschema


# Create your views here.

class ProviderProfileAPIView(APIView):
    permission_classes = [IsAuthenticated, IsProvider]

    @providerprofileschema
    def post(self, request):
        serializer_class = ProviderProfileSerializer(data=request.data, context={"request": request})
        serializer_class.is_valid(raise_exception=True)
        serializer_class.save()

        return standard_message(
            message="Provider profile successfully created",
            data=serializer_class.data,
            status_code=status.HTTP_201_CREATED
        )


class ProviderSlotAPIView(APIView):
    permission_classes = [IsAuthenticated, IsProvider]

    @availableslotschema
    def post(self, request):
        print(f'requested data is {request.data}')
        serializer_class = ProviderSlotSerializer(data=request.data, context={"request": request})
        serializer_class.is_valid(raise_exception=True)
        serializer_class.save()
        return standard_message(message="Slot availability created", data=serializer_class.data,
                                status_code=status.HTTP_201_CREATED)


class ProviderCategoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Category.objects.prefetch_related("skills")
        serializer_class = CategorySerializer(queryset, many=True)
        return standard_message(message="category list", data=serializer_class.data, status_code=status.HTTP_200_OK)
