from django.urls import path

from .views import ProviderProfileAPIView, ProviderSlotAPIView, ProviderCategoryAPIView

urlpatterns = [
    path("profile/", ProviderProfileAPIView.as_view(), name="provider-profile"),
    path("availability/", ProviderSlotAPIView.as_view(), name="provider-availability"),
    path("category/", ProviderCategoryAPIView.as_view(), name="provider-category")

]
