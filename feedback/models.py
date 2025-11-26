from uuid import uuid4

from django.db import models

from accounts.models import BaseModel, User
from bookings.models import Booking
from providers.models import ProviderProfile


# Create your models here.


class Feedback(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE, related_name='provider_feedback')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer_feedback")
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="feedback")

    rating = models.IntegerField()
    comment = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'feedback'

    def __str__(self):
        return f"Rating: {self.rating} for {self.provider.user.full_name}"
