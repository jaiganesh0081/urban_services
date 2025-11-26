from django.urls import path
from customers.views import ProviderAvailableAPIView, ProviderViewCategoryAPIView

urlpatterns = [
    path("availability/", ProviderAvailableAPIView.as_view(), name="slot-availability"),
    path("category/", ProviderViewCategoryAPIView.as_view(), name="provider-view-category")
]
