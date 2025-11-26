from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from accounts.permissions import IsCustomer, IsProvider
from urban_services.utils import standard_message
from .serializer import BookingServicesSerializer
from .swagger_schema import bookingcreateschema, bookingupdateschema
from .models import Booking
from .serializer import ProviderBookingSerializer


# Create your views here.

class BookingServicesAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    @bookingcreateschema
    def post(self, request):
        print('lets start')
        serializer_class = BookingServicesSerializer(data=request.data, context={"request": request})
        serializer_class.is_valid(raise_exception=True)
        serializer_class.save()

        return standard_message(message="Booking successfully created", data=serializer_class.data,
                                status_code=status.HTTP_201_CREATED)


class ProviderBookingAPIView(APIView):
    permission_classes = [IsAuthenticated, IsProvider]

    def get(self, request):
        provider = request.user.provider_profile
        queryset = Booking.objects.select_related(
            "customer", "service"
        ).filter(provider=provider)

        serializer = ProviderBookingSerializer(queryset, many=True)

        return standard_message(
            message="Booking list",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

    @bookingupdateschema
    def patch(self, request):
        booking_id = request.data.get("booking_id")
        print(f'booking is {booking_id}')
        if not booking_id:
            return standard_message(
                message="booking_id field is required",
                errors={"booking_id": "Missing field"},
                status_code=status.HTTP_400_BAD_REQUEST
            )
        try:
            instance = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return standard_message(
                message="Booking not found",
                errors={"booking_id": "Invalid ID"},
                status_code=status.HTTP_404_NOT_FOUND
            )

            # Provider must own the booking
        if instance.provider != request.user.provider_profile:
            return standard_message(
                message="You are not allowed to update this booking",
                status_code=status.HTTP_403_FORBIDDEN
            )
        previous_status = instance.status

        serializer = ProviderBookingSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return standard_message(
            message="Booking status updated successfully",
            data={
                "booking_id": str(instance.id),
                "previous_status": previous_status,
                "updated_status": instance.status,
                "updated_at": str(instance.updated_at)
            },
            status_code=status.HTTP_200_OK
        )