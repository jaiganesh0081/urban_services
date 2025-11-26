from django.urls import path

from .views import ProviderProfileAPIView, ProviderSlotAPIView

urlpatterns = [
    path("profile/", ProviderProfileAPIView.as_view(), name="provider-profile"),
    path("availability/", ProviderSlotAPIView.as_view(), name="provider-availability"),



]
