from uuid import uuid4

from django.db import models

from accounts.models import BaseModel, User
from providers.models import ProviderProfile
from services.models import Service


# Create your models here.

class BookingStatus(models.TextChoices):
    Pending = "Pending"
    Accepted = "Accepted"
    Rejected = "Rejected"
    Completed = "Completed"
    Paid = "Paid"


class Booking(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE, related_name="provider_booking")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer_booking")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="service_booking")

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    status = models.CharField(max_length=20, choices=BookingStatus.choices, default=BookingStatus.Pending)

    class Meta:
        db_table = "booking"

    def __str__(self):
        return f"Booking-{self.id} ({self.status})"
