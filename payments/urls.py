from django.urls import path
from .views import PaymentCheckoutAPIView
urlpatterns = [
    path("stripe/initiate/", PaymentCheckoutAPIView.as_view(), name="payment-checkout"),
]