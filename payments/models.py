# payments/models.py
from uuid import uuid4
from django.db import models
from bookings.models import Booking
from accounts.models import BaseModel


class PaymentStatus(models.TextChoices):
    Initiated = "Initiated"
    Success = "Success"
    Failed = "Failed"


class PaymentRecord(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="payment")
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_gateway_order_id = models.CharField(max_length=255)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.Initiated)

    def __str__(self):
        return f"Payment-{self.id} ({self.status})"
