from django.urls import path
from .views import BookingServicesAPIView, ProviderBookingAPIView

urlpatterns = [
    path("service/", BookingServicesAPIView.as_view(), name="booking-services"),
    path("status/", ProviderBookingAPIView.as_view(), name="provider-booking-status"),
    # path("status-update/", ProviderBookingAPIView.as_view(), name="provider-booking-update")
]
