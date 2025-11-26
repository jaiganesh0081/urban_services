from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from accounts.permissions import IsCustomer
from providers.models import ProviderProfile, Availabilty
from urban_services.utils import standard_message
from .serializer import ProviderAvailableSerializer
from .swagger_schema import provideravailableschema


# Create your views here.


class ProviderAvailableAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    @provideravailableschema
    def get(self, request):
        provider_id = request.query_params.get("provider_id")
        if not provider_id:
            return standard_message("provider_id is required", status_code=400)
        try:
            provider = ProviderProfile.objects.get(id=provider_id)
        except ProviderProfile.DoesNotExist:
            return standard_message("Provider not found", status_code=404)
        provider_available = Availabilty.objects.filter(provider=provider)
        serializer_class = ProviderAvailableSerializer(provider_available, many=True)
        return standard_message(message="Provider availablity datas", data=serializer_class.data,
                                status_code=status.HTTP_200_OK)
