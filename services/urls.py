from django.urls import path

from .views import ProviderServiceAPIView, ServiceListAPIView

urlpatterns = [
    path("provider-service/", ProviderServiceAPIView.as_view(), name="provider-service"),
    path("list-service/", ServiceListAPIView.as_view(), name='list-service')
]
