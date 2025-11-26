from django.urls import path
from customers.views import ProviderAvailableAPIView



urlpatterns = [
    path("availability/", ProviderAvailableAPIView.as_view(), name="slot-availability")
]
